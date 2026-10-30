"""
Centralized Notification Manager for Security Alerts.
"""

from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.dashboard import NotificationItem, NotificationLevel


class NotificationManager:
    """
    Manages real-time notification queue for SOC analysts.
    """

    def __init__(self):
        self._notifications: List[NotificationItem] = []
        self._populate_initial_notifications()

    def _populate_initial_notifications(self):
        self.add_notification(
            level="Information",
            source="Threat Intelligence Engine",
            title="Providers Operational",
            message="VirusTotal, WHOIS, RDAP, AbuseIPDB, and URLScan plugins loaded successfully.",
        )

    def add_notification(
        self,
        level: NotificationLevel,
        source: str,
        title: str,
        message: str,
        action_link: Optional[str] = None,
    ) -> NotificationItem:
        notif_id = f"NOTIF-{len(self._notifications) + 1001}"
        now = datetime.now(timezone.utc).isoformat()
        item = NotificationItem(
            notification_id=notif_id,
            timestamp=now,
            level=level,
            source=source,
            title=title,
            message=message,
            read=False,
            action_link=action_link,
        )
        self._notifications.append(item)
        return item

    def get_notifications(self, limit: int = 20, unread_only: bool = False) -> List[NotificationItem]:
        items = self._notifications
        if unread_only:
            items = [n for n in items if not n.read]
        return sorted(items, key=lambda x: x.timestamp, reverse=True)[:limit]


notification_manager = NotificationManager()
