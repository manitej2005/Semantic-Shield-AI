"""
VirusTotal v3 API Threat Intelligence Provider.
Supports URL, Domain, IP, and File Hash analysis.
"""

import httpx
import base64
from typing import Dict, Any
from app.core.config import settings
from app.services.threat_intelligence.models import ThreatIntelResult
from app.services.threat_intelligence.providers.base import BaseThreatIntelProvider
from app.services.threat_intelligence.providers.registry import provider_registry
from app.utils.reputation import get_reputation_label, get_recommended_action


class VirusTotalProvider(BaseThreatIntelProvider):
    """
    VirusTotal v3 API threat intelligence provider plugin.
    """

    def __init__(self):
        super().__init__(
            provider_name="VirusTotal",
            api_key=settings.VIRUSTOTAL_API_KEY,
            timeout_seconds=10.0,
        )

    def _requires_api_key(self) -> bool:
        return True

    async def _execute_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        headers = {"x-apikey": self.api_key}

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            if indicator_type == "url":
                # VirusTotal URL identifier is base64url without padding
                url_id = base64.urlsafe_b64encode(indicator.encode()).decode().strip("=")
                endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
            elif indicator_type == "domain":
                endpoint = f"https://www.virustotal.com/api/v3/domains/{indicator}"
            elif indicator_type in ["ipv4", "ipv6"]:
                endpoint = f"https://www.virustotal.com/api/v3/ip_addresses/{indicator}"
            else:  # sha256, md5, sha1
                endpoint = f"https://www.virustotal.com/api/v3/files/{indicator}"

            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json().get("data", {}).get("attributes", {})

            stats = data.get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0) + stats.get("undetected", 0)
            total = malicious + suspicious + harmless

            # Calculate risk score (0-100) based on vendor ratio
            ratio = (malicious * 1.0 + suspicious * 0.5) / max(total, 1)
            risk_score = min(100, int(ratio * 100))
            confidence = min(98, int((total / 70.0) * 100)) if total > 0 else 50

            tags = data.get("tags", [])
            categories = list(data.get("categories", {}).values())

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
                last_analysis=data.get("last_analysis_date"),
                tags=tags,
                categories=categories,
                recommendation=get_recommended_action(risk_score, indicator_type, tags),
                raw_data={"stats": stats, "tags": tags[:10]},
            )

    async def _execute_mock_lookup(self, indicator: str, indicator_type: str) -> ThreatIntelResult:
        # Deterministic mock response for Dev Mode / Quota safety
        is_suspicious = any(kw in indicator.lower() for kw in ["phish", "login", "verify", "secure", "bank", "185."])
        
        malicious = 18 if is_suspicious else 0
        suspicious = 3 if is_suspicious else 0
        harmless = 62 if is_suspicious else 75
        risk_score = 92 if is_suspicious else 0
        confidence = 96

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
            last_analysis="2026-08-04T09:00:00Z",
            categories=["phishing", "credential-harvesting"] if is_suspicious else ["harmless"],
            tags=["typosquatting", "executive-impersonation"] if is_suspicious else ["verified-clean"],
            recommendation=get_recommended_action(risk_score, indicator_type, []),
            raw_data={"mock": True, "vendor_count": 83},
        )


# Register provider instance into registry automatically
virustotal_instance = VirusTotalProvider()
provider_registry.register_provider(virustotal_instance)
