import os
import sys
import csv
import time
import json
import asyncio
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.abspath("backend"))

from app.services.phishing_simulation.engine import phishing_simulation_engine
from app.schemas.phishing_simulation import PhishingSimulationRequest

SCENARIOS = [
    {
        "id": "SIM-EML-001",
        "name": "Microsoft 365 Urgent Password Reset Scam",
        "default_role": "HR Manager",
        "subject": "URGENT: Microsoft 365 Password Reset & Account Suspension Warning",
        "body": "CRITICAL SECURITY ALERT: Your Microsoft 365 password expires in 15 minutes. Please verify your credentials immediately at: http://login-secure-payroll-verify.com/auth/harvest"
    },
    {
        "id": "SIM-EML-002",
        "name": "Urgent Executive Wire Transfer Re-Verification",
        "default_role": "Finance Manager",
        "subject": "URGENT & CONFIDENTIAL: Q3 Executive Wire Transfer Re-Verification Required",
        "body": "Team,\nWe need to urgently update vendor bank details for the $145,000 international wire before 2:00 PM today. Please re-verify corporate account authorization code at: http://secure-wire-transfer-portal.com/verify-banking\n\nDo not discuss this over standard Slack channels due to strict M&A audit protocols."
    },
    {
        "id": "SIM-EML-003",
        "name": "HR Payroll Direct Deposit Bonus Form (Quishing)",
        "default_role": "HR Specialist",
        "subject": "Action Required: Updated Direct Deposit Form & Bonus Distribution",
        "body": "Dear Employee,\nYour annual Q3 bonus distribution form has been updated. Scan the QR code below using your mobile device camera to verify your banking details:\n\n[Embedded Mobile QR Code Payload]\nTarget Link: https://qr-benefits-update-portal.org/login"
    },
    {
        "id": "SIM-EML-004",
        "name": "FedEx Express Package Hold & Customs Fee Warning",
        "default_role": "Logistics Coordinator",
        "subject": "Delivery Failed: Package #FX-99482 Held at Regional Hub",
        "body": "Notice: Your incoming package (#FX-99482) could not be delivered due to an outstanding $3.50 customs fee.\nPay fee and update delivery address within 24 hours:\nhttp://fedx-customs-payment-clearance.com/pay"
    },
    {
        "id": "SIM-EML-005",
        "name": "M365 Security Alert: Unrecognized Device Revocation",
        "default_role": "Systems Administrator",
        "subject": "Security Notice: Unrecognized Linux Login Detected (Moscow, RU)",
        "body": "We detected a successful login to your Microsoft 365 tenant from an unmanaged Linux device in Moscow, Russia (IP: 185.220.101.5).\nIf this was not you, revoke device credentials immediately:\nhttps://login-microsoft-security-auth.com/revoke-access"
    },
    {
        "id": "SIM-EML-006",
        "name": "Okta / Duo Push MFA Session Timeout Bypass",
        "default_role": "Senior Engineer",
        "subject": "MFA Security Policy Update: Re-authenticate Push Notification Token",
        "body": "Attention: Your Okta Verify push token session will expire in 30 minutes due to system maintenance.\nPlease complete MFA re-authentication at:\nhttps://okta-sso-corp-portal.com/mfa-verify\n\nInput both your primary password and current 6-digit Duo/Okta passcode when prompted."
    },
    {
        "id": "SIM-EML-007",
        "name": "Legitimate Team Weekly Standup Meeting",
        "default_role": "Software Developer",
        "subject": "Team Weekly Engineering Standup & Q3 Roadmap Update",
        "body": "Hi Team,\nReminder for our weekly standup meeting today at 10:00 AM.\nGoogle Meet Link: https://meet.google.com/abc-defg-hij\n\nAgenda:\n1. Phishing Simulation & Behavioral Analysis\n2. Q3 Engineering Progress"
    }
]

PROFILES = [
    {"profile": "trusting", "role": "HR Manager"},
    {"profile": "security_conscious", "role": "Senior Developer"},
    {"profile": "overwhelmed", "role": "Finance Manager"},
    {"profile": "executive", "role": "VP of Operations"}
]

os.makedirs("paper/data", exist_ok=True)

all_rows = []

# Load Repetition 1 from results_live.csv
with open("results_live.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        r["repetition"] = 1
        all_rows.append(r)

print(f"Loaded {len(all_rows)} rows for Repetition 1 from results_live.csv")

async def run_matrix(rep_number):
    print(f"\n--- STARTING REPETITION {rep_number} ---")
    run_counter = 1
    rep_rows = []
    
    for sc in SCENARIOS:
        for pr in PROFILES:
            run_id = f"REP{rep_number}_RUN_{run_counter:03d}"
            req = PhishingSimulationRequest(
                scenario=sc["name"],
                employee_role=pr["role"],
                behavior_profile=pr["profile"],
                email_subject=sc["subject"],
                email_body=sc["body"]
            )
            
            success = False
            attempts = 0
            while not success and attempts < 5:
                attempts += 1
                try:
                    print(f"[{run_id}] Executing {sc['id']} ({pr['profile']}) attempt {attempts}...", flush=True)
                    st = time.time()
                    sim_id, now_iso, system_prompt, user_msg, start_time, stream_gen = await phishing_simulation_engine.execute_simulation(req)
                    
                    full_chunks = []
                    async for chunk in stream_gen():
                        full_chunks.append(chunk)
                    full_text = "".join(full_chunks)
                    
                    res = await phishing_simulation_engine.finalize_simulation(
                        sim_id=sim_id,
                        now_iso=now_iso,
                        request=req,
                        full_reasoning_text=full_text,
                        start_time=st
                    )
                    dur = res.duration_seconds
                    
                    fallback_used = False
                    if "Scanning incoming email headers" in full_text or "Executing fallback streaming agent" in full_text:
                        fallback_used = True
                        
                    row = {
                        "run_id": run_id,
                        "scenario_id": sc["id"],
                        "scenario_name": sc["name"],
                        "behavior_profile": pr["profile"],
                        "decision": res.agent_decision,
                        "risk_score": res.risk_score,
                        "severity": res.threat_severity,
                        "confidence_pct": res.confidence_score,
                        "duration_seconds": dur,
                        "model_name": "gemini-3.5-flash",
                        "fallback_used": str(fallback_used),
                        "timestamp": res.timestamp,
                        "repetition": rep_number
                    }
                    rep_rows.append(row)
                    print(f" -> Result: [{res.agent_decision}] Risk: {res.risk_score}, Conf: {res.confidence_score}%, Dur: {dur}s, Fallback: {fallback_used}", flush=True)
                    success = True
                except Exception as e:
                    print(f" -> Error on attempt {attempts}: {e}", flush=True)
                    await asyncio.sleep(4.0)
            
            run_counter += 1
            await asyncio.sleep(2.0) # Rate limit spacing
            
    return rep_rows

async def main():
    rep2 = await run_matrix(2)
    all_rows.extend(rep2)
    
    rep3 = await run_matrix(3)
    all_rows.extend(rep3)
    
    # Write paper/data/results_all.csv
    fieldnames = [
        "run_id", "scenario_id", "scenario_name", "behavior_profile",
        "decision", "risk_score", "severity", "confidence_pct",
        "duration_seconds", "model_name", "fallback_used", "timestamp", "repetition"
    ]
    
    out_path = "paper/data/results_all.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
        
    print(f"\nSUCCESS! Total runs saved to {out_path}: {len(all_rows)}")

if __name__ == "__main__":
    asyncio.run(main())
