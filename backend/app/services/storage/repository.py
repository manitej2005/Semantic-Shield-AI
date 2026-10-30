"""
Data Access Object (DAO) repositories for persistent storage in SemanticShield AI.
Handles SQL database operations and JSON serialization for complex fields.
"""

import json
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.services.storage.db import SessionLocal
from app.services.storage.models import (
    DBIncident,
    DBActivityItem,
    DBThreatReport,
    DBNotificationItem,
    DBSimulation,
)
from app.schemas.incident import IncidentModel, TimelineEvent, AnalystNote
from app.schemas.dashboard import ActivityItem, NotificationItem
from app.domain.entities.threat_report import ThreatReport
from app.schemas.phishing_simulation import PhishingSimulationResponse

logger = logging.getLogger("app.services.storage.repository")


class IncidentRepository:
    """
    Persistence DAO for enterprise security incidents.
    """

    def save_incident(self, incident: IncidentModel) -> IncidentModel:
        """
        Persists or updates an incident record in the database.
        """
        db: Session = SessionLocal()
        try:
            timeline_json = json.dumps([t.dict() for t in incident.timeline])
            notes_json = json.dumps([n.dict() for n in incident.notes])
            mitre_json = json.dumps(incident.mitre_mappings or [])
            iocs_json = json.dumps(incident.iocs_identified or [])
            intel_json = json.dumps(incident.threat_intel_results) if incident.threat_intel_results else None
            assets_json = json.dumps(incident.affected_assets or [])
            containment_json = json.dumps(incident.containment_recommendations or [])
            remediation_json = json.dumps(incident.remediation_recommendations or [])
            audit_json = json.dumps(incident.audit_history or [])

            # Check if incident is simulation based on title/source or flag
            is_sim = "[SIMULATION]" in incident.title or "Simulation" in incident.source

            db_obj = db.query(DBIncident).filter(DBIncident.incident_id == incident.incident_id).first()

            if db_obj:
                db_obj.title = incident.title
                db_obj.threat_type = incident.threat_type
                db_obj.severity = incident.severity
                db_obj.priority = incident.priority
                db_obj.status = incident.status
                db_obj.source = incident.source
                db_obj.target = incident.target
                db_obj.detection_timestamp = incident.detection_timestamp
                db_obj.investigation_timestamp = incident.investigation_timestamp
                db_obj.reporter = incident.reporter
                db_obj.assigned_analyst = incident.assigned_analyst
                db_obj.risk_score = incident.risk_score
                db_obj.confidence_score = incident.confidence_score
                db_obj.ai_summary = incident.ai_summary
                db_obj.technical_summary = incident.technical_summary
                db_obj.executive_summary = incident.executive_summary
                db_obj.mitre_mappings = mitre_json
                db_obj.iocs_identified = iocs_json
                db_obj.threat_intel_results = intel_json
                db_obj.affected_assets = assets_json
                db_obj.business_impact = incident.business_impact
                db_obj.containment_recommendations = containment_json
                db_obj.remediation_recommendations = remediation_json
                db_obj.resolution_notes = incident.resolution_notes
                db_obj.timeline = timeline_json
                db_obj.notes = notes_json
                db_obj.audit_history = audit_json
                db_obj.is_simulation = is_sim
            else:
                db_obj = DBIncident(
                    incident_id=incident.incident_id,
                    title=incident.title,
                    threat_type=incident.threat_type,
                    severity=incident.severity,
                    priority=incident.priority,
                    status=incident.status,
                    source=incident.source,
                    target=incident.target,
                    detection_timestamp=incident.detection_timestamp,
                    investigation_timestamp=incident.investigation_timestamp,
                    reporter=incident.reporter,
                    assigned_analyst=incident.assigned_analyst,
                    risk_score=incident.risk_score,
                    confidence_score=incident.confidence_score,
                    ai_summary=incident.ai_summary,
                    technical_summary=incident.technical_summary,
                    executive_summary=incident.executive_summary,
                    mitre_mappings=mitre_json,
                    iocs_identified=iocs_json,
                    threat_intel_results=intel_json,
                    affected_assets=assets_json,
                    business_impact=incident.business_impact,
                    containment_recommendations=containment_json,
                    remediation_recommendations=remediation_json,
                    resolution_notes=incident.resolution_notes,
                    timeline=timeline_json,
                    notes=notes_json,
                    audit_history=audit_json,
                    is_simulation=is_sim,
                )
                db.add(db_obj)

            db.commit()
            logger.debug(f"[IncidentRepository] Saved incident '{incident.incident_id}' to DB.")
            return incident
        except Exception as e:
            db.rollback()
            logger.error(f"[IncidentRepository] Error saving incident '{incident.incident_id}': {e}", exc_info=True)
            return incident
        finally:
            db.close()

    def load_all_incidents(self) -> List[IncidentModel]:
        """
        Loads all persisted incidents from database into Pydantic models.
        """
        db: Session = SessionLocal()
        results = []
        try:
            records = db.query(DBIncident).order_by(desc(DBIncident.id)).all()
            for r in records:
                timeline_raw = json.loads(r.timeline) if r.timeline else []
                notes_raw = json.loads(r.notes) if r.notes else []
                timeline = [TimelineEvent(**t) for t in timeline_raw]
                notes = [AnalystNote(**n) for n in notes_raw]

                inc = IncidentModel(
                    incident_id=r.incident_id,
                    title=r.title,
                    threat_type=r.threat_type,
                    severity=r.severity,
                    priority=r.priority,
                    status=r.status,
                    source=r.source,
                    target=r.target,
                    detection_timestamp=r.detection_timestamp,
                    investigation_timestamp=r.investigation_timestamp,
                    reporter=r.reporter,
                    assigned_analyst=r.assigned_analyst,
                    risk_score=r.risk_score,
                    confidence_score=r.confidence_score,
                    ai_summary=r.ai_summary or "",
                    technical_summary=r.technical_summary or "",
                    executive_summary=r.executive_summary or "",
                    mitre_mappings=json.loads(r.mitre_mappings) if r.mitre_mappings else [],
                    iocs_identified=json.loads(r.iocs_identified) if r.iocs_identified else [],
                    threat_intel_results=json.loads(r.threat_intel_results) if r.threat_intel_results else None,
                    affected_assets=json.loads(r.affected_assets) if r.affected_assets else [],
                    business_impact=r.business_impact or "",
                    containment_recommendations=json.loads(r.containment_recommendations) if r.containment_recommendations else [],
                    remediation_recommendations=json.loads(r.remediation_recommendations) if r.remediation_recommendations else [],
                    resolution_notes=r.resolution_notes,
                    timeline=timeline,
                    notes=notes,
                    audit_history=json.loads(r.audit_history) if r.audit_history else [],
                )
                results.append(inc)
            logger.info(f"[IncidentRepository] Loaded {len(results)} incidents from DB.")
            return results
        except Exception as e:
            logger.error(f"[IncidentRepository] Error loading incidents: {e}", exc_info=True)
            return []
        finally:
            db.close()

    def delete_incident(self, incident_id: str) -> bool:
        """
        Deletes an incident record by ID.
        """
        db: Session = SessionLocal()
        try:
            db_obj = db.query(DBIncident).filter(DBIncident.incident_id == incident_id).first()
            if db_obj:
                db.delete(db_obj)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"[IncidentRepository] Error deleting incident '{incident_id}': {e}", exc_info=True)
            return False
        finally:
            db.close()


