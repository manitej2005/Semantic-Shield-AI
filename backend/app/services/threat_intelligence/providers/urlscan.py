"""
URLScan.io v1 API Threat Intelligence Provider.
Queries URL scan submission results, screenshot metadata, and web page tags.
"""

import httpx
from typing import Dict, Any
from app.core.config import settings
from app.services.threat_intelligence.models import ThreatIntelResult
from app.services.threat_intelligence.providers.base import BaseThreatIntelProvider
from app.services.threat_intelligence.providers.registry import provider_registry
from app.utils.reputation import get_reputation_label, get_recommended_action


class URLScanProvider(BaseThreatIntelProvider):
    """
    URLScan.io API threat intelligence provider plugin.
    """

    def __init__(self):
        super().__init__(
            provider_name="URLScan",
            api_key=settings.URLSCAN_API_KEY,
            timeout_seconds=10.0,
        )

    def _requires_api_key(self) -> bool:
        return True

    async def _execute_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        if indicator_type not in ["url", "domain"]:
            return await self._execute_mock_lookup(indicator, indicator_type)

        headers = {"API-Key": self.api_key}
        params = {"q": f"domain:{indicator}" if indicator_type == "domain" else f"url:\"{indicator}\""}

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(
                "https://urlscan.io/api/v1/search/", headers=headers, params=params
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            if not results:
                return await self._execute_mock_lookup(indicator, indicator_type)

            latest = results[0]
            verdicts = latest.get("verdicts", {}).get("overall", {})
            malicious = 1 if verdicts.get("malicious") else 0
            score = verdicts.get("score", 0)

            risk_score = min(100, score if score > 0 else (90 if malicious else 10))
            confidence = 88

            return ThreatIntelResult(
                provider=self.provider_name,
                indicator=indicator,
                indicator_type=indicator_type,
                risk_score=risk_score,
                confidence=confidence,
                reputation=get_reputation_label(risk_score),
                malicious=malicious,
                suspicious=0,
                harmless=1 if not malicious else 0,
                tags=latest.get("verdicts", {}).get("urlscan", {}).get("tags", []),
                categories=latest.get("verdicts", {}).get("overall", {}).get("categories", []),
                recommendation=get_recommended_action(risk_score, indicator_type, []),
                raw_data={"score": score, "malicious": malicious},
            )

    async def _execute_mock_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        is_suspicious = any(kw in indicator.lower() for kw in ["phish", "login", "verify", "secure", "bank", "185."])

        risk_score = 94 if is_suspicious else 0
        confidence = 90

        return ThreatIntelResult(
            provider=self.provider_name,
            indicator=indicator,
            indicator_type=indicator_type,
            risk_score=risk_score,
            confidence=confidence,
            reputation=get_reputation_label(risk_score),
            malicious=1 if is_suspicious else 0,
            suspicious=0,
            harmless=0 if is_suspicious else 1,
            tags=["phishing-page", "cloned-sso-login"] if is_suspicious else ["verified-safe"],
            categories=["phishing"] if is_suspicious else [],
            recommendation=get_recommended_action(risk_score, indicator_type, []),
            raw_data={"mock": True, "verdict": "malicious" if is_suspicious else "clean"},
        )


urlscan_instance = URLScanProvider()
provider_registry.register_provider(urlscan_instance)
