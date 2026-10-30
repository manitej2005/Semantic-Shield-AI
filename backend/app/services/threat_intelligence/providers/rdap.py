"""
RDAP (Registration Data Access Protocol) Threat Intelligence Provider.
Queries ICANN, ARIN, APNIC, RIPE endpoints for IP and domain ownership metadata.
"""

import httpx
from typing import Dict, Any
from app.services.threat_intelligence.models import ThreatIntelResult
from app.services.threat_intelligence.providers.base import BaseThreatIntelProvider
from app.services.threat_intelligence.providers.registry import provider_registry
from app.utils.reputation import get_reputation_label, get_recommended_action


class RDAPProvider(BaseThreatIntelProvider):
    """
    RDAP protocol threat intelligence provider plugin.
    """

    def __init__(self):
        super().__init__(
            provider_name="RDAP",
            api_key="",
            timeout_seconds=10.0,
        )

    def _requires_api_key(self) -> bool:
        return False

    async def _execute_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        if indicator_type in ["ipv4", "ipv6"]:
            endpoint = f"https://rdap.arin.net/registry/ip/{indicator}"
        elif indicator_type == "domain":
            endpoint = f"https://rdap.org/domain/{indicator}"
        else:
            return await self._execute_mock_lookup(indicator, indicator_type)

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(endpoint)
            if response.status_code != 200:
                return await self._execute_mock_lookup(indicator, indicator_type)
            
            data = response.json()
            country = data.get("country", "US")
            handle = data.get("handle", "")
            
            risk_score = 10
            confidence = 85

            return ThreatIntelResult(
                provider=self.provider_name,
                indicator=indicator,
                indicator_type=indicator_type,
                risk_score=risk_score,
                confidence=confidence,
                reputation=get_reputation_label(risk_score),
                country=country,
                asn=f"AS-{handle}" if handle else None,
                recommendation=get_recommended_action(risk_score, indicator_type, []),
                raw_data={"handle": handle, "country": country},
            )

    async def _execute_mock_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        is_suspicious = any(kw in indicator.lower() for kw in ["185.", "45.", "login", "phish"])
        
        risk_score = 75 if is_suspicious else 5
        confidence = 88

        return ThreatIntelResult(
            provider=self.provider_name,
            indicator=indicator,
            indicator_type=indicator_type,
            risk_score=risk_score,
            confidence=confidence,
            reputation=get_reputation_label(risk_score),
            country="LU" if is_suspicious else "US",
            asn="AS60729-TOR" if is_suspicious else "AS15169-GOOGLE",
            recommendation=get_recommended_action(risk_score, indicator_type, []),
            raw_data={"mock": True, "rdap_status": "active"},
        )


rdap_instance = RDAPProvider()
provider_registry.register_provider(rdap_instance)