class ActivityRepository:
    """
    Persistence DAO for system activity log feed.
    """

    def save_activity(self, activity: ActivityItem) -> ActivityItem:
        db: Session = SessionLocal()
        try:
            db_obj = db.query(DBActivityItem).filter(DBActivityItem.activity_id == activity.activity_id).first()
            if not db_obj:
                db_obj = DBActivityItem(
                    activity_id=activity.activity_id,
                    timestamp=activity.timestamp,
                    category=activity.category,
                    title=activity.title,
                    details=activity.details,
                    severity=activity.severity,
                    actor=activity.actor,
                )
                db.add(db_obj)
                db.commit()
            return activity
        except Exception as e:
            db.rollback()
            logger.error(f"[ActivityRepository] Error saving activity: {e}", exc_info=True)
            return activity
        finally:
            db.close()

    def load_all_activities(self, limit: int = 100) -> List[ActivityItem]:
        db: Session = SessionLocal()
        try:
            records = db.query(DBActivityItem).order_by(desc(DBActivityItem.id)).limit(limit).all()
            results = [
                ActivityItem(
                    activity_id=r.activity_id,
                    timestamp=r.timestamp,
                    category=r.category,
                    title=r.title,
                    details=r.details,
                    severity=r.severity,
                    actor=r.actor,
                )
                for r in records
            ]
            return results
        except Exception as e:
            logger.error(f"[ActivityRepository] Error loading activities: {e}", exc_info=True)
            return []
        finally:
            db.close()


