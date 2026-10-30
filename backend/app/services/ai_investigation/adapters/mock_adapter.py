"""
Deterministic Mock LLM Adapter for Dev Mode & Quota-safe execution.
"""

from typing import Dict, Any
from app.services.ai_investigation.adapters.base import BaseLLMAdapter


class MockLLMAdapter(BaseLLMAdapter):
    """
    Deterministic reasoning adapter returning structured analysis without consuming API quotas.
    """

    def __init__(self):
        super().__init__(model_name="mock-reasoning-engine")

    async def investigate(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        risk_score = evidence.get("overall_risk_score", 0)
        subject = evidence.get("subject", "")
        sender = evidence.get("sender", "")
        display_name_spoofing = evidence.get("display_name_spoofing", False)
        brand = evidence.get("brand_impersonation")
        url_count = evidence.get("extracted_urls_count", 0)
        qr_count = evidence.get("qr_detected", 0)

        if risk_score >= 85 or display_name_spoofing or brand:
            verdict = "Critical" if risk_score >= 85 else "Phishing"
            explanation = (
                f"High-confidence phishing attack detected. Sender '{sender}' impersonates '{brand or 'Executive'}' "
                f"using display name spoofing and urgent credential harvesting triggers across {url_count} extracted links."
            )
            key_findings = [
                f"Sender display name '{evidence.get('display_name')}' spoofed target brand '{brand}'",
                f"Extracted {url_count} malicious links and {qr_count} embedded QR code payloads",
                "High-pressure urgency and credential harvesting themes identified",
            ]
            attack_techniques = ["Spearphishing Link", "Display Name Spoofing", "Credential Harvesting"]
            mitre_ids = ["T1566.002", "T1566.003", "T1204.002"]
            impact = "High risk of corporate credential compromise and unauthorized account takeover."
            actions = [
                "Quarantine email across user inboxes",
                "Block malicious sender domain across perimeter firewall",
                "Force MFA re-authentication for targeted user",
            ]
        elif risk_score >= 40:
            verdict = "Suspicious"
            explanation = f"Suspicious email indicators detected for subject '{subject}'. Requires analyst review."
            key_findings = [f"Risk score {risk_score}/100", f"Contains {url_count} external links"]
            attack_techniques = ["Phishing Link"]
            mitre_ids = ["T1566"]
            impact = "Moderate risk of social engineering."
            actions = ["Assign to analyst queue for manual inspection."]
        else:
            verdict = "Safe"
            explanation = f"No malicious phishing indicators or social engineering triggers identified."
            key_findings = ["Verified clean email telemetry across all active analysis engines."]
            attack_techniques = []
            mitre_ids = []
            impact = "Zero identified impact."
            actions = ["No action required."]

        return {
            "verdict": verdict,
            "confidence_score": 92 if verdict != "Safe" else 98,
            "explanation": explanation,
            "key_findings": key_findings,
            "attack_techniques": attack_techniques,
            "mitre_ids": mitre_ids,
            "business_impact": impact,
            "recommended_actions": actions,
        }
