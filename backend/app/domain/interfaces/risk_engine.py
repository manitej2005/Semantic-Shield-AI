"""
Abstract interface contract for the Risk Assessment Engine.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.domain.models.response import AgentResponsePayload
from app.domain.models.risk_score import RiskAssessment


class IRiskEngine(ABC):
    """
    Abstract interface for combining agent evaluation outputs into unified risk metrics.
    """

    @abstractmethod
    def calculate_risk(
        self, agent_responses: List[AgentResponsePayload], extra_flags: Optional[Dict[str, Any]] = None
    ) -> RiskAssessment:
        """
        Processes multi-agent outputs and applies security overrides to compute final risk score.
        """
        pass
