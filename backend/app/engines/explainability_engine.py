"""
Explainability Engine Implementation (Module 2 / Module 5).
Synthesizes agent response vectors and risk metrics into human-readable explanations and actionable recommendations.
Does NOT make additional LLM API calls.
"""

import logging
from typing import List, Dict, Any
from app.domain.interfaces.explainability import IExplainabilityEngine
from app.domain.models.response import AgentResponsePayload
from app.domain.models.risk_score import RiskAssessment, RiskLevel

logger = logging.getLogger(__name__)


class ExplainabilityEngine(IExplainabilityEngine):
    """
    Explainability Engine for generating reasoning and actionable safety recommendations.
    Synthesizes output deterministically without additional LLM latency.
    """

    RECOMMENDATIONS_MAP = {
        "High Risk": [
            "Do not interact with this content or click any links.",
            "Verify sender identity through trusted offline channels.",
            "Report this content to your organization's IT/Security team.",
            "Contact the official organization directly using their verified website or phone number."
        ],
        "Suspicious": [
            "Exercise caution before submitting passwords, banking info, or personal data.",
            "Verify that the destination URL matches the legitimate official domain.",
            "Do not download attachments or approve browser notification permissions."
        ],
        "Safe": [
            "No immediate semantic manipulation or high-risk technical signals detected.",
            "Always verify URLs in your browser address bar before logging in."
        ]
    }

    def generate_reasons(
        self,
        agent_responses: List[AgentResponsePayload],
        assessment: RiskAssessment
    ) -> List[str]:
        """
        Extracts and deduplicates explanatory bullet points from all agent responses.
        """
        reasons: List[str] = []

        for resp in agent_responses:
            if resp.reasoning and "unavailable" not in resp.reasoning.lower():
                reasons.append(resp.reasoning)
            for signal in resp.detected_signals:
                if signal and signal not in reasons and "unavailable" not in signal.lower():
                    reasons.append(signal)

        if not reasons:
            reasons = ["Automated multi-agent security evaluation completed."]

        return list(dict.fromkeys(reasons))

    def generate_agent_summaries(
        self,
        agent_responses: List[AgentResponsePayload]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Formats agent output metrics into the required dictionary format for 'agents':
        {
            "semantic": {"score": 88, "reason": "..."},
            "behavior": {"score": 74, "reason": "..."},
            "url": {"score": 95, "reason": "..."}
        }
        """
        summary = {
            "semantic": {"score": 0, "reason": "Semantic analysis not performed."},
            "behavior": {"score": 0, "reason": "Behavior analysis not performed."},
            "url": {"score": 0, "reason": "URL analysis not performed."}
        }

        for resp in agent_responses:
            score = int(round(resp.threat_score))
            reason = resp.reasoning or (resp.detected_signals[0] if resp.detected_signals else "Evaluation complete.")

            if "semantic" in resp.agent_name.lower():
                summary["semantic"] = {"score": score, "reason": reason}
            elif "behavior" in resp.agent_name.lower():
                summary["behavior"] = {"score": score, "reason": reason}
            elif "url" in resp.agent_name.lower() or "heuristic" in resp.agent_name.lower():
                summary["url"] = {"score": score, "reason": reason}

        return summary

    def generate_recommendations(self, classification: str) -> List[str]:
        """
        Returns actionable user recommendations based on threat classification.
        """
        return self.RECOMMENDATIONS_MAP.get(
            classification,
            self.RECOMMENDATIONS_MAP["Suspicious"]
        )
