"""
AI Context Builder for threat intelligence evaluation.
Transforms normalized provider outputs into concise JSON context payloads for Gemini LLM agents.
"""

from typing import List, Dict, Any
from app.services.threat_intelligence.models import ThreatIntelResult
from app.utils.reputation import get_reputation_label, get_recommended_action


class AIContextBuilder:
    """
    Generates structured AI-ready context for Offensive AI and Defensive AI agents.
    """

    @staticmethod
    def build_context(
        indicator: str,
        indicator_type: str,
        risk_score: int,
        confidence: int,
        providers: List[ThreatIntelResult],
    ) -> Dict[str, Any]:
        """
        Builds normalized AI agent prompt payload.
        """
        key_findings = []
        categories = set()
        tags = set()
        malicious_providers = []
        ioc_summary = {}

        for p in providers:
            if p.risk_score >= 70:
                malicious_providers.append(p.provider)
                key_findings.append(f"{p.provider} flagged high risk score ({p.risk_score}/100)")
            for cat in p.categories:
                categories.add(cat)
            for t in p.tags:
                tags.add(t)

            if p.country and "country" not in ioc_summary:
                ioc_summary["country"] = p.country
            if p.asn and "asn" not in ioc_summary:
                ioc_summary["asn"] = p.asn
            if p.registrar and "registrar" not in ioc_summary:
                ioc_summary["registrar"] = p.registrar
            if p.domain_age is not None and "domain_age_days" not in ioc_summary:
                ioc_summary["domain_age_days"] = p.domain_age

        if ioc_summary.get("domain_age_days", 999) < 7:
            key_findings.append(f"Domain registered < 7 days ago ({ioc_summary.get('domain_age_days')} days old)")

        total_p = max(len(providers), 1)
        consensus_ratio = f"{len(malicious_providers)}/{total_p} providers flagged malicious"

        reputation = get_reputation_label(risk_score)
        rec_action = get_recommended_action(risk_score, indicator_type, list(tags))

        if risk_score >= 85:
            summary = f"CRITICAL THREAT: {indicator} ({indicator_type}) verified malicious by {consensus_ratio} with high confidence."
        elif risk_score >= 70:
            summary = f"HIGH THREAT: {indicator} ({indicator_type}) exhibits strong phishing indicators."
        elif risk_score >= 40:
            summary = f"SUSPICIOUS: {indicator} ({indicator_type}) exhibits anomalous signals under investigation."
        else:
            summary = f"CLEAN: {indicator} ({indicator_type}) verified safe across threat intelligence providers."

        return {
            "indicator": indicator,
            "indicator_type": indicator_type,
            "risk_score": risk_score,
            "confidence": confidence,
            "reputation": reputation,
            "summary": summary,
            "key_findings": key_findings if key_findings else ["Verified clean across all active provider plugins"],
            "recommended_action": rec_action,
            "provider_consensus": consensus_ratio,
            "categories": list(categories),
            "tags": list(tags),
            "ioc_summary": ioc_summary,
        }
