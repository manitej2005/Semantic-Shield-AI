"""
Telemetry and performance metrics instrumentation for Threat Intelligence.
"""

import time
import asyncio
from typing import Dict, Any


class ThreatIntelTelemetry:
    """
    Internal metrics collector tracking execution times, cache hit ratios, and provider failures.
    """
    def __init__(self):
        self._lock = asyncio.Lock()
        self.total_lookups: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.provider_exec_times: Dict[str, list] = {}
        self.provider_errors: Dict[str, int] = {}
        self.provider_retries: Dict[str, int] = {}

    async def record_lookup(self, cache_hit: bool):
        async with self._lock:
            self.total_lookups += 1
            if cache_hit:
                self.cache_hits += 1
            else:
                self.cache_misses += 1

    async def record_provider_metric(
        self, provider: str, duration_ms: float, is_error: bool = False, is_retry: bool = False
    ):
        async with self._lock:
            if provider not in self.provider_exec_times:
                self.provider_exec_times[provider] = []
                self.provider_errors[provider] = 0
                self.provider_retries[provider] = 0

            self.provider_exec_times[provider].append(duration_ms)
            # Keep recent 100 duration samples
            if len(self.provider_exec_times[provider]) > 100:
                self.provider_exec_times[provider].pop(0)

            if is_error:
                self.provider_errors[provider] += 1
            if is_retry:
                self.provider_retries[provider] += 1

    async def get_metrics_snapshot(self) -> Dict[str, Any]:
        async with self._lock:
            avg_times = {}
            for prov, times in self.provider_exec_times.items():
                avg_times[prov] = round(sum(times) / len(times), 2) if times else 0.0

            return {
                "total_lookups": self.total_lookups,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_ratio": (
                    round(self.cache_hits / self.total_lookups, 4) if self.total_lookups > 0 else 0.0
                ),
                "avg_response_times_ms": avg_times,
                "provider_errors": self.provider_errors.copy(),
                "provider_retries": self.provider_retries.copy(),
            }


telemetry_instance = ThreatIntelTelemetry()
