"""
Risk Assessment Engine Implementation (Module 2 / Module 4).
Calculates weighted composite risk score from multi-agent output vectors.
Applies security overrides, classification, and confidence scoring.
"""

import logging
from typing import List, Dict, Any, Optional

from app.domain.interfaces.risk_engine import IRiskEngine
from app.domain.models.response import AgentResponsePayload
from app.domain.models.risk_score import RiskAssessment, RiskLevel, ThreatCategory

logger = logging.getLogger(__name__)


class RiskEngine(IRiskEngine):
    """
    Weighted Risk Assessment Engine.
    Combines agent responses according to Module 2 specifications:
    - Semantic Agent = 40%
    - Behavior Agent = 25%
    - URL Intelligence Agent = 35%
    """

    WEIGHTS = {
        "Semantic Analysis Agent": 0.40,
        "Behavior Analysis Agent": 0.25,
        "URL Intelligence Agent": 0.35,
    }

    def calculate_risk(
        self,
        agent_responses: List[AgentResponsePayload],
        extra_flags: Optional[Dict[str, Any]] = None
    ) -> RiskAssessment:
        """
        Calculates weighted composite risk score, classification, and confidence.
        """
        if not agent_responses:
            return RiskAssessment(
                raw_score=0.0,
                normalized_score=0,
                risk_level=RiskLevel.SAFE,
                categories=[],
                reasons=["No agent responses available."],
                agent_outputs={}
            )

        scores_by_agent: Dict[str, float] = {}
        confidences_by_agent: Dict[str, float] = {}

        for resp in agent_responses:
            scores_by_agent[resp.agent_name] = resp.threat_score
            confidences_by_agent[resp.agent_name] = resp.confidence

        # Calculate weighted average
        weighted_score = 0.0
        total_weight_applied = 0.0

        for agent_name, weight in self.WEIGHTS.items():
            if agent_name in scores_by_agent:
                weighted_score += scores_by_agent[agent_name] * weight
                total_weight_applied += weight

        if total_weight_applied > 0:
            raw_score = weighted_score / total_weight_applied
        else:
            raw_score = sum(scores_by_agent.values()) / len(scores_by_agent)

        # High signal security boost & risk floor enforcement
        max_agent_score = max(scores_by_agent.values()) if scores_by_agent else 0.0
        if max_agent_score >= 80.0:
            raw_score = max(raw_score, (raw_score * 0.20) + (max_agent_score * 0.80))
        elif max_agent_score >= 60.0:
            raw_score = max(raw_score, (raw_score * 0.35) + (max_agent_score * 0.65))
        elif max_agent_score >= 45.0:
            raw_score = max(raw_score, (raw_score * 0.50) + (max_agent_score * 0.50))

        raw_score = max(0.0, min(100.0, raw_score))

        # 0-50 normalized score for Chrome extension compatibility
        normalized_score = int(round(raw_score * 0.5))
        normalized_score = max(0, min(50, normalized_score))

        # Determine Classification and RiskLevel
        if raw_score >= 65.0:
            risk_level = RiskLevel.DANGEROUS
        elif raw_score >= 35.0:
            risk_level = RiskLevel.SUSPICIOUS
        else:
            risk_level = RiskLevel.SAFE

        # Compute average confidence across active agents
        valid_confidences = [c for c in confidences_by_agent.values() if c > 0]
        avg_confidence = round(sum(valid_confidences) / len(valid_confidences), 2) if valid_confidences else 0.85

        # Merge threat categories across all agents
        all_categories = []
        all_reasons = []

        for resp in agent_responses:
            all_categories.extend(resp.threat_categories)
            if resp.reasoning:
                all_reasons.append(resp.reasoning)
            for signal in resp.detected_signals:
                if signal not in all_reasons:
                    all_reasons.append(signal)

        dedup_categories = [ThreatCategory(c) for c in set(all_categories) if c in [item.value for item in ThreatCategory]]

        return RiskAssessment(
            raw_score=round(raw_score, 1),
            normalized_score=normalized_score,
            risk_level=risk_level,
            categories=dedup_categories,
            reasons=list(dict.fromkeys(all_reasons)),
            agent_outputs={
                "confidence": avg_confidence,
                "scores_by_agent": scores_by_agent
            }
        )
