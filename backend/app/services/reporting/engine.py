"""
Reporting Engine generating Executive, Technical, SOC Investigation, and IoC Reports.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.schemas.report import ReportModel, ReportType
from app.schemas.incident import IncidentModel


class ReportEngine:
    """
    Generates multi-perspective security reports from incident telemetry.
    """

    @classmethod
    def generate_report(
        cls, incident: IncidentModel, report_type: ReportType = "Technical"
    ) -> ReportModel:
        rep_id = f"REP-{incident.incident_id}-{report_type[:4].upper()}"
        now = datetime.now(timezone.utc).isoformat()

        if report_type == "Executive":
            title = f"Executive Threat Assessment: {incident.incident_id}"
            summary = (
                f"Executive Summary for Incident {incident.incident_id}.\n"
                f"Severity: {incident.severity.upper()} | Risk Score: {incident.risk_score}/100.\n"
                f"Business Impact: {incident.business_impact}"
            )
            sections = {
                "Executive Summary": incident.executive_summary,
                "Business Risk": incident.business_impact,
                "Key Findings": incident.ai_summary,
                "Primary Action": incident.containment_recommendations[0] if incident.containment_recommendations else "Quarantine user inbox.",
            }
        elif report_type == "SOC_Investigation":
            title = f"SOC Investigation Master Record: {incident.incident_id}"
            summary = f"Full SOC Investigation Record for Incident {incident.incident_id} (Status: {incident.status})."
            sections = {
                "Incident Overview": f"Assigned Analyst: {incident.assigned_analyst or 'Unassigned'}",
                "Attack Chain": incident.technical_summary,
                "MITRE ATT&CK": incident.mitre_mappings,
                "Timeline": [f"[{t.timestamp}] {t.event_type}: {t.description}" for t in incident.timeline],
                "Analyst Notes": [f"[{n.timestamp}] {n.analyst}: {n.content}" for n in incident.notes],
            }
        else:  # Technical / IoC / Threat Intel
            title = f"Technical Threat Analysis & IoC Record: {incident.incident_id}"
            summary = f"Technical SOC Report detailing threat IoCs, MITRE tactics, and remediation steps."
            sections = {
                "Technical Summary": incident.technical_summary,
                "Identified IoCs": incident.iocs_identified,
                "MITRE Mappings": incident.mitre_mappings,
                "Remediation Steps": incident.remediation_recommendations,
            }

        return ReportModel(
            report_id=rep_id,
            incident_id=incident.incident_id,
            report_type=report_type,
            title=title,
            generated_at=now,
            author="SemanticShield AI Reporting Engine",
            summary=summary,
            sections=sections,
            iocs=incident.iocs_identified,
        )


report_engine = ReportEngine()
