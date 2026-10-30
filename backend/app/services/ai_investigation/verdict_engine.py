"""
Verdict & Confidence Decision Engine combining heuristics, threat scores, and LLM reasoning.
"""

from typing import Tuple, Dict, Any
from app.schemas.investigation import VerdictType


class VerdictEngine:
    """
    Computes composite verdict and confidence score.
    """

    @staticmethod
    def compute_final_verdict(risk_score: int, llm_verdict: str) -> Tuple[VerdictType, int]:
        """
        Calculates unified verdict and confidence score.
        """
        # Determine verdict threshold
        if risk_score >= 85 or llm_verdict == "Critical":
            final_verdict: VerdictType = "Critical"
            confidence = 96
        elif risk_score >= 70 or llm_verdict == "Phishing":
            final_verdict = "Phishing"
            confidence = 92
        elif risk_score >= 35 or llm_verdict == "Suspicious":
            final_verdict = "Suspicious"
            confidence = 85
        else:
            final_verdict = "Safe"
            confidence = 98

        return final_verdict, confidence