class ThreatReportRepository:
    """
    Persistence DAO for threat scan reports.
    """

    def save_report(self, report: ThreatReport) -> ThreatReport:
        db: Session = SessionLocal()
        try:
            categories_json = json.dumps(report.threat_categories or [])
            reasons_json = json.dumps(report.reasons or [])
            summary_json = json.dumps(report.agent_summary) if report.agent_summary else None

            db_obj = DBThreatReport(
                report_id=report.report_id,
                timestamp=report.timestamp,
                target_url=report.target_url,
                risk_score=report.risk_score,
                risk_level=report.risk_level,
                threat_categories=categories_json,
                reasons=reasons_json,
                agent_summary=summary_json,
            )
            db.add(db_obj)
            db.commit()
            return report
        except Exception as e:
            db.rollback()
            logger.error(f"[ThreatReportRepository] Error saving report: {e}", exc_info=True)
            return report
        finally:
            db.close()

    def load_all_reports(self) -> List[ThreatReport]:
        db: Session = SessionLocal()
        try:
            records = db.query(DBThreatReport).order_by(desc(DBThreatReport.id)).all()
            results = [
                ThreatReport(
                    report_id=r.report_id,
                    timestamp=r.timestamp,
                    target_url=r.target_url,
                    risk_score=r.risk_score,
                    risk_level=r.risk_level,
                    threat_categories=json.loads(r.threat_categories) if r.threat_categories else [],
                    reasons=json.loads(r.reasons) if r.reasons else [],
                    agent_summary=json.loads(r.agent_summary) if r.agent_summary else {},
                )
                for r in records
            ]
            return results
        except Exception as e:
            logger.error(f"[ThreatReportRepository] Error loading reports: {e}", exc_info=True)
            return []
        finally:
            db.close()


class NotificationRepository:
    """
    Persistence DAO for system notifications.
    """

    def save_notification(self, notif: NotificationItem) -> NotificationItem:
        db: Session = SessionLocal()
        try:
            db_obj = db.query(DBNotificationItem).filter(DBNotificationItem.notification_id == notif.notification_id).first()
            if not db_obj:
                db_obj = DBNotificationItem(
                    notification_id=notif.notification_id,
                    timestamp=notif.timestamp,
                    level=notif.level,
                    source=notif.source,
                    title=notif.title,
                    message=notif.message,
                    read=notif.read,
                    action_link=notif.action_link,
                )
                db.add(db_obj)
                db.commit()
            return notif
        except Exception as e:
            db.rollback()
            logger.error(f"[NotificationRepository] Error saving notification: {e}", exc_info=True)
            return notif
        finally:
            db.close()

    def load_all_notifications(self) -> List[NotificationItem]:
        db: Session = SessionLocal()
        try:
            records = db.query(DBNotificationItem).order_by(desc(DBNotificationItem.id)).all()
            return [
                NotificationItem(
                    notification_id=r.notification_id,
                    timestamp=r.timestamp,
                    level=r.level,
                    source=r.source,
                    title=r.title,
                    message=r.message,
                    read=r.read,
                    action_link=r.action_link,
                )
                for r in records
            ]
        except Exception as e:
            logger.error(f"[NotificationRepository] Error loading notifications: {e}", exc_info=True)
            return []
        finally:
            db.close()


class SimulationRepository:
    """
    Persistence DAO for phishing simulation runs.
    """

    def save_simulation(self, sim: PhishingSimulationResponse) -> PhishingSimulationResponse:
        db: Session = SessionLocal()
        try:
            db_obj = DBSimulation(
                simulation_id=sim.simulation_id,
                timestamp=sim.timestamp,
                scenario_type=sim.scenario_type,
                employee_role=sim.employee_role,
                behavior_profile=sim.behavior_profile,
                email_subject=sim.email_subject,
                email_body=sim.email_body,
                agent_reasoning=sim.agent_reasoning,
                agent_decision=sim.agent_decision,
                threat_category=sim.threat_category,
                threat_severity=sim.threat_severity,
                confidence_score=sim.confidence_score,
                duration_seconds=sim.duration_seconds,
                is_simulation=sim.is_simulation,
            )
            db.add(db_obj)
            db.commit()
            logger.debug(f"[SimulationRepository] Saved simulation run '{sim.simulation_id}' to DB.")
            return sim
        except Exception as e:
            db.rollback()
            logger.error(f"[SimulationRepository] Error saving simulation: {e}", exc_info=True)
            return sim
        finally:
            db.close()

    def load_all_simulations(self) -> List[PhishingSimulationResponse]:
        db: Session = SessionLocal()
        try:
            records = db.query(DBSimulation).order_by(desc(DBSimulation.id)).all()
            return [
                PhishingSimulationResponse(
                    simulation_id=r.simulation_id,
                    timestamp=r.timestamp,
                    scenario_type=r.scenario_type,
                    employee_role=r.employee_role,
                    behavior_profile=r.behavior_profile,
                    email_subject=r.email_subject,
                    email_body=r.email_body,
                    agent_reasoning=r.agent_reasoning,
                    agent_decision=r.agent_decision,
                    threat_category=r.threat_category or "phishing",
                    threat_severity=r.threat_severity or "SUSPICIOUS",
                    confidence_score=r.confidence_score or 80,
                    duration_seconds=r.duration_seconds or 0.0,
                    is_simulation=r.is_simulation,
                )
                for r in records
            ]
        except Exception as e:
            logger.error(f"[SimulationRepository] Error loading simulations: {e}", exc_info=True)
            return []
        finally:
            db.close()


# Instantiate Repository Singletons
incident_repository = IncidentRepository()
activity_repository = ActivityRepository()
threat_report_repository = ThreatReportRepository()
notification_repository = NotificationRepository()
simulation_repository = SimulationRepository()
