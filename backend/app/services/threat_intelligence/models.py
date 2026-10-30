"""
Data models and Pydantic schemas for the Threat Intelligence Engine.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ThreatIntelResult(BaseModel):
    """
    Normalized result schema returned by individual threat intelligence providers.
    """
    provider: str
    indicator: str
    indicator_type: str
    risk_score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    reputation: str
    malicious: int = 0
    suspicious: int = 0
    harmless: int = 0
    last_analysis: Optional[str] = None
    country: Optional[str] = None
    asn: Optional[str] = None
    registrar: Optional[str] = None
    domain_age: Optional[int] = None  # Age in days
    creation_date: Optional[str] = None
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    recommendation: str
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class ThreatAnalyzeRequest(BaseModel):
    """
    Request model for threat intelligence investigation endpoint.
    """
    indicator: str = Field(..., description="URL, Domain, IP, Hash, or Email to analyze")
    type: Optional[str] = Field(None, description="Optional type override: url, domain, ip, hash, email")


class ThreatAnalyzeResponse(BaseModel):
    """
    Unified composite response model returned by the Threat Intelligence Engine.
    """
    indicator: str
    type: str
    risk_score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    reputation: str
    recommendation: str
    providers: List[ThreatIntelResult] = Field(default_factory=list)
    ai_context: Dict[str, Any] = Field(default_factory=dict)
    cache_hit: bool = False
    execution_time_ms: float = 0.0


class ProviderHealthStatus(BaseModel):
    """
    Health telemetry model for threat intelligence providers.
    """
    provider: str
    status: str  # "operational", "degraded", "offline", "mock_mode"
    reachability: bool
    avg_response_time_ms: float
    consecutive_failures: int
    last_successful_request: Optional[str] = None
    rate_limit_status: str = "OK"


class ThreatHistoryRecord(BaseModel):
    """
    Historical threat tracking model for incident correlation and timeline analysis.
    """
    indicator: str
    indicator_type: str
    first_seen: str
    last_seen: str
    lookup_count: int = 1
    last_risk_score: int
    last_confidence_score: int
