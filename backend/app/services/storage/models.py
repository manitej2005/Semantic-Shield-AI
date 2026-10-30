"""
SQLAlchemy ORM Models for SemanticShield AI Persistence.
Maps database tables to relational ORM entities.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    DateTime,
    func
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DBIncident(Base):
    """
    Incident Record entity stored in the 'incidents' database table.
    """
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    threat_type = Column(String(128), nullable=False)
    severity = Column(String(32), nullable=False)
    priority = Column(String(16), nullable=False)
    status = Column(String(32), nullable=False, default="New")
    source = Column(String(128), nullable=False)
    target = Column(Text, nullable=False)
    detection_timestamp = Column(String(64), nullable=False)
    investigation_timestamp = Column(String(64), nullable=True)
    reporter = Column(String(128), nullable=True)
    assigned_analyst = Column(String(128), nullable=True)
    risk_score = Column(Integer, default=0)
    confidence_score = Column(Integer, default=0)
    ai_summary = Column(Text, nullable=True)
    technical_summary = Column(Text, nullable=True)
    executive_summary = Column(Text, nullable=True)
    mitre_mappings = Column(Text, nullable=True)  # JSON serialized list
    iocs_identified = Column(Text, nullable=True)  # JSON serialized list
    threat_intel_results = Column(Text, nullable=True)  # JSON serialized dict
    affected_assets = Column(Text, nullable=True)  # JSON serialized list
    business_impact = Column(Text, nullable=True)
    containment_recommendations = Column(Text, nullable=True)  # JSON serialized list
    remediation_recommendations = Column(Text, nullable=True)  # JSON serialized list
    resolution_notes = Column(Text, nullable=True)
    timeline = Column(Text, nullable=True)  # JSON serialized list
    notes = Column(Text, nullable=True)  # JSON serialized list
    audit_history = Column(Text, nullable=True)  # JSON serialized list
    is_simulation = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class DBActivityItem(Base):
    """
    Activity Timeline entity stored in the 'activity_feed' database table.
    """
    __tablename__ = "activity_feed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(String(64), unique=True, nullable=False, index=True)
    timestamp = Column(String(64), nullable=False)
    category = Column(String(128), nullable=False)
    title = Column(String(255), nullable=False)
    details = Column(Text, nullable=False)
    severity = Column(String(32), default="info")
    actor = Column(String(128), default="System")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DBThreatReport(Base):
    """
    Threat Scan Report entity stored in the 'threat_reports' database table.
    """
    __tablename__ = "threat_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(String(64), unique=True, nullable=False, index=True)
    timestamp = Column(String(64), nullable=False)
    target_url = Column(Text, nullable=False)
    risk_score = Column(Integer, nullable=True)
    risk_level = Column(String(32), nullable=True)
    threat_categories = Column(Text, nullable=True)  # JSON serialized list
    reasons = Column(Text, nullable=True)  # JSON serialized list
    agent_summary = Column(Text, nullable=True)  # JSON serialized dict
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DBNotificationItem(Base):
    """
    System Notification entity stored in the 'notifications' database table.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    notification_id = Column(String(64), unique=True, nullable=False, index=True)
    timestamp = Column(String(64), nullable=False)
    level = Column(String(32), nullable=False)
    source = Column(String(128), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    action_link = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DBSimulation(Base):
    """
    Phishing Simulation record stored in the 'simulations' database table.
    """
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(String(64), unique=True, nullable=False, index=True)
    timestamp = Column(String(64), nullable=False)
    scenario_type = Column(String(128), nullable=False)
    employee_role = Column(String(128), nullable=False)
    behavior_profile = Column(String(128), nullable=False)
    email_subject = Column(Text, nullable=False)
    email_body = Column(Text, nullable=False)
    agent_reasoning = Column(Text, nullable=False)
    agent_decision = Column(String(32), nullable=False)
    threat_category = Column(String(128), nullable=True)
    threat_severity = Column(String(32), nullable=True)
    confidence_score = Column(Integer, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    is_simulation = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
