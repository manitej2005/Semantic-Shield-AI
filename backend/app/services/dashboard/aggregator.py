"""
Master SOC Dashboard Aggregator Service for React Admin Dashboard integration.
Aggregates summary stats, system health, analytics, activity feed, notifications, incidents, reports, and provider health.
"""

from app.schemas.dashboard import DashboardFullPayload
from app.services.dashboard.statistics import StatisticsEngine
from app.services.health.monitor import system_health_monitor
from app.services.incident_management.analytics import AnalyticsEngine
from app.services.incident_management.manager import incident_manager
from app.services.activity.feed import activity_feed_manager
from app.services.notifications.manager import notification_manager
from app.services.threat_intelligence.provider_health import health_monitor_instance


class DashboardAggregator:
    """
    Unified SOC platform aggregator service.
    """

    @classmethod
    async def get_full_dashboard(cls) -> DashboardFullPayload:
        summary = await StatisticsEngine.compute_summary()
        health = await system_health_monitor.get_system_health()
        analytics = await AnalyticsEngine.compute_analytics()
        activity = activity_feed_manager.get_recent_activities(limit=15)
        notifications = notification_manager.get_notifications(limit=10)
        recent_incidents = await incident_manager.list_incidents()
        provider_health = await health_monitor_instance.get_all_health()

        return DashboardFullPayload(
            summary=summary,
            health=health,
            analytics=analytics,
            activity_feed=activity,
            notifications=notifications,
            recent_incidents=recent_incidents[:10],
            recent_reports=[],
            provider_health=provider_health,
        )


dashboard_aggregator = DashboardAggregator()
