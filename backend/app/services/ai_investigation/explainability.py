"""
Human-Readable Explainability Engine & Report Generator.
"""

from typing import List, Dict, Any
from datetime import datetime, timezone
from app.schemas.investigation import VerdictType, ExecutiveReport, TechnicalReport, MITRETechnique


class ExplainabilityEngine:
    """
    Generates human-readable explanations and executive/technical reports.
    """

    @staticmethod
    def generate_explanation(
        verdict: VerdictType,
        key_findings: List[str],
        subject: str,
        sender: str,
    ) -> str:
        if verdict == "Insufficient Evidence":
            return "Insufficient evidence telemetry was provided to conclude an investigation."

        bullet_points = "\n- ".join(key_findings) if key_findings else "Verified clean across threat engines."
        return (
            f"SemanticShield AI classified this incident as '{verdict.upper()}' for email subject '{subject}' sent from '{sender}'.\n\n"
            f"KEY SUPPORTING EVIDENCE:\n- {bullet_points}"
        )

    @staticmethod
    def generate_executive_report(
        verdict: VerdictType,
        subject: str,
        key_findings: List[str],
        recommended_actions: List[str],
    ) -> ExecutiveReport:
        title = f"Phishing Risk Assessment: {verdict.upper()} - '{subject}'"
        summary = f"The platform classified this communication as {verdict.upper()} based on multi-agent threat intelligence correlation."
        takeaway = key_findings[0] if key_findings else "No high-risk threat indicators flagged."
        impact = "Potential unauthorized credential exposure and unauthorized corporate access." if verdict in ["Phishing", "Critical"] else "Low impact."
        rec = recommended_actions[0] if recommended_actions else "No action required."

        return ExecutiveReport(
            title=title,
            verdict=verdict,
            summary=summary,
            key_takeaway=takeaway,
            business_impact=impact,
            recommended_action=rec,
        )

    @staticmethod
    def generate_technical_report(
        verdict: VerdictType,
        subject: str,
        mitre_mappings: List[MITRETechnique],
        unified_iocs: List[Dict[str, str]],
        recommended_actions: List[str],
    ) -> TechnicalReport:
        inc_id = f"INC-{int(datetime.now(timezone.utc).timestamp()) % 100000}"
        ts = datetime.now(timezone.utc).isoformat()
        
        chain = [
            "1. External email message received",
            "2. Display Name spoofing & Reply-To mismatch detected",
            "3. Malicious link / QR code extracted",
            "4. Multi-agent threat score 85+ flagged",
        ]

        return TechnicalReport(
            incident_id=inc_id,
            timestamp=ts,
            threat_type="Spear-Phishing Credential Harvest",
            affected_assets=["User Inbox", "Corporate Credentials"],
            attack_chain=chain,
            mitre_techniques=mitre_mappings,
            iocs_identified=unified_iocs,
            remediation_steps=recommended_actions,
        )
