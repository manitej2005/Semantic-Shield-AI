"""
Request Pydantic schemas for SemanticShield AI.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """
    Primary payload received from client applications (Chrome Extension / API).
    Preserves exact field names for zero-downtime backward compatibility.
    """
    url: str = Field(..., description="Target webpage or link URL to analyze")
    page_text: str = Field(..., description="Scraped visible innerText or raw email content")
    scan_id: Optional[str] = Field(default=None, description="Client-generated unique scan UUID")
    timestamp: Optional[str] = Field(default=None, description="Client ISO 8601 generation timestamp")
    dedup_key: Optional[str] = Field(default=None, description="Deduplication key for guaranteed delivery")


class AgentRequestPayload(BaseModel):
    """
    Standardized payload distributed to individual specialized agents.
    """
    url: str = Field(..., description="Target URL being evaluated")
    content_text: str = Field(..., description="Extracted content text")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description="HTTP/Email headers if available")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Contextual flags and source info")
