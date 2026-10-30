"""
Database Initialization & Startup Loader for SemanticShield AI.
Handles automatic schema migration, in-memory singleton loading, and dual-write repository hooks.
"""

import os
import logging
from typing import Dict, Any
from alembic.config import Config
from alembic import command

from app.core.config import settings
from app.services.storage.db import init_db, engine
from app.services.storage.repository import (
    incident_repository,
    activity_repository,
    threat_report_repository,
    notification_repository,
    simulation_repository,
)
from app.services.incident_management.manager import incident_manager
from app.services.activity.feed import activity_feed_manager
from app.services.notifications.manager import notification_manager

logger = logging.getLogger("app.services.storage.init")


def run_migrations() -> None:
    """
    Executes Alembic database migrations programmatically on application startup.
    """
    try:
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        alembic_ini_path = os.path.join(backend_dir, "alembic.ini")

        if os.path.exists(alembic_ini_path):
            logger.info("[Database Init] Running Alembic migrations to head...")
            alembic_cfg = Config(alembic_ini_path)
            alembic_cfg.set_main_option("script_location", os.path.join(backend_dir, "alembic"))
            alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
            command.upgrade(alembic_cfg, "head")
            logger.info("[Database Init] Alembic migrations completed successfully.")
        else:
            logger.warning(f"[Database Init] alembic.ini not found at {alembic_ini_path}. Falling back to Base.metadata.create_all().")
            init_db()
    except Exception as exc:
        logger.warning(f"[Database Init] Alembic migration warning: {exc}. Initializing tables directly.")
        init_db()


def load_from_db_to_memory() -> None:
    """
    Loads persisted database records into in-memory singletons for zero-latency operations.
    """
    try:
        incidents = incident_repository.load_all_incidents()
        for inc in incidents:
            incident_manager._incidents[inc.incident_id] = inc
        logger.info(f"[Database Init] Restored {len(incidents)} incidents into IncidentManager.")

        activities = activity_repository.load_all_activities(limit=500)
        if activities:
            # Append non-duplicate activities
            existing_ids = {a.activity_id for a in activity_feed_manager._activities}
            for act in reversed(activities):
                if act.activity_id not in existing_ids:
                    activity_feed_manager._activities.append(act)
        logger.info(f"[Database Init] Restored {len(activities)} activities into ActivityFeedManager.")

        notifications = notification_repository.load_all_notifications()
        if notifications:
            existing_notif_ids = {n.notification_id for n in notification_manager._notifications}
            for notif in reversed(notifications):
                if notif.notification_id not in existing_notif_ids:
                    notification_manager._notifications.append(notif)
        logger.info(f"[Database Init] Restored {len(notifications)} notifications into NotificationManager.")

    except Exception as exc:
        logger.error(f"[Database Init] Error loading persisted data into memory: {exc}", exc_info=True)


def setup_dual_write_hooks() -> None:
    """
    Attaches dual-write listeners to in-memory singletons so all runtime mutations persist to database automatically.
    """
    # 1. Hook IncidentManager
    orig_create_scan = incident_manager.create_from_scan
    async def hooked_create_from_scan(*args, **kwargs):
        inc = await orig_create_scan(*args, **kwargs)
        if inc:
            incident_repository.save_incident(inc)
        return inc
    incident_manager.create_from_scan = hooked_create_from_scan

    orig_create_inv = incident_manager.create_from_investigation
    async def hooked_create_from_investigation(*args, **kwargs):
        inc = await orig_create_inv(*args, **kwargs)
        if inc:
            incident_repository.save_incident(inc)
        return inc
    incident_manager.create_from_investigation = hooked_create_from_investigation

    if hasattr(incident_manager, "update_status"):
        orig_update_status = incident_manager.update_status
        def hooked_update_status(*args, **kwargs):
            inc = orig_update_status(*args, **kwargs)
            if inc:
                incident_repository.save_incident(inc)
            return inc
        incident_manager.update_status = hooked_update_status

    # 2. Hook ActivityFeedManager
    orig_log_act = activity_feed_manager.log_activity
    def hooked_log_activity(*args, **kwargs):
        act = orig_log_act(*args, **kwargs)
        if act:
            activity_repository.save_activity(act)
        return act
    activity_feed_manager.log_activity = hooked_log_activity

    # 3. Hook NotificationManager if method exists
    if hasattr(notification_manager, "add_notification"):
        orig_add_notif = notification_manager.add_notification
        def hooked_add_notification(*args, **kwargs):
            notif = orig_add_notif(*args, **kwargs)
            if notif:
                notification_repository.save_notification(notif)
            return notif
        notification_manager.add_notification = hooked_add_notification

    logger.info("[Database Init] Dual-write hooks successfully attached to in-memory singletons.")


def init_database() -> None:
    """
    Master startup initialization procedure called on FastAPI app startup.
    """
    logger.info("[Database Init] Starting SemanticShield AI database initialization sequence...")
    
    # Step 1: Ensure tables exist / run migrations
    if settings.DATABASE_AUTO_MIGRATE:
        run_migrations()
    else:
        init_db()

    # Step 2: Restore DB records into memory
    load_from_db_to_memory()

    # Step 3: Setup dual-write background hooks
    setup_dual_write_hooks()

    logger.info("[Database Init] Database initialization & setup complete.")


def persist_to_db() -> None:
    """
    Shutdown handler ensuring all in-memory singletons are flushed to database.
    """
    logger.info("[Database Shutdown] Flushing in-memory state to persistent database...")
    try:
        for inc in incident_manager.get_all():
            incident_repository.save_incident(inc)
        for act in activity_feed_manager.get_recent_activities(limit=500):
            activity_repository.save_activity(act)
        logger.info("[Database Shutdown] State sync flush complete.")
    except Exception as exc:
        logger.error(f"[Database Shutdown] Error flushing state to database: {exc}", exc_info=True)


def get_db_stats() -> Dict[str, Any]:
    """
    Returns database summary stats for admin endpoints.
    """
    try:
        return {
            "total_incidents": len(incident_repository.load_all_incidents()),
            "total_activities": len(activity_repository.load_all_activities(limit=1000)),
            "total_simulations": len(simulation_repository.load_all_simulations()),
            "database_url": settings.DATABASE_URL.split("@")[-1],
        }
    except Exception:
        return {"status": "error"}
