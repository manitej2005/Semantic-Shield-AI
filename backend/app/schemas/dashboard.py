"""
Pydantic Schemas & Data Models for Enterprise SOC Dashboard Integration.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from app.schemas.incident import IncidentModel, SOCAnalytics
from app.schemas.report import ReportModel
from app.services.threat_intelligence.models import ProviderHealthStatus

ActivityCategory = Literal[
    "Email Uploaded",
    "Threat Intelligence Started",
    "Threat Intelligence Completed",
    "AI Investigation Started",
    "AI Investigation Completed",
    "Incident Created",
    "Incident Updated",
    "Report Generated",
    "Provider Status Changed",
    "Offensive Simulation Executed",
    "Page Scan Completed",
]

NotificationLevel = Literal["Critical", "Warning", "Information", "Success"]


class ActivityItem(BaseModel):
    activity_id: str
    timestamp: str
    category: ActivityCategory
    title: str
    details: str
    severity: str = "info"
    actor: str = "System"


class NotificationItem(BaseModel):
    notification_id: str
    timestamp: str
    level: NotificationLevel
    source: str
    title: str
    message: str
    read: bool = False
    action_link: Optional[str] = None


class SubsystemHealth(BaseModel):
    name: str
    status: Literal["Healthy", "Warning", "Critical", "Offline"]
    latency_ms: float = 0.0
    details: str = "Operational"


class SystemHealthSummary(BaseModel):
    status: str = "ok"
    ai: Literal["connected", "fallback"] = "connected"
    overall_status: Literal["Healthy", "Warning", "Critical", "Offline"]
    subsystems: List[SubsystemHealth]
    providers: List[ProviderHealthStatus]
    last_check: str


class SOCDashboardSummary(BaseModel):
    total_emails_analyzed: int
    total_threats_blocked: int
    active_incidents_count: int
    critical_alerts_count: int
    detection_accuracy_percentage: float
    average_investigation_time_seconds: float


class DashboardFullPayload(BaseModel):
    summary: SOCDashboardSummary
    health: SystemHealthSummary
    analytics: SOCAnalytics
    activity_feed: List[ActivityItem]
    notifications: List[NotificationItem]
    recent_incidents: List[IncidentModel]
    recent_reports: List[ReportModel]
    provider_health: List[ProviderHealthStatus]
