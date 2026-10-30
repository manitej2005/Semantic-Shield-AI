"""
Response Pydantic schemas for SemanticShield AI.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentResponsePayload(BaseModel):
    """
    Standardized result contract emitted by every autonomous agent.
    Guarantees 'score', 'label', and 'reasons' fields alongside detailed diagnostic metrics.
    """
    agent_name: str = Field(..., description="Unique identifier of the agent")
    threat_score: float = Field(..., ge=0.0, le=100.0, description="Evaluated threat score (0-100)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Agent decision confidence (0.0 - 1.0)")
    threat_categories: List[str] = Field(default_factory=list, description="Associated threat vectors")
    detected_signals: List[str] = Field(default_factory=list, description="Human-readable warning signals")
    reasoning: str = Field(..., description="Agent reasoning output")
    flags: Dict[str, Any] = Field(default_factory=dict, description="Technical flags and diagnostic markers")

    @property
    def score(self) -> float:
        return self.threat_score

    @property
    def label(self) -> str:
        if self.threat_score >= 65.0:
            return "High Risk"
        elif self.threat_score >= 35.0:
            return "Suspicious"
        else:
            return "Safe"

    @property
    def reasons(self) -> List[str]:
        res: List[str] = []
        if self.reasoning:
            res.append(self.reasoning)
        for sig in self.detected_signals:
            if sig not in res:
                res.append(sig)
        return res if res else ["No specific risk signals detected."]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "label": self.label,
            "reasons": self.reasons,
            "agent_name": self.agent_name,
            "threat_score": self.threat_score,
            "confidence": self.confidence,
            "threat_categories": self.threat_categories,
            "detected_signals": self.detected_signals,
            "reasoning": self.reasoning,
            "flags": self.flags,
        }


class AnalyzeResponse(BaseModel):
    """
    Unified analysis result returned to client interceptors.
    Matches the schema expected by SentinelWeb Guard Chrome Extension.
    """
    risk_score: int = Field(..., ge=0, le=50, description="Aggregate normalized risk score (0-50)")
    risk_level: str = Field(..., description="Categorical risk: safe | suspicious | dangerous")
    threat_categories: List[str] = Field(default_factory=list, description="Active threat categories")
    reasons: List[str] = Field(default_factory=list, description="Aggregated explainability bullet points")
    details: Dict[str, Any] = Field(default_factory=dict, description="Granular analyzer/agent outputs")
