"""
Pydantic Schemas & Data Models for Email and URL Intelligence Agents.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.services.threat_intelligence.models import ThreatAnalyzeResponse


class URLHeuristicsResult(BaseModel):
    """
    Heuristic metrics and risk indicators for an individual URL.
    """
    url: str
    length: int
    hostname: str
    is_ip_address: bool = False
    is_shortener: bool = False
    subdomain_count: int = 0
    entropy_score: float = 0.0
    has_credential_keywords: bool = False
    has_homoglyphs: bool = False
    is_https: bool = True
    non_standard_port: Optional[int] = None
    typosquatting_detected: bool = False
    suspicious_flags: List[str] = Field(default_factory=list)
    heuristic_risk_score: int = Field(ge=0, le=100, default=0)


class URLEvidence(BaseModel):
    """
    Unified intelligence model for an extracted URL.
    """
    original_url: str
    normalized_url: str
    expanded_url: Optional[str] = None
    protocol: str = "http"
    hostname: str = ""
    domain: str = ""
    subdomains: List[str] = Field(default_factory=list)
    path: str = ""
    query_params: Dict[str, str] = Field(default_factory=dict)
    heuristics: URLHeuristicsResult
    threat_intel: Optional[ThreatAnalyzeResponse] = None


class EmailAuthResult(BaseModel):
    """
    SPF, DKIM, and DMARC authentication verification results.
    """
    spf_status: str = "None"  # Pass, Fail, SoftFail, Neutral, None
    dkim_status: str = "None"
    dmarc_status: str = "None"
    details: Dict[str, str] = Field(default_factory=dict)
    auth_passed: bool = True


class EmailHeaderEvidence(BaseModel):
    """
    Extracted email header telemetry.
    """
    subject: str = ""
    date: Optional[str] = None
    message_id: Optional[str] = None
    from_header: str = ""
    from_address: str = ""
    display_name: str = ""
    sender_address: Optional[str] = None
    to_addresses: List[str] = Field(default_factory=list)
    cc_addresses: List[str] = Field(default_factory=list)
    reply_to: Optional[str] = None
    return_path: Optional[str] = None
    received_chain: List[str] = Field(default_factory=list)
    x_headers: Dict[str, str] = Field(default_factory=dict)
    user_agent: Optional[str] = None
    mailer: Optional[str] = None
    priority: Optional[str] = None


class AttachmentMetadata(BaseModel):
    """
    Metadata for extracted email attachments.
    """
    filename: str
    extension: str
    mime_type: str
    size_bytes: int
    md5: str
    sha256: str
    has_macros: bool = False
    is_suspicious_extension: bool = False
    is_password_protected: bool = False
    embedded_urls: List[str] = Field(default_factory=list)


class EmailHeuristicsResult(BaseModel):
    """
    Email-specific social engineering and spoofing heuristic findings.
    """
    display_name_spoofing: bool = False
    reply_to_mismatch: bool = False
    return_path_mismatch: bool = False
    unicode_spoofing: bool = False
    brand_impersonation: Optional[str] = None  # Microsoft, Google, Bank, HR, etc.
    urgency_detected: bool = False
    financial_request_detected: bool = False
    credential_request_detected: bool = False
    invoice_theme_detected: bool = False
    mfa_reset_theme_detected: bool = False
    heuristics_risk_score: int = Field(ge=0, le=100, default=0)
    findings: List[str] = Field(default_factory=list)


class EmailAnalyzeRequest(BaseModel):
    """
    JSON request model for raw MIME or email text analysis.
    """
    raw_mime: Optional[str] = Field(None, description="Raw RFC822 .eml string")
    text_body: Optional[str] = Field(None, description="Plain text email body")
    html_body: Optional[str] = Field(None, description="HTML email body")
    subject: Optional[str] = Field(None, description="Email subject line")
    from_address: Optional[str] = Field(None, description="Sender email address")


class EmailAnalyzeResponse(BaseModel):
    """
    Unified comprehensive evidence response returned by Email Intelligence Agent.
    """
    headers: EmailHeaderEvidence
    authentication: EmailAuthResult
    heuristics: EmailHeuristicsResult
    urls: List[URLEvidence] = Field(default_factory=list)
    qr_codes_detected: int = 0
    attachments: List[AttachmentMetadata] = Field(default_factory=list)
    unified_iocs: List[Dict[str, str]] = Field(default_factory=list)
    overall_risk_score: int = Field(ge=0, le=100, default=0)
    overall_confidence: int = Field(ge=0, le=100, default=0)
    ai_context_payload: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0
