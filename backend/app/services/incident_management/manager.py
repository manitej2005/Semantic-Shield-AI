"""
Incident Lifecycle Repository & Storage Manager.
Handles auto-incident creation from AI investigation verdicts, status workflows, analyst assignment, and search/filtering.
"""

import time
import asyncio
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone
from app.schemas.incident import (
    IncidentModel,
    IncidentStatus,
    IncidentSeverity,
    IncidentPriority,
    TimelineEvent,
    AnalystNote,
)
from app.schemas.investigation import InvestigationResponse
from app.services.incident_management.timeline import TimelineGenerator

logger = logging.getLogger(__name__)


class IncidentManager:
    """
    Central repository for enterprise SOC incident storage and management.
    """

    def __init__(self):
        self._incidents: Dict[str, IncidentModel] = {}

    def _generate_incident_id(self) -> str:
        seq = len(self._incidents) + 1001
        year = datetime.now(timezone.utc).year
        return f"INC-{year}-{seq}"

    async def create_from_investigation(
        self, inv: InvestigationResponse, target: str = "Corporate User Inbox"
    ) -> Optional[IncidentModel]:
        """
        Auto-creates an incident if AI investigation verdict is Suspicious, Phishing, or Critical.
        """
        if inv.verdict not in ["Suspicious", "Phishing", "Critical"]:
            return None

        inc_id = self._generate_incident_id()
        now = datetime.now(timezone.utc).isoformat()

        # Map Severity from Verdict & Risk Score
        if inv.verdict == "Critical" or inv.risk_score >= 85:
            severity: IncidentSeverity = "Critical"
            priority: IncidentPriority = "P1"
        elif inv.verdict == "Phishing" or inv.risk_score >= 70:
            severity = "High"
            priority = "P2"
        else:
            severity = "Medium"
            priority = "P3"

        timeline = TimelineGenerator.initial_investigation_timeline()
        mitre_list = [{"id": m.id, "name": m.name, "tactic": m.tactic} for m in inv.mitre_mappings]

        inc = IncidentModel(
            incident_id=inc_id,
            title=f"{inv.verdict.upper()} Threat: {inv.executive_report.title}",
            threat_type=inv.technical_report.threat_type or "Spear-Phishing Credential Harvest",
            severity=severity,
            priority=priority,
            status="New",
            source="Email Intelligence & AI Agent Pipeline",
            target=target,
            detection_timestamp=now,
            investigation_timestamp=now,
            reporter="Automated AI Guard",
            assigned_analyst=None,
            risk_score=inv.risk_score,
            confidence_score=inv.confidence_score,
            ai_summary=inv.explanation,
            technical_summary=inv.executive_report.summary,
            executive_summary=inv.executive_report.summary,
            mitre_mappings=mitre_list,
            iocs_identified=inv.technical_report.iocs_identified,
            affected_assets=inv.affected_assets,
            business_impact=inv.business_impact,
            containment_recommendations=inv.recommended_actions,
            remediation_recommendations=inv.recommended_actions,
            resolution_notes=None,
            timeline=timeline,
            notes=[],
            audit_history=[f"Incident auto-created with ID {inc_id} at {now}"],
        )

        self._incidents[inc_id] = inc
        return inc

    async def create_from_scan(
        self,
        url: str,
        risk_score: int,
        classification: str,
        reasons: List[str],
        source: str = "Chrome Extension Guard",
        is_simulation: bool = False
    ) -> Optional[IncidentModel]:
        """
        Auto-creates an incident from an extension scan or simulation if risk_score >= 40 or classification is High Risk/Suspicious.
        """
        if risk_score < 40 and classification not in ["High Risk", "Suspicious", "Critical", "Phishing"]:
            return None

        inc_id = self._generate_incident_id()
        now = datetime.now(timezone.utc).isoformat()

        if classification == "Critical" or risk_score >= 85:
            severity: IncidentSeverity = "Critical"
            priority: IncidentPriority = "P1"
        elif classification in ["High Risk", "Phishing"] or risk_score >= 70:
            severity = "High"
            priority = "P2"
        else:
            severity = "Medium"
            priority = "P3"

        # Idempotency Check: Prevent duplicate incidents for identical target URL
        for existing in self._incidents.values():
            if existing.target == url and existing.severity == severity and not is_simulation:
                logger.info(f"[IncidentManager] Idempotent deduplication: Incident {existing.incident_id} already exists for {url}")
                return existing

        tag = " [SIMULATION]" if is_simulation else ""
        title = f"{classification.upper()} Threat: {url}{tag}"
        summary_text = reasons[0] if reasons else f"Identified {classification} threat vector."

        inc = IncidentModel(
            incident_id=inc_id,
            title=title,
            threat_type="Web Phishing / Credential Harvest",
            severity=severity,
            priority=priority,
            status="New",
            source=source,
            target=url,
            detection_timestamp=now,
            investigation_timestamp=now,
            reporter="SemanticShield AI Guard",
            assigned_analyst=None,
            risk_score=risk_score,
            confidence_score=90,
            ai_summary=summary_text,
            technical_summary=f"URL: {url} | Reasons: {', '.join(reasons)}",
            executive_summary=summary_text,
            mitre_mappings=[{"id": "T1566.002", "name": "Spearphishing Link", "tactic": "Initial Access"}],
            iocs_identified=[{"type": "url", "value": url}],
            affected_assets=[url],
            business_impact="Potential credential harvesting or user impersonation",
            containment_recommendations=["Block URL at DNS gateway", "Isolate user session"],
            remediation_recommendations=["Revoke compromised tokens"],
            resolution_notes=None,
            timeline=[TimelineGenerator.create_event("Detection", f"Threat detected on {url}", actor=source)],
            notes=[],
            audit_history=[f"Incident auto-created with ID {inc_id} at {now}"],
        )

        self._incidents[inc_id] = inc
        return inc

    async def get_incident(self, incident_id: str) -> Optional[IncidentModel]:
        return self._incidents.get(incident_id)

    async def list_incidents(
        self,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        threat_type: Optional[str] = None,
        assigned_analyst: Optional[str] = None,
        min_risk_score: Optional[int] = None,
        query: Optional[str] = None,
    ) -> List[IncidentModel]:
        results = list(self._incidents.values())

        if severity:
            results = [i for i in results if i.severity.lower() == severity.lower()]
        if status:
            results = [i for i in results if i.status.lower() == status.lower()]
        if threat_type:
            results = [i for i in results if threat_type.lower() in i.threat_type.lower()]
        if assigned_analyst:
            results = [i for i in results if i.assigned_analyst and i.assigned_analyst.lower() == assigned_analyst.lower()]
        if min_risk_score is not None:
            results = [i for i in results if i.risk_score >= min_risk_score]
        if query:
            q_low = query.lower()
            results = [i for i in results if q_low in i.title.lower() or q_low in i.incident_id.lower() or q_low in i.ai_summary.lower()]

        # Sort newest first
        results.sort(key=lambda x: x.detection_timestamp, reverse=True)
        return results

    async def update_status(
        self, incident_id: str, new_status: IncidentStatus, resolution_notes: Optional[str] = None
    ) -> Optional[IncidentModel]:
        inc = self._incidents.get(incident_id)
        if not inc:
            return None

        old_status = inc.status
        inc.status = new_status
        now = datetime.now(timezone.utc).isoformat()

        if resolution_notes:
            inc.resolution_notes = resolution_notes

        event_desc = f"Status updated from '{old_status}' to '{new_status}'"
        inc.timeline.append(TimelineGenerator.create_event("Status Changed", event_desc, actor="Analyst"))
        inc.audit_history.append(f"{event_desc} at {now}")
        return inc

    async def assign_analyst(self, incident_id: str, analyst_name: str) -> Optional[IncidentModel]:
        inc = self._incidents.get(incident_id)
        if not inc:
            return None

        inc.assigned_analyst = analyst_name
        if inc.status == "New":
            inc.status = "Investigating"

        now = datetime.now(timezone.utc).isoformat()
        event_desc = f"Incident assigned to analyst '{analyst_name}'"
        inc.timeline.append(TimelineGenerator.create_event("Analyst Assigned", event_desc, actor=analyst_name))
        inc.audit_history.append(f"{event_desc} at {now}")
        return inc

    async def add_note(self, incident_id: str, analyst: str, content: str) -> Optional[IncidentModel]:
        inc = self._incidents.get(incident_id)
        if not inc:
            return None

        now = datetime.now(timezone.utc).isoformat()
        note_id = f"NOTE-{len(inc.notes) + 1}"
        note = AnalystNote(note_id=note_id, timestamp=now, analyst=analyst, content=content)
        inc.notes.append(note)

        inc.timeline.append(TimelineGenerator.create_event("Analyst Note Added", f"Note added by {analyst}", actor=analyst))
        inc.audit_history.append(f"Note '{note_id}' added by {analyst} at {now}")
        return inc

    async def add_timeline_event(
        self, incident_id: str, event_type: str, description: str, actor: str = "Analyst"
    ) -> Optional[IncidentModel]:
        inc = self._incidents.get(incident_id)
        if not inc:
            return None

        event = TimelineGenerator.create_event(event_type, description, actor)
        inc.timeline.append(event)
        return inc

    async def delete_incident(self, incident_id: str) -> bool:
        if incident_id in self._incidents:
            del self._incidents[incident_id]
            return True
        return False


incident_manager = IncidentManager()
