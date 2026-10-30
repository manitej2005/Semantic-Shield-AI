"""
Abstract interface for the Explainability Engine.
"""

from abc import ABC, abstractmethod
from typing import List
from app.domain.models.response import AgentResponsePayload
from app.domain.models.risk_score import RiskAssessment


class IExplainabilityEngine(ABC):
    """
    Abstract contract for translating agent technical metrics into human-understandable reasoning.
    """

    @abstractmethod
    def generate_reasons(
        self, agent_responses: List[AgentResponsePayload], assessment: RiskAssessment
    ) -> List[str]:
        """
        Generates clean, deduplicated human-readable bullet points explaining threat metrics.
        """
        pass
