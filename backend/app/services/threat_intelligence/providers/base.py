"""
Abstract Base Provider for Threat Intelligence services.
Enforces async HTTPX client, 10s timeouts, retry logic, mock fallback, and telemetry hooks.
"""

import time
import logging
import httpx
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.core.config import settings
from app.services.threat_intelligence.models import ThreatIntelResult
from app.services.threat_intelligence.provider_health import health_monitor_instance
from app.services.threat_intelligence.telemetry import telemetry_instance

logger = logging.getLogger("app.services.threat_intelligence")


class BaseThreatIntelProvider(ABC):
    """
    Abstract base provider class for all threat intelligence sources.
    """

    def __init__(self, provider_name: str, api_key: str = "", timeout_seconds: float = 10.0):
        self.provider_name = provider_name
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    @property
    def is_mock_mode(self) -> bool:
        """
        Determines if provider should run in Mock Mode.
        True if settings.THREAT_INTEL_MOCK_MODE is enabled or if API key is required but missing.
        """
        if settings.THREAT_INTEL_MOCK_MODE:
            return True
        if self._requires_api_key() and not self.api_key:
            return True
        return False

    def _requires_api_key(self) -> bool:
        return True

    @abstractmethod
    async def _execute_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        """
        Implementation method for live API lookup.
        """
        pass

    @abstractmethod
    async def _execute_mock_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        """
        Implementation method for deterministic mock lookup.
        """
        pass

    async def lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        """
        Public lookup execution wrapper with retries, timeout, telemetry, and error safety.
        """
        start_time = time.time()

        if self.is_mock_mode:
            logger.info(f"[{self.provider_name}] Executing MOCK lookup for '{indicator}' ({indicator_type})")
            res = await self._execute_mock_lookup(indicator, indicator_type)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            await health_monitor_instance.record_success(self.provider_name, duration_ms)
            await telemetry_instance.record_provider_metric(self.provider_name, duration_ms)
            return res

        # Live execution with retries
        retries = 2
        last_exception = None

        for attempt in range(1 + retries):
            try:
                logger.info(f"[{self.provider_name}] Attempt {attempt + 1}: Live lookup for '{indicator}'")
                res = await asyncio.wait_for(
                    self._execute_lookup(indicator, indicator_type),
                    timeout=self.timeout_seconds,
                )
                duration_ms = round((time.time() - start_time) * 1000, 2)
                await health_monitor_instance.record_success(self.provider_name, duration_ms)
                await telemetry_instance.record_provider_metric(
                    self.provider_name, duration_ms, is_retry=(attempt > 0)
                )
                return res

            except (httpx.HTTPStatusError, httpx.RequestError, asyncio.TimeoutError) as exc:
                last_exception = exc
                is_retry = attempt < retries
                logger.warning(
                    f"[{self.provider_name}] Request failed (attempt {attempt + 1}): {str(exc)}. Retrying: {is_retry}"
                )
                await telemetry_instance.record_provider_metric(
                    self.provider_name, 0.0, is_error=True, is_retry=is_retry
                )
                if is_retry:
                    await asyncio.sleep(0.5 * (attempt + 1))
                else:
                    status_code = getattr(getattr(exc, "response", None), "status_code", None)
                    await health_monitor_instance.record_failure(self.provider_name, status_code)

            except Exception as exc:
                logger.error(f"[{self.provider_name}] Unexpected failure: {str(exc)}", exc_info=True)
                await health_monitor_instance.record_failure(self.provider_name)
                break

        # Fallback to mock/safe response on persistent failure
        logger.warning(f"[{self.provider_name}] Falling back to safe fallback response due to: {last_exception}")
        return await self._execute_mock_lookup(indicator, indicator_type)
