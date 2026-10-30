"""
Integration test suite for combined Email Intelligence Agent (Module 2) and URL Intelligence Agent (Module 3).
"""

import sys
import asyncio
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.url_intelligence.agent import url_intelligence_agent
from app.services.email_intelligence.agent import email_intelligence_agent
from app.services.threat_intelligence.manager import threat_intel_manager


# Sample raw RFC822 MIME phishing email payload
SAMPLE_RAW_EML = """From: "Microsoft Security Team" <attacker@phishing-gateway-host.com>
To: victim@enterprise-corp.com
Reply-To: harvest-receiver@malicious-domain-fake.net
Return-Path: <bounce@attacker-host.com>
Subject: URGENT: Microsoft 365 Password Reset & Account Suspension Warning
Date: Tue, 04 Aug 2026 09:15:00 +0000
Message-ID: <phish-9048-alert@phishing-gateway-host.com>
Authentication-Results: spf=fail (sender IP 185.220.101.5); dkim=fail; dmarc=fail
Content-Type: multipart/alternative; boundary="boundary-1234"

--boundary-1234
Content-Type: text/plain; charset="utf-8"

CRITICAL SECURITY ALERT: Your Microsoft 365 password expires in 15 minutes.
Please verify your credentials immediately at:
http://login-secure-payroll-verify.com/auth/harvest

Otherwise your account direct deposit will be suspended.
--boundary-1234
Content-Type: text/html; charset="utf-8"

<html>
  <body>
    <h2>Microsoft 365 Security Alert</h2>
    <p>Your password expires in 15 minutes. Click below to confirm direct deposit:</p>
    <a href="http://login-secure-payroll-verify.com/auth/harvest">Verify Account Now</a>
    <br/>
    <p>Alternative QR Login:</p>
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" alt="QR Code"/>
    <span style="font-size:0px">quishing: https://qr-benefits-update-portal.org/login</span>
  </body>
</html>
--boundary-1234--
"""


async def run_tests():
    print("==================================================", flush=True)
    print("[TEST] SEMANTIC SHIELD AI - EMAIL & URL INTELLIGENCE AGENTS", flush=True)
    print("==================================================", flush=True)

    # 1. Test URL Intelligence Agent
    test_url = "http://login-secure-payroll-verify.com/auth/harvest"
    print(f"\n[1] Testing URL Intelligence Agent: '{test_url}'", flush=True)
    url_ev = await url_intelligence_agent.analyze_url(test_url)
    
    print(f"  -> Protocol: {url_ev.protocol} | Hostname: {url_ev.hostname}", flush=True)
    print(f"  -> Entropy Score: {url_ev.heuristics.entropy_score}", flush=True)
    print(f"  -> Credential Keywords: {url_ev.heuristics.has_credential_keywords}", flush=True)
    print(f"  -> Typosquatting Flag: {url_ev.heuristics.typosquatting_detected}", flush=True)
    print(f"  -> Heuristic Risk Score: {url_ev.heuristics.heuristic_risk_score}/100", flush=True)
    assert url_ev.heuristics.heuristic_risk_score >= 50, "URL Heuristic scoring failed!"
    assert url_ev.threat_intel is not None, "Threat Intel integration failed!"
    print(f"  -> Threat Intel Composite Score: {url_ev.threat_intel.risk_score}/100", flush=True)

    # 2. Test Email Intelligence Agent
    print(f"\n[2] Testing Email Intelligence Agent (.eml MIME analysis)...", flush=True)
    email_res = await email_intelligence_agent.analyze_email(raw_mime=SAMPLE_RAW_EML)
    
    print(f"  -> Subject: {email_res.headers.subject}", flush=True)
    print(f"  -> From: {email_res.headers.from_address} (Display Name: '{email_res.headers.display_name}')", flush=True)
    print(f"  -> SPF: {email_res.authentication.spf_status} | DKIM: {email_res.authentication.dkim_status} | DMARC: {email_res.authentication.dmarc_status}", flush=True)
    print(f"  -> Display Name Spoofing: {email_res.heuristics.display_name_spoofing}", flush=True)
    print(f"  -> Reply-To Mismatch: {email_res.heuristics.reply_to_mismatch}", flush=True)
    print(f"  -> Brand Impersonation: {email_res.heuristics.brand_impersonation}", flush=True)
    print(f"  -> Extracted URLs Count: {len(email_res.urls)}", flush=True)
    print(f"  -> QR Codes Detected: {email_res.qr_codes_detected}", flush=True)
    print(f"  -> Unified IoCs Count: {len(email_res.unified_iocs)}", flush=True)
    print(f"  -> Overall Risk Score: {email_res.overall_risk_score}/100", flush=True)
    print(f"  -> Overall Confidence: {email_res.overall_confidence}/100", flush=True)

    assert email_res.heuristics.display_name_spoofing is True, "Display name spoofing failed!"
    assert email_res.heuristics.reply_to_mismatch is True, "Reply-to mismatch failed!"
    assert email_res.overall_risk_score >= 70, "Overall email risk score threshold failed!"

    # 3. Test Threat Intelligence Engine (Module 1) compatibility check
    print(f"\n[3] Testing Module 1 Threat Intel Engine Compatibility...", flush=True)
    ti_res = await threat_intel_manager.analyze_indicator("185.220.101.5", force_type="ipv4")
    print(f"  -> IP Analysis Risk Score: {ti_res.risk_score}/100 ({ti_res.reputation})", flush=True)
    assert ti_res.risk_score >= 70, "Module 1 Threat Intel compatibility failed!"

    print("\n==================================================", flush=True)
    print("[SUCCESS] ALL EMAIL & URL INTELLIGENCE AGENT TESTS PASSED!", flush=True)
    print("==================================================", flush=True)


if __name__ == "__main__":
    asyncio.run(run_tests())
