"""
Thread-safe, async-compatible memory and Redis-ready Cache Layer for Threat Intelligence.
"""

import time
import asyncio
from typing import Dict, Any, Optional, Tuple
from app.core.config import settings


class ThreatIntelCache:
    """
    In-memory TTL cache with Redis compatibility interface.
    """
    def __init__(self, default_ttl: int = settings.THREAT_INTEL_CACHE_TTL):
        self._store: Dict[str, Tuple[Any, float]] = {}
        self._lock = asyncio.Lock()
        self._default_ttl = default_ttl

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key not in self._store:
                return None
            val, expire_at = self._store[key]
            if time.time() > expire_at:
                del self._store[key]
                return None
            return val

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        duration = ttl if ttl is not None else self._default_ttl
        expire_at = time.time() + duration
        async with self._lock:
            self._store[key] = (value, expire_at)

    async def has(self, key: str) -> bool:
        res = await self.get(key)
        return res is not None

    async def clear(self) -> None:
        async with self._lock:
            self._store.clear()


# Global singleton cache instance
cache_instance = ThreatIntelCache()
