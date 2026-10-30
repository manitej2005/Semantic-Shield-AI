"""
Integration test suite for Enterprise SOC Integration Layer (Milestone 2 - Module 6).
"""

import sys
import asyncio
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.dashboard.aggregator import dashboard_aggregator
from app.services.dashboard.statistics import StatisticsEngine
from app.services.activity.feed import activity_feed_manager
from app.services.notifications.manager import notification_manager
from app.services.health.monitor import system_health_monitor
from app.services.websocket.manager import websocket_manager
from app.services.ai_investigation.agent import ai_investigation_agent


SAMPLE_RAW_EML = """From: "Microsoft Security Team" <attacker@phishing-gateway-host.com>
To: victim@enterprise-corp.com
Subject: URGENT: Account Suspension Notice
Date: Tue, 04 Aug 2026 09:15:00 +0000
Content-Type: text/html; charset="utf-8"

<html>
  <body>
    <a href="http://login-secure-payroll-verify.com/auth/harvest">Verify Account Now</a>
  </body>
</html>
"""


async def run_tests():
    print("==================================================", flush=True)
    print("[TEST] SEMANTIC SHIELD AI - ENTERPRISE SOC INTEGRATION LAYER", flush=True)
    print("==================================================", flush=True)

    # 1. Test Activity Feed Logger & Notification Manager
    print(f"\n[1] Testing Activity Feed Logger & Notification Queue...", flush=True)
    activity_feed_manager.log_activity(
        category="Email Uploaded",
        title="Email Payload Uploaded",
        details="Inbound phishing sample uploaded by security analyst",
        actor="Security Analyst",
    )
    notification_manager.add_notification(
        level="Warning",
        source="Email Intelligence Agent",
        title="Suspicious Email Detected",
        message="Display name spoofing identified for external email",
    )

    activities = activity_feed_manager.get_recent_activities()
    notifications = notification_manager.get_notifications()
    print(f"  -> Activity Timeline Count: {len(activities)} (Latest: '{activities[0].title}')", flush=True)
    print(f"  -> Notifications Count: {len(notifications)} (Latest: '{notifications[0].title}')", flush=True)
    assert len(activities) >= 1, "Activity feed logging failed!"
    assert len(notifications) >= 1, "Notification manager failed!"

    # 2. Trigger AI Investigation & Auto-Incident Generation
    print(f"\n[2] Triggering End-to-End Investigation Pipeline...", flush=True)
    await ai_investigation_agent.investigate_email(raw_mime=SAMPLE_RAW_EML)

    # 3. Test Unified System Health Monitor
    print(f"\n[3] Testing Unified System Health Monitor...", flush=True)
    health = await system_health_monitor.get_system_health()
    print(f"  -> Overall System Status: {health.overall_status}", flush=True)
    print(f"  -> Monitored Subsystems Count: {len(health.subsystems)}", flush=True)
    print(f"  -> Monitored Providers Count: {len(health.providers)}", flush=True)
    assert health.overall_status in ["Healthy", "Warning"], "System health monitor evaluation failed!"

    # 4. Test Master SOC Dashboard Aggregator
    print(f"\n[4] Testing Master SOC Dashboard Aggregator (React Frontend Payload)...", flush=True)
    payload = await dashboard_aggregator.get_full_dashboard()
    print(f"  -> Total Emails Analyzed: {payload.summary.total_emails_analyzed}", flush=True)
    print(f"  -> Total Threats Blocked: {payload.summary.total_threats_blocked}", flush=True)
    print(f"  -> Active Incidents Count: {payload.summary.active_incidents_count}", flush=True)
    print(f"  -> Critical Alerts Count: {payload.summary.critical_alerts_count}", flush=True)
    print(f"  -> Detection Accuracy: {payload.summary.detection_accuracy_percentage}%", flush=True)
    print(f"  -> Recent Incidents Count: {len(payload.recent_incidents)}", flush=True)
    print(f"  -> Provider Health Cards Count: {len(payload.provider_health)}", flush=True)

    assert payload.summary.total_emails_analyzed >= 1, "Dashboard summary calculation failed!"
    assert len(payload.recent_incidents) >= 1, "Dashboard recent incidents payload failed!"

    # 5. Test WebSocket Broadcaster
    print(f"\n[5] Testing Async WebSocket Broadcaster...", flush=True)
    await websocket_manager.broadcast_event("incident_created", {"incident_id": "INC-2026-1001"}, channel="dashboard")
    print("  -> Broadcast executed cleanly without errors", flush=True)

    print("\n==================================================", flush=True)
    print("[SUCCESS] ALL ENTERPRISE SOC INTEGRATION LAYER TESTS PASSED!", flush=True)
    print("==================================================", flush=True)


if __name__ == "__main__":
    asyncio.run(run_tests())
