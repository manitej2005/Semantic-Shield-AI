"""
Anti-Hallucination Response Parser and JSON Validator.
"""

import json
from typing import Dict, Any


class ResponseParser:
    """
    Parses LLM outputs and enforces anti-hallucination evidence validation.
    """

    @staticmethod
    def parse_and_validate(llm_output: Dict[str, Any], evidence_payload: Dict[str, Any]) -> Dict[str, Any]:
        # Anti-hallucination check: If telemetry is empty, force 'Insufficient Evidence'
        if not evidence_payload or (not evidence_payload.get("subject") and not evidence_payload.get("unified_iocs")):
            return {
                "verdict": "Insufficient Evidence",
                "confidence_score": 100,
                "explanation": "Provided evidence telemetry is empty or insufficient to evaluate phishing intent.",
                "key_findings": ["No headers or IoCs available for investigation."],
                "attack_techniques": [],
                "mitre_ids": [],
                "business_impact": "None evaluated due to missing telemetry.",
                "recommended_actions": ["Provide raw email or URL payload for analysis."],
            }

        # Normalize verdict
        verdict = llm_output.get("verdict", "Suspicious")
        if verdict not in ["Safe", "Suspicious", "Phishing", "Critical", "Insufficient Evidence"]:
            verdict = "Suspicious"

        confidence = max(0, min(100, llm_output.get("confidence_score", 85)))

        return {
            "verdict": verdict,
            "confidence_score": confidence,
            "explanation": llm_output.get("explanation", "Investigation complete."),
            "key_findings": llm_output.get("key_findings", []),
            "attack_techniques": llm_output.get("attack_techniques", []),
            "mitre_ids": llm_output.get("mitre_ids", ["T1566"]),
            "business_impact": llm_output.get("business_impact", "Potential threat risk."),
            "recommended_actions": llm_output.get("recommended_actions", ["Review incident telemetry."]),
        }
