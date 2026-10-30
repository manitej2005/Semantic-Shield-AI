import os
import csv
import json
import time
import urllib.request

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

os.makedirs("runs", exist_ok=True)
url = "http://127.0.0.1:8000/api/v1/phishing-simulation/simulate?stream=false"

results = []
run_counter = 1

print(f"Starting 28 Simulation Runs against {url}...")

for sc in SCENARIOS:
    for pr in PROFILES:
        run_id = f"RUN_{run_counter:03d}"
        payload = {
            "scenario": sc["name"],
            "employee_role": pr["role"],
            "behavior_profile": pr["profile"],
            "email_subject": sc["subject"],
            "email_body": sc["body"]
        }
        
        success = False
        attempts = 0
        while not success and attempts < 5:
            attempts += 1
            try:
                print(f"[{run_id}] Executing {sc['id']} ({sc['name']}) with profile '{pr['profile']}' (Attempt {attempts})...", flush=True)
                req_data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"})
                start_t = time.time()
                with urllib.request.urlopen(req) as resp:
                    res_json = json.loads(resp.read().decode("utf-8"))
                dur = round(time.time() - start_t, 2)
                
                reasoning = res_json.get("agent_reasoning", "")
                decision = res_json.get("agent_decision", "UNKNOWN")
                risk_score = res_json.get("risk_score", 0)
                severity = res_json.get("threat_severity", "UNKNOWN")
                confidence = res_json.get("confidence_score", 0)
                ts = res_json.get("timestamp", "")
                
                # Check fallback
                fallback_used = False
                if "Scanning incoming email headers" in reasoning or "Executing fallback streaming agent" in reasoning:
                    fallback_used = True
                
                # Save reasoning text file
                with open(os.path.join("runs", f"{run_id}.txt"), "w", encoding="utf-8") as f:
                    f.write(reasoning)
                
                row = {
                    "run_id": run_id,
                    "scenario_id": sc["id"],
                    "scenario_name": sc["name"],
                    "behavior_profile": pr["profile"],
                    "decision": decision,
                    "risk_score": risk_score,
                    "severity": severity,
                    "confidence_pct": confidence,
                    "duration_seconds": dur,
                    "model_name": "gemini-3.5-flash",
                    "fallback_used": fallback_used,
                    "timestamp": ts
                }
                results.append(row)
                print(f" -> Result: [{decision}] Risk: {risk_score}, Severity: {severity}, Conf: {confidence}%, Duration: {dur}s, Fallback: {fallback_used}", flush=True)
                success = True
            except Exception as e:
                print(f" -> Error on attempt {attempts}: {e}", flush=True)
                time.sleep(5.0)
        
        run_counter += 1
        time.sleep(3.0)  # Rate limit spacing

# Save CSV
csv_cols = [
    "run_id", "scenario_id", "scenario_name", "behavior_profile",
    "decision", "risk_score", "severity", "confidence_pct",
    "duration_seconds", "model_name", "fallback_used", "timestamp"
]

with open("results_live.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_cols)
    writer.writeheader()
    writer.writerows(results)

print("\n--- SIMULATION SUMMARY ---")
print(f"Total runs completed: {len(results)}")
distinct_scores = set(r["risk_score"] for r in results)
print(f"Distinct risk scores ({len(distinct_scores)}): {sorted(list(distinct_scores))}")

dec_counts = {}
for r in results:
    dec_counts[r["decision"]] = dec_counts.get(r["decision"], 0) + 1
print(f"Runs per decision: {dec_counts}")

profile_decisions = {}
for r in results:
    p = r["behavior_profile"]
    if p not in profile_decisions:
        profile_decisions[p] = set()
    profile_decisions[p].add(r["decision"])

for p, decs in profile_decisions.items():
    print(f"Profile '{p}' decisions across scenarios: {list(decs)}")

print("Done! Saved results_live.csv and 28 run text files in runs/.")
