"""
Pydantic Schemas & Data Models for Enterprise Incident Management.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, Field

IncidentStatus = Literal["New", "Investigating", "Contained", "Mitigated", "Resolved", "Closed"]
IncidentSeverity = Literal["Critical", "High", "Medium", "Low", "Informational"]
IncidentPriority = Literal["P1", "P2", "P3", "P4", "P5"]


class TimelineEvent(BaseModel):
    """
    Audit timeline milestone event.
    """
    timestamp: str
    event_type: str
    description: str
    actor: str = "System"


class AnalystNote(BaseModel):
    """
    Analyst investigation note.
    """
    note_id: str
    timestamp: str
    analyst: str
    content: str


class IncidentModel(BaseModel):
    """
    Enterprise Security Incident data model.
    """
    incident_id: str
    title: str
    threat_type: str
    severity: IncidentSeverity
    priority: IncidentPriority
    status: IncidentStatus = "New"
    source: str = "Email Intelligence Pipeline"
    target: str = "Corporate Inbox"
    detection_timestamp: str
    investigation_timestamp: Optional[str] = None
    reporter: str = "Automated AI Guard"
    assigned_analyst: Optional[str] = None
    risk_score: int = Field(ge=0, le=100)
    confidence_score: int = Field(ge=0, le=100)
    ai_summary: str
    technical_summary: str
    executive_summary: str
    mitre_mappings: List[Dict[str, str]] = Field(default_factory=list)
    iocs_identified: List[Dict[str, str]] = Field(default_factory=list)
    threat_intel_results: Optional[Dict[str, Any]] = None
    affected_assets: List[str] = Field(default_factory=list)
    business_impact: str
    containment_recommendations: List[str] = Field(default_factory=list)
    remediation_recommendations: List[str] = Field(default_factory=list)
    resolution_notes: Optional[str] = None
    timeline: List[TimelineEvent] = Field(default_factory=list)
    notes: List[AnalystNote] = Field(default_factory=list)
    audit_history: List[str] = Field(default_factory=list)


class IncidentCreate(BaseModel):
    """
    Request payload to create an incident manually.
    """
    title: str
    threat_type: str = "Spear-Phishing Credential Harvest"
    severity: IncidentSeverity = "High"
    priority: IncidentPriority = "P2"
    target: str = "Corporate Inbox"
    risk_score: int = 80
    confidence_score: int = 90
    ai_summary: str
    technical_summary: str
    executive_summary: str
    iocs_identified: List[Dict[str, str]] = Field(default_factory=list)


class IncidentUpdate(BaseModel):
    """
    Request payload to update an incident.
    """
    status: Optional[IncidentStatus] = None
    severity: Optional[IncidentSeverity] = None
    priority: Optional[IncidentPriority] = None
    assigned_analyst: Optional[str] = None
    resolution_notes: Optional[str] = None


class AssignAnalystRequest(BaseModel):
    analyst_name: str


class AddNoteRequest(BaseModel):
    analyst_name: str
    content: str


class SOCAnalytics(BaseModel):
    total_incidents: int
    severity_distribution: Dict[str, int]
    status_distribution: Dict[str, int]
    threat_type_distribution: Dict[str, int]
    top_threat_iocs: List[Dict[str, Any]]
    average_resolution_time_minutes: float
