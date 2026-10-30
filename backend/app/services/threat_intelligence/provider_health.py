"""
Provider Health Monitor service for tracking API availability and latency telemetry.
"""

import time
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.services.threat_intelligence.models import ProviderHealthStatus


class ProviderHealthMonitor:
    """
    Monitors operational health metrics for registered threat intelligence providers.
    """
    def __init__(self):
        self._lock = asyncio.Lock()
        self._health_map: Dict[str, Dict[str, Any]] = {}

    def _ensure_registered_unlocked(self, provider_name: str):
        """Helper to ensure entry exists without acquiring lock twice."""
        if provider_name not in self._health_map:
            self._health_map[provider_name] = {
                "provider": provider_name,
                "status": "operational",
                "reachability": True,
                "latencies": [],
                "consecutive_failures": 0,
                "last_successful_request": None,
                "rate_limit_status": "OK",
            }

    async def register_provider(self, provider_name: str):
        async with self._lock:
            self._ensure_registered_unlocked(provider_name)

    async def record_success(self, provider_name: str, latency_ms: float):
        async with self._lock:
            self._ensure_registered_unlocked(provider_name)
            
            entry = self._health_map[provider_name]
            entry["consecutive_failures"] = 0
            entry["reachability"] = True
            entry["status"] = "operational"
            entry["last_successful_request"] = datetime.now(timezone.utc).isoformat()
            entry["latencies"].append(latency_ms)
            if len(entry["latencies"]) > 50:
                entry["latencies"].pop(0)

    async def record_failure(self, provider_name: str, error_code: Optional[int] = None):
        async with self._lock:
            self._ensure_registered_unlocked(provider_name)
            
            entry = self._health_map[provider_name]
            entry["consecutive_failures"] += 1
            if error_code == 429:
                entry["rate_limit_status"] = "RATE_LIMITED"
                entry["status"] = "degraded"
            elif entry["consecutive_failures"] >= 3:
                entry["status"] = "degraded"
            elif entry["consecutive_failures"] >= 5:
                entry["status"] = "offline"
                entry["reachability"] = False

    async def get_all_health(self) -> List[ProviderHealthStatus]:
        async with self._lock:
            results = []
            for name, entry in self._health_map.items():
                lats = entry["latencies"]
                avg_ms = round(sum(lats) / len(lats), 2) if lats else 0.0
                results.append(
                    ProviderHealthStatus(
                        provider=entry["provider"],
                        status=entry["status"],
                        reachability=entry["reachability"],
                        avg_response_time_ms=avg_ms,
                        consecutive_failures=entry["consecutive_failures"],
                        last_successful_request=entry["last_successful_request"],
                        rate_limit_status=entry["rate_limit_status"],
                    )
                )
            return results


health_monitor_instance = ProviderHealthMonitor()
