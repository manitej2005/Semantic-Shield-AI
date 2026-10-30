"""
Risk score domain types and metrics.
"""

from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    DANGEROUS = "dangerous"


class ThreatCategory(str, Enum):
    PHISHING = "phishing"
    MALWARE_DISTRIBUTION = "malware_distribution"
    PIRACY = "piracy"
    SOCIAL_ENGINEERING = "social_engineering"
    DECEPTIVE_ADS = "deceptive_ads"
    NOTIFICATION_ABUSE = "notification_abuse"
    AUTHORITY_ABUSE = "authority_abuse"


class RiskAssessment(BaseModel):
    """
    Domain entity encapsulating computed security evaluation.
    """
    raw_score: float = Field(..., ge=0.0, le=100.0)
    normalized_score: int = Field(..., ge=0, le=50)
    risk_level: RiskLevel
    categories: List[ThreatCategory] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    agent_outputs: Dict[str, Any] = Field(default_factory=dict)
