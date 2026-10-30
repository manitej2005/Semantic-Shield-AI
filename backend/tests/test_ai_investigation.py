"""
Integration test suite for AI Investigation Engine (Milestone 2 - Module 4).
"""

import sys
import asyncio
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai_investigation.agent import ai_investigation_agent
from app.services.email_intelligence.agent import email_intelligence_agent
from app.services.threat_intelligence.manager import threat_intel_manager


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
    print("[TEST] SEMANTIC SHIELD AI - AI INVESTIGATION ENGINE TESTS", flush=True)
    print("==================================================", flush=True)

    # 1. Test AI Investigation on Raw EML Phishing Email
    print(f"\n[1] Testing AI Investigation Agent on Raw Phishing Email...", flush=True)
    inv_res = await ai_investigation_agent.investigate_email(raw_mime=SAMPLE_RAW_EML)

    print(f"  -> Final Verdict: {inv_res.verdict}", flush=True)
    print(f"  -> Confidence Score: {inv_res.confidence_score}/100", flush=True)
    print(f"  -> Composite Risk Score: {inv_res.risk_score}/100", flush=True)
    print(f"  -> Explanation Summary:\n{inv_res.explanation}", flush=True)
    print(f"  -> Key Supporting Findings ({len(inv_res.evidence_summary)}):", flush=True)
    for k in inv_res.evidence_summary:
        print(f"     * {k}", flush=True)

    print(f"  -> MITRE ATT&CK Mappings ({len(inv_res.mitre_mappings)}):", flush=True)
    for m in inv_res.mitre_mappings:
        print(f"     * [{m.id}] {m.name} ({m.tactic}): {m.description}", flush=True)

    print(f"  -> Executive Report Title: '{inv_res.executive_report.title}'", flush=True)
    print(f"  -> Technical Incident ID: '{inv_res.technical_report.incident_id}'", flush=True)

    assert inv_res.verdict in ["Phishing", "Critical"], "AI Investigation verdict failed expected phishing status!"
    assert inv_res.confidence_score >= 80, "Confidence score threshold failed!"
    assert len(inv_res.mitre_mappings) >= 1, "MITRE ATT&CK mapping failed!"

    # 2. Test Anti-Hallucination Guard (Insufficient Evidence)
    print(f"\n[2] Testing Anti-Hallucination Guard (Insufficient Evidence)...", flush=True)
    empty_res = await ai_investigation_agent.investigate_email(raw_mime="", text_body="")
    print(f"  -> Empty Evidence Verdict: {empty_res.verdict}", flush=True)
    print(f"  -> Explanation: {empty_res.explanation}", flush=True)
    assert empty_res.verdict == "Insufficient Evidence", "Anti-hallucination guard failed!"

    # 3. Test Module 1 & Module 2 compatibility check
    print(f"\n[3] Testing Previous Modules Compatibility...", flush=True)
    ti_res = await threat_intel_manager.analyze_indicator("185.220.101.5", force_type="ipv4")
    print(f"  -> Threat Intel Risk Score: {ti_res.risk_score}/100 ({ti_res.reputation})", flush=True)
    assert ti_res.risk_score >= 70, "Threat Intel engine failed!"

    print("\n==================================================", flush=True)
    print("[SUCCESS] ALL AI INVESTIGATION ENGINE TESTS PASSED!", flush=True)
    print("==================================================", flush=True)


if __name__ == "__main__":
    asyncio.run(run_tests())
