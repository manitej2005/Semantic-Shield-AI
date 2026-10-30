"""
Pydantic Schemas for Reporting Engine and Multi-Format Exports (JSON, Markdown, CSV, STIX 2.1).
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

ReportType = Literal["Executive", "Technical", "SOC_Investigation", "IoC_Report", "Threat_Intel_Report"]
ExportFormat = Literal["json", "markdown", "csv", "stix"]


class ReportModel(BaseModel):
    """
    Generated SOC Report data model.
    """
    report_id: str
    incident_id: str
    report_type: ReportType
    title: str
    generated_at: str
    author: str = "SemanticShield AI Reporting Engine"
    summary: str
    sections: Dict[str, Any]
    iocs: List[Dict[str, str]] = Field(default_factory=list)


class ExportRequest(BaseModel):
    """
    Request model to export a report or incident.
    """
    incident_id: str
    report_type: ReportType = "Technical"
    export_format: ExportFormat = "json"


class STIX21Object(BaseModel):
    type: str
    spec_version: str = "2.1"
    id: str
    created: str
    modified: str
    name: Optional[str] = None
    pattern: Optional[str] = None
    pattern_type: Optional[str] = None
    labels: List[str] = Field(default_factory=list)


class STIX21Package(BaseModel):
    type: str = "bundle"
    id: str
    objects: List[Dict[str, Any]] = Field(default_factory=list)
