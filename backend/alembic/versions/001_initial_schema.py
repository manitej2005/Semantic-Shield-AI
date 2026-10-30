"""Initial schema creation for incidents, activity_feed, threat_reports, notifications, and simulations.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-28 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create incidents table
    op.create_table(
        'incidents',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('incident_id', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('threat_type', sa.String(length=128), nullable=False),
        sa.Column('severity', sa.String(length=32), nullable=False),
        sa.Column('priority', sa.String(length=16), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='New'),
        sa.Column('source', sa.String(length=128), nullable=False),
        sa.Column('target', sa.Text(), nullable=False),
        sa.Column('detection_timestamp', sa.String(length=64), nullable=False),
        sa.Column('investigation_timestamp', sa.String(length=64), nullable=True),
        sa.Column('reporter', sa.String(length=128), nullable=True),
        sa.Column('assigned_analyst', sa.String(length=128), nullable=True),
        sa.Column('risk_score', sa.Integer(), server_default='0'),
        sa.Column('confidence_score', sa.Integer(), server_default='0'),
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('technical_summary', sa.Text(), nullable=True),
        sa.Column('executive_summary', sa.Text(), nullable=True),
        sa.Column('mitre_mappings', sa.Text(), nullable=True),
        sa.Column('iocs_identified', sa.Text(), nullable=True),
        sa.Column('threat_intel_results', sa.Text(), nullable=True),
        sa.Column('affected_assets', sa.Text(), nullable=True),
        sa.Column('business_impact', sa.Text(), nullable=True),
        sa.Column('containment_recommendations', sa.Text(), nullable=True),
        sa.Column('remediation_recommendations', sa.Text(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('timeline', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('audit_history', sa.Text(), nullable=True),
        sa.Column('is_simulation', sa.Boolean(), server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('incident_id')
    )
    op.create_index(op.f('ix_incidents_incident_id'), 'incidents', ['incident_id'], unique=True)
    op.create_index(op.f('ix_incidents_is_simulation'), 'incidents', ['is_simulation'], unique=False)

    # 2. Create activity_feed table
    op.create_table(
        'activity_feed',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('activity_id', sa.String(length=64), nullable=False),
        sa.Column('timestamp', sa.String(length=64), nullable=False),
        sa.Column('category', sa.String(length=128), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('details', sa.Text(), nullable=False),
        sa.Column('severity', sa.String(length=32), server_default='info'),
        sa.Column('actor', sa.String(length=128), server_default='System'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('activity_id')
    )
    op.create_index(op.f('ix_activity_feed_activity_id'), 'activity_feed', ['activity_id'], unique=True)

    # 3. Create threat_reports table
    op.create_table(
        'threat_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('report_id', sa.String(length=64), nullable=False),
        sa.Column('timestamp', sa.String(length=64), nullable=False),
        sa.Column('target_url', sa.Text(), nullable=False),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('risk_level', sa.String(length=32), nullable=True),
        sa.Column('threat_categories', sa.Text(), nullable=True),
        sa.Column('reasons', sa.Text(), nullable=True),
        sa.Column('agent_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('report_id')
    )
    op.create_index(op.f('ix_threat_reports_report_id'), 'threat_reports', ['report_id'], unique=True)

    # 4. Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('notification_id', sa.String(length=64), nullable=False),
        sa.Column('timestamp', sa.String(length=64), nullable=False),
        sa.Column('level', sa.String(length=32), nullable=False),
        sa.Column('source', sa.String(length=128), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('read', sa.Boolean(), server_default='0'),
        sa.Column('action_link', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('notification_id')
    )
    op.create_index(op.f('ix_notifications_notification_id'), 'notifications', ['notification_id'], unique=True)

    # 5. Create simulations table
    op.create_table(
        'simulations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('simulation_id', sa.String(length=64), nullable=False),
        sa.Column('timestamp', sa.String(length=64), nullable=False),
        sa.Column('scenario_type', sa.String(length=128), nullable=False),
        sa.Column('employee_role', sa.String(length=128), nullable=False),
        sa.Column('behavior_profile', sa.String(length=128), nullable=False),
        sa.Column('email_subject', sa.Text(), nullable=False),
        sa.Column('email_body', sa.Text(), nullable=False),
        sa.Column('agent_reasoning', sa.Text(), nullable=False),
        sa.Column('agent_decision', sa.String(length=32), nullable=False),
        sa.Column('threat_category', sa.String(length=128), nullable=True),
        sa.Column('threat_severity', sa.String(length=32), nullable=True),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('is_simulation', sa.Boolean(), server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('simulation_id')
    )
    op.create_index(op.f('ix_simulations_simulation_id'), 'simulations', ['simulation_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_simulations_simulation_id'), table_name='simulations')
    op.drop_table('simulations')
    op.drop_index(op.f('ix_notifications_notification_id'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_threat_reports_report_id'), table_name='threat_reports')
    op.drop_table('threat_reports')
    op.drop_index(op.f('ix_activity_feed_activity_id'), table_name='activity_feed')
    op.drop_table('activity_feed')
    op.drop_index(op.f('ix_incidents_is_simulation'), table_name='incidents')
    op.drop_index(op.f('ix_incidents_incident_id'), table_name='incidents')
    op.drop_table('incidents')
