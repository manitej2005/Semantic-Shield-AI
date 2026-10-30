"""
Integration test suite for Enterprise Incident Management & Reporting Platform (Milestone 2 - Module 5).
"""

import sys
import asyncio
import json
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai_investigation.agent import ai_investigation_agent
from app.services.incident_management.manager import incident_manager
from app.services.incident_management.analytics import AnalyticsEngine
from app.services.reporting.engine import report_engine
from app.services.reporting.exporters import exporter_engine


SAMPLE_RAW_EML = """From: "Microsoft Security Team" <attacker@phishing-gateway-host.com>
To: victim@enterprise-corp.com
Reply-To: harvest-receiver@malicious-domain-fake.net
Subject: URGENT: Microsoft 365 Password Reset & Account Suspension Warning
Date: Tue, 04 Aug 2026 09:15:00 +0000
Content-Type: text/html; charset="utf-8"

<html>
  <body>
    <h2>Microsoft 365 Security Alert</h2>
    <p>Your password expires in 15 minutes. Click below to confirm direct deposit:</p>
    <a href="http://login-secure-payroll-verify.com/auth/harvest">Verify Account Now</a>
  </body>
</html>
"""


async def run_tests():
    print("==================================================", flush=True)
    print("[TEST] SEMANTIC SHIELD AI - INCIDENT MANAGEMENT & REPORTING TESTS", flush=True)
    print("==================================================", flush=True)

    # 1. Trigger AI Investigation (Triggers Auto-Incident Creation)
    print(f"\n[1] Triggering AI Investigation on Phishing Email...", flush=True)
    inv_res = await ai_investigation_agent.investigate_email(raw_mime=SAMPLE_RAW_EML)
    print(f"  -> Verdict: {inv_res.verdict} | Risk: {inv_res.risk_score}/100", flush=True)

    # 2. Verify Incident Auto-Creation in Repository
    print(f"\n[2] Verifying Incident Auto-Creation...", flush=True)
    incidents = await incident_manager.list_incidents()
    print(f"  -> Total Managed Incidents in Repository: {len(incidents)}", flush=True)
    assert len(incidents) >= 1, "Auto-incident creation failed!"
    
    inc = incidents[0]
    print(f"  -> Incident ID: {inc.incident_id}", flush=True)
    print(f"  -> Title: '{inc.title}'", flush=True)
    print(f"  -> Severity: {inc.severity} | Priority: {inc.priority} | Status: {inc.status}", flush=True)
    print(f"  -> Initial Timeline Events Count: {len(inc.timeline)}", flush=True)
    assert inc.severity in ["High", "Critical"], "Incident severity mapping failed!"
    assert inc.status == "New", "Initial incident status failed!"

    # 3. Assign Security Analyst
    print(f"\n[3] Assigning Analyst 'Alex Rivera (Tier-2 Analyst)'...", flush=True)
    assigned_inc = await incident_manager.assign_analyst(inc.incident_id, "Alex Rivera")
    assert assigned_inc is not None
    print(f"  -> Updated Status: {assigned_inc.status} | Assigned To: {assigned_inc.assigned_analyst}", flush=True)
    assert assigned_inc.status == "Investigating", "Analyst assignment status transition failed!"

    # 4. Add Analyst Note & Custom Audit Event
    print(f"\n[4] Adding Analyst Note & Custom Audit Event...", flush=True)
    await incident_manager.add_note(inc.incident_id, "Alex Rivera", "Verified credential harvesting URL. Initiating domain block across perimeter firewall.")
    await incident_manager.add_timeline_event(inc.incident_id, "Containment Applied", "Domain blocked at egress proxy", actor="Alex Rivera")
    
    updated_inc = await incident_manager.get_incident(inc.incident_id)
    assert updated_inc is not None
    print(f"  -> Notes Count: {len(updated_inc.notes)} | Notes Content: '{updated_inc.notes[0].content}'", flush=True)
    print(f"  -> Timeline Events Count: {len(updated_inc.timeline)}", flush=True)

    # 5. Resolve Incident
    print(f"\n[5] Updating Incident Status to 'Resolved'...", flush=True)
    resolved_inc = await incident_manager.update_status(inc.incident_id, "Resolved", resolution_notes="Firewall rules deployed. Targeted inbox purged.")
    assert resolved_inc is not None
    print(f"  -> Final Status: {resolved_inc.status} | Resolution Notes: '{resolved_inc.resolution_notes}'", flush=True)

    # 6. Test Search & Filtering
    print(f"\n[6] Testing Search & Filtering APIs...", flush=True)
    filtered = await incident_manager.list_incidents(severity=inc.severity, min_risk_score=70)
    print(f"  -> Filtered Incidents Count: {len(filtered)}", flush=True)
    assert len(filtered) >= 1, "Incident search & filtering failed!"

    # 7. Generate Reports & Test Exporters (JSON, Markdown, CSV, STIX 2.1)
    print(f"\n[7] Generating Security Reports & Testing Exporters...", flush=True)
    report = report_engine.generate_report(resolved_inc, report_type="Technical")
    print(f"  -> Report Generated: '{report.report_id}' | Title: '{report.title}'", flush=True)

    md_export = exporter_engine.export(resolved_inc, report, "markdown")
    csv_export = exporter_engine.export(resolved_inc, report, "csv")
    stix_export = exporter_engine.export(resolved_inc, report, "stix")

    print(f"  -> Markdown Export Length: {len(md_export)} chars", flush=True)
    print(f"  -> CSV Export Line Count: {len(csv_export.splitlines())} lines", flush=True)
    print(f"  -> STIX 2.1 Export valid JSON: {'type' in json.loads(stix_export)}", flush=True)
    
    assert "STIX" in stix_export or "bundle" in stix_export, "STIX 2.1 export failed!"

    # 8. Test SOC Operational Analytics
    print(f"\n[8] Testing Real-time SOC Operational Analytics...", flush=True)
    analytics = await AnalyticsEngine.compute_analytics()
    print(f"  -> Total Incidents: {analytics.total_incidents}", flush=True)
    print(f"  -> Severity Distribution: {analytics.severity_distribution}", flush=True)
    print(f"  -> Status Distribution: {analytics.status_distribution}", flush=True)
    print(f"  -> Top Threat IoCs: {analytics.top_threat_iocs}", flush=True)
    assert analytics.total_incidents >= 1, "SOC analytics computation failed!"

    print("\n==================================================", flush=True)
    print("[SUCCESS] ALL INCIDENT MANAGEMENT & REPORTING TESTS PASSED!", flush=True)
    print("==================================================", flush=True)


if __name__ == "__main__":
    asyncio.run(run_tests())
