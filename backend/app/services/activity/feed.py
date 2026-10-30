"""
System-wide Activity Timeline Logger.
"""

from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.dashboard import ActivityItem, ActivityCategory


class ActivityFeedManager:
    """
    Logs and retrieves real-time system activity events.
    """

    def __init__(self):
        self._activities: List[ActivityItem] = []
        self._populate_initial_activities()

    def _populate_initial_activities(self):
        now = datetime.now(timezone.utc).isoformat()
        self.log_activity(
            category="Threat Intelligence Completed",
            title="System Telemetry Engine Ready",
            details="Registered 5 specialized threat intelligence provider plugins",
            severity="info",
            actor="System Core",
        )

    def log_activity(
        self,
        category: ActivityCategory,
        title: str,
        details: str,
        severity: str = "info",
        actor: str = "System",
    ) -> ActivityItem:
        act_id = f"ACT-{len(self._activities) + 101}"
        now = datetime.now(timezone.utc).isoformat()
        item = ActivityItem(
            activity_id=act_id,
            timestamp=now,
            category=category,
            title=title,
            details=details,
            severity=severity,
            actor=actor,
        )
        self._activities.append(item)
        return item

    def get_recent_activities(self, limit: int = 20, since: Optional[str] = None) -> List[ActivityItem]:
        results = self._activities
        if since and since.strip():
            results = [x for x in results if x.timestamp > since]
        return sorted(results, key=lambda x: x.timestamp, reverse=True)[:limit]


activity_feed_manager = ActivityFeedManager()
