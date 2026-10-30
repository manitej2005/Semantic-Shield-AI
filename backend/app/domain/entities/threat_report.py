"""
Threat report domain entity skeleton.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ThreatReport(BaseModel):
    """
    Domain entity representing a persisted threat analysis report.
    Used for SOC tracking, history, and audit log generation.
    """
    report_id: str = Field(..., description="Unique UUID for this threat record")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    target_url: str = Field(..., description="URL evaluated")
    risk_score: int = Field(..., description="Normalized score 0-50")
    risk_level: str = Field(..., description="Safe, Suspicious, or Dangerous")
    threat_categories: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    agent_summary: Dict[str, Any] = Field(default_factory=dict)
