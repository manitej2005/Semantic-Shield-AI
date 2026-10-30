"""
Threat Intelligence Manager & Orchestration Engine.
Orchestrates concurrent provider execution, caching, telemetry, scoring, and AI context building.
"""

import time
import logging
import asyncio
from typing import Optional, List
from app.utils.ioc import IOCNormalizer, IOC
from app.services.threat_intelligence.models import ThreatIntelResult, ThreatAnalyzeResponse
from app.services.threat_intelligence.providers.registry import provider_registry
from app.services.threat_intelligence.scoring import ThreatScoringEngine
from app.services.threat_intelligence.context_builder import AIContextBuilder
from app.services.threat_intelligence.cache import cache_instance
from app.services.threat_intelligence.telemetry import telemetry_instance
from app.services.threat_intelligence.provider_health import health_monitor_instance

# Force import of providers so plugins register themselves
import app.services.threat_intelligence.providers.virustotal
import app.services.threat_intelligence.providers.abuseipdb
import app.services.threat_intelligence.providers.whois
import app.services.threat_intelligence.providers.rdap
import app.services.threat_intelligence.providers.urlscan

logger = logging.getLogger("app.services.threat_intelligence")


class ThreatIntelManager:
    """
    Core Orchestrator managing threat intelligence investigations.
    """

    async def analyze_indicator(
        self, raw_indicator: str, force_type: Optional[str] = None
    ) -> ThreatAnalyzeResponse:
        """
        Performs full asynchronous investigation across registered intelligence providers.
        """
        start_time = time.time()

        # 1. Normalize IoC
        ioc: IOC = IOCNormalizer.normalize(raw_indicator, force_type=force_type)
        logger.info(f"[ThreatManager] Investigating '{ioc.normalized_value}' (Type: {ioc.type})")

        # 2. Check Cache
        cached_val = await cache_instance.get(ioc.hash_key)
        if cached_val:
            logger.info(f"[ThreatManager] Cache HIT for key {ioc.hash_key[:12]}...")
            await telemetry_instance.record_lookup(cache_hit=True)
            cached_val.execution_time_ms = round((time.time() - start_time) * 1000, 2)
            cached_val.cache_hit = True
            return cached_val

        await telemetry_instance.record_lookup(cache_hit=False)

        # 3. Retrieve Registered Provider Plugins
        providers = provider_registry.get_registered_providers()
        if not providers:
            logger.warning("[ThreatManager] No threat providers registered in registry!")

        # 4. Dispatch Provider Queries Concurrently
        tasks = [p.lookup(ioc.normalized_value, ioc.type) for p in providers]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter valid ThreatIntelResult instances
        provider_results: List[ThreatIntelResult] = []
        for p, res in zip(providers, raw_results):
            if isinstance(res, ThreatIntelResult):
                provider_results.append(res)
            elif isinstance(res, Exception):
                logger.error(f"[ThreatManager] Provider '{p.provider_name}' crashed: {str(res)}")
                await health_monitor_instance.record_failure(p.provider_name)

        # 5. Dual Metric Scoring (Risk Score & Confidence Score)
        risk_score, confidence_score = ThreatScoringEngine.calculate_composite_scores(provider_results)

        # 6. Build AI Agent Context Payload
        ai_context = AIContextBuilder.build_context(
            indicator=ioc.normalized_value,
            indicator_type=ioc.type,
            risk_score=risk_score,
            confidence=confidence_score,
            providers=provider_results,
        )

        execution_time = round((time.time() - start_time) * 1000, 2)

        response = ThreatAnalyzeResponse(
            indicator=ioc.normalized_value,
            type=ioc.type,
            risk_score=risk_score,
            confidence=confidence_score,
            reputation=ai_context.get("reputation", "Unknown"),
            recommendation=ai_context.get("recommended_action", ""),
            providers=provider_results,
            ai_context=ai_context,
            cache_hit=False,
            execution_time_ms=execution_time,
        )

        # 7. Store Result in Cache
        await cache_instance.set(ioc.hash_key, response)

        return response


# Global manager instance
threat_intel_manager = ThreatIntelManager()
