"""
AbuseIPDB v2 API Threat Intelligence Provider.
Specialized in IP reputation, abuse reports, ISP, and country metrics.
"""

import httpx
from typing import Dict, Any
from app.core.config import settings
from app.services.threat_intelligence.models import ThreatIntelResult
from app.services.threat_intelligence.providers.base import BaseThreatIntelProvider
from app.services.threat_intelligence.providers.registry import provider_registry
from app.utils.reputation import get_reputation_label, get_recommended_action


class AbuseIPDBProvider(BaseThreatIntelProvider):
    """
    AbuseIPDB v2 API threat intelligence provider plugin.
    """

    def __init__(self):
        super().__init__(
            provider_name="AbuseIPDB",
            api_key=settings.ABUSEIPDB_API_KEY,
            timeout_seconds=10.0,
        )

    def _requires_api_key(self) -> bool:
        return True

    async def _execute_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        if indicator_type not in ["ipv4", "ipv6"]:
            # AbuseIPDB only inspects IP addresses directly
            return await self._execute_mock_lookup(indicator, indicator_type)

        headers = {"Key": self.api_key, "Accept": "application/json"}
        params = {"ipAddress": indicator, "maxAgeInDays": "90", "verbose": ""}

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(
                "https://api.abuseipdb.com/api/v2/check", headers=headers, params=params
            )
            response.raise_for_status()
            data = response.json().get("data", {})

            abuse_score = data.get("abuseConfidenceScore", 0)
            total_reports = data.get("totalReports", 0)

            # Map AbuseIPDB score directly to risk score
            risk_score = abuse_score
            confidence = min(95, 50 + min(45, total_reports * 2))

            return ThreatIntelResult(
                provider=self.provider_name,
                indicator=indicator,
                indicator_type=indicator_type,
                risk_score=risk_score,
                confidence=confidence,
                reputation=get_reputation_label(risk_score),
                malicious=1 if abuse_score > 50 else 0,
                suspicious=1 if 20 <= abuse_score <= 50 else 0,
                harmless=1 if abuse_score < 20 else 0,
                country=data.get("countryCode"),
                asn=f"AS{data.get('asn')}" if data.get('asn') else None,
                tags=[data.get("usageType", "")] if data.get("usageType") else [],
                recommendation=get_recommended_action(risk_score, indicator_type, []),
                raw_data={
                    "abuse_confidence_score": abuse_score,
                    "total_reports": total_reports,
                    "isp": data.get("isp"),
                    "domain": data.get("domain"),
                },
            )

    async def _execute_mock_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        is_suspicious_ip = indicator.startswith(("185.", "45.", "103.", "198.")) or any(
            kw in indicator.lower() for kw in ["phish", "login", "verify", "secure", "bank"]
        )

        if is_suspicious_ip:
            abuse_score = 92
            risk_score = 92
            confidence = 90
            malicious = 1
            suspicious = 0
            harmless = 0
            country = "LU"
            asn = "AS60729"
            tags = ["Data Center/Web Hosting/Transit"]
        else:
            # Controlled mock variability across indicators: clean, suspicious, low-risk
            hash_val = sum(ord(c) for c in indicator) % 3
            if hash_val == 1:
                # low-risk
                abuse_score = 25
                risk_score = 25
                confidence = 85
                malicious = 0
                suspicious = 1
                harmless = 0
                country = "US"
                asn = "AS15169"
                tags = ["Commercial"]
            elif hash_val == 2:
                # suspicious
                abuse_score = 55
                risk_score = 55
                confidence = 88
                malicious = 0
                suspicious = 1
                harmless = 0
                country = "DE"
                asn = "AS24940"
                tags = ["Suspicious Host"]
            else:
                # clean
                abuse_score = 0
                risk_score = 0
                confidence = 90
                malicious = 0
                suspicious = 0
                harmless = 1
                country = "US"
                asn = "AS15169"
                tags = ["Commercial"]

        return ThreatIntelResult(
            provider=self.provider_name,
            indicator=indicator,
            indicator_type=indicator_type,
            risk_score=risk_score,
            confidence=confidence,
            reputation=get_reputation_label(risk_score),
            malicious=malicious,
            suspicious=suspicious,
            harmless=harmless,
            country=country,
            asn=asn,
            tags=tags,
            recommendation=get_recommended_action(risk_score, indicator_type, []),
            raw_data={"mock": True, "total_reports": 142 if is_suspicious_ip else (12 if risk_score > 0 else 0)},
        )


abuseipdb_instance = AbuseIPDBProvider()
provider_registry.register_provider(abuseipdb_instance)
