"""
Pydantic Schemas & Data Models for the AI Investigation Engine.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from app.schemas.email import EmailAnalyzeResponse

VerdictType = Literal["Safe", "Suspicious", "Phishing", "Critical", "Insufficient Evidence"]


class MITRETechnique(BaseModel):
    """
    MITRE ATT&CK technique mapping.
    """
    id: str  # e.g., "T1566.002"
    name: str  # e.g., "Spearphishing Link"
    tactic: str  # e.g., "Initial Access"
    description: str


class ExecutiveReport(BaseModel):
    """
    Executive-level summary report for CISOs and non-technical stakeholders.
    """
    title: str
    verdict: VerdictType
    summary: str
    key_takeaway: str
    business_impact: str
    recommended_action: str


class TechnicalReport(BaseModel):
    """
    Technical SOC incident report for Tier-2/Tier-3 security analysts.
    """
    incident_id: str
    timestamp: str
    threat_type: str
    affected_assets: List[str]
    attack_chain: List[str]
    mitre_techniques: List[MITRETechnique]
    iocs_identified: List[Dict[str, str]]
    remediation_steps: List[str]


class InvestigationRequest(BaseModel):
    """
    Request model for AI Investigation analysis.
    Optionally accepts email_evidence or raw_mime / text_body.
    """
    email_evidence: Optional[EmailAnalyzeResponse] = Field(None, description="Pre-analyzed Email Evidence payload")
    raw_mime: Optional[str] = Field(None, description="Raw RFC822 .eml string to investigate")
    text_body: Optional[str] = Field(None, description="Plain text email body")
    url: Optional[str] = Field(None, description="Target URL string to investigate")


class InvestigationResponse(BaseModel):
    """
    Unified AI Investigation Engine output payload.
    """
    verdict: VerdictType
    confidence_score: int = Field(ge=0, le=100)
    risk_score: int = Field(ge=0, le=100)
    explanation: str
    evidence_summary: List[str] = Field(default_factory=list)
    attack_techniques: List[str] = Field(default_factory=list)
    mitre_mappings: List[MITRETechnique] = Field(default_factory=list)
    affected_assets: List[str] = Field(default_factory=list)
    business_impact: str
    recommended_actions: List[str] = Field(default_factory=list)
    executive_report: ExecutiveReport
    technical_report: TechnicalReport
    raw_evidence: Optional[Dict[str, Any]] = None
    execution_time_ms: float = 0.0
