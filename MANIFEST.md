# Screenshot Manifest & Verification Log

This document records the exact details, routes, transcribed screen values, and verification metadata for the paper screenshots generated from the live **SemanticShield AI** platform.

---

## Part 1 Results Summary (Table 4 Data)

- **Total Simulations Run:** 28 (7 scenarios × 4 behavioral profiles)
- **Model Called:** `gemini-3.5-flash` (Live Google GenAI API)
- **Fallback Generator Used:** `False` (0 fallback executions across all 28 runs)
- **Distinct Risk Score Values (2):** `18` (for SAFE outcomes) and `84` (for VULNERABLE outcomes)
- **Decision Distribution:** 15 `VULNERABLE`, 13 `SAFE`
- **Profile Decision Patterns:**
  - `trusting`: 7/7 `VULNERABLE` (100% vulnerability rate across all attack vectors)
  - `security_conscious`: 7/7 `SAFE` (100% safe outcome across all attack vectors)
  - `overwhelmed`: 5/7 `VULNERABLE`, 2/7 `SAFE` (Vulnerable to credential & package scams; Safe on M365 device alert & legitimate standup)
  - `executive`: 3/7 `VULNERABLE`, 4/7 `SAFE` (Vulnerable to password reset, device revocation, and MFA bypass; Safe on wire transfer, quishing, package hold, & standup)

---

## Part 2 Screenshot Manifest

### 1. `fig7_simulator_setup.png`
- **Filename:** `paper_screenshots/fig7_simulator_setup.png`
- **Route / Page:** `/admin/simulator` ([`Simulator.tsx`](file:///c:/Users/home/OneDrive/Desktop/Semantic_Sheild_AI/frontend/src/pages/Simulator.tsx))
- **Dimensions / Aspect Ratio:** 1600 × 900 px @ 2x Scale Factor (Full Width ~2:1)
- **Transcribed Screen Values:**
  - **Header Banner:** "Offensive AI Simulation Sandbox", "Phishing Simulation & Behavioral Threat Analysis"
  - **Scenario Catalog (7 scenarios):**
    - `SIM-EML-001`: Microsoft 365 Urgent Password Reset Scam (Classification: Phishing [Risk 88], Difficulty: Intermediate)
    - `SIM-EML-002`: Urgent Executive Wire Transfer Re-Verification (Classification: Critical [Risk 94], Difficulty: Advanced)
    - `SIM-EML-003`: HR Payroll Direct Deposit Bonus Form (Quishing) (Classification: Phishing [Risk 82], Difficulty: Beginner)
    - `SIM-EML-004`: FedEx Express Package Hold & Customs Fee Warning (Classification: Phishing [Risk 76], Difficulty: Beginner)
    - `SIM-EML-005`: M365 Security Alert: Unrecognized Device Revocation (Classification: Critical [Risk 90], Difficulty: Intermediate)
    - `SIM-EML-006`: Okta / Duo Push MFA Session Timeout Bypass (Classification: Critical [Risk 96], Difficulty: Advanced)
    - `SIM-EML-007`: Legitimate Team Weekly Standup Meeting (Classification: Safe [Risk 12], Difficulty: Beginner)
  - **Controls:** Search bar ("Search attack scenarios..."), Category Filter ("All Attack Categories"), Difficulty Filter ("All Difficulties").
  - **Action Buttons:** "Interactive Simulation", "Analyze with Defensive AI".

---

### 2. `fig8_vulnerable_result.png`
- **Filename:** `paper_screenshots/fig8_vulnerable_result.png`
- **Route / Page:** Modal Drawer on `/admin/simulator` ([`Simulator.tsx`](file:///c:/Users/home/OneDrive/Desktop/Semantic_Sheild_AI/frontend/src/pages/Simulator.tsx))
- **Dimensions / Aspect Ratio:** 768 × 810 px (Modal Drawer Crop, ~5:4 Aspect Ratio)
- **Transcribed Screen Values:**
  - **Scenario ID:** `SIM-EML-001` (Microsoft 365 Urgent Password Reset Scam)
  - **Behavioral Profile:** `Trusting (HR)` / `HR Manager`
  - **Streamed Reasoning Text:** Live streamed Gemini LLM reasoning text highlighting urgency cues, sender domain evaluation (`security@account-update-m365.com`), and decision to proceed with password reset.
  - **Agent Decision Result:** `[VULNERABLE]`
  - **Composite Risk Score:** `84/100`
  - **Threat Category:** `phishing`
  - **Severity Level:** `DANGEROUS`
  - **Confidence Score:** `98%`
  - **Duration:** `33.46s`
  - **Technique Explanation:** "Credential Harvesting / Brand Impersonation"

---

### 3. `fig9_safe_result.png`
- **Filename:** `paper_screenshots/fig9_safe_result.png`
- **Route / Page:** Modal Drawer on `/admin/simulator` ([`Simulator.tsx`](file:///c:/Users/home/OneDrive/Desktop/Semantic_Sheild_AI/frontend/src/pages/Simulator.tsx))
- **Dimensions / Aspect Ratio:** 768 × 810 px (Identical crop size to `fig8_vulnerable_result.png`)
- **Transcribed Screen Values:**
  - **Scenario ID:** `SIM-EML-001` (Microsoft 365 Urgent Password Reset Scam)
  - **Behavioral Profile:** `Security-Conscious (Dev)` / `Senior Developer`
  - **Streamed Reasoning Text:** Live streamed Gemini LLM reasoning examining domain mismatch, flagging unverified external link, and rejecting password reset request.
  - **Agent Decision Result:** `[SAFE]`
  - **Composite Risk Score:** `18/100`
  - **Threat Category:** `phishing`
  - **Severity Level:** `SAFE`
  - **Confidence Score:** `98%`
  - **Duration:** `14.31s`
  - **Technique Explanation:** "Credential Harvesting / Brand Impersonation"

---

### 4. `fig10_defensive_portal.png`
- **Filename:** `paper_screenshots/fig10_defensive_portal.png`
- **Route / Page:** `/dashboard` ([`UserDashboard.tsx`](file:///c:/Users/home/OneDrive/Desktop/Semantic_Sheild_AI/frontend/src/pages/UserDashboard.tsx))
- **Dimensions / Aspect Ratio:** 1600 × 900 px @ 2x Scale Factor (Full Width ~2:1)
- **Transcribed Screen Values:**
  - **Banner:** "Simulated payload 'Microsoft 365 Urgent Password Reset Scam' transferred from Offensive Lab."
  - **Defensive AI Classification:** `CRITICAL`
  - **Composite Risk Score:** `88/100`
  - **Confidence Score:** `94%`
  - **Incident ID:** `INC-001`
  - **AI Explanation Summary:** "Multi-agent threat analysis completed across WHOIS, DNS, and heuristic features. Detected credential harvesting keywords and sender domain mismatch."
  - **Flagged Phishing Indicators:** `Header Display Name Spoofing`, `Unverified Link Origin`, `High Pressure Urgency`
  - **Status Footer:** "Result automatically saved to Scan History & Dashboard"

---

### 5. `fig11_incidents.png`
- **Filename:** `paper_screenshots/fig11_incidents.png`
- **Route / Page:** `/admin/incidents` ([`Incidents.tsx`](file:///c:/Users/home/OneDrive/Desktop/Semantic_Sheild_AI/frontend/src/pages/Incidents.tsx))
- **Dimensions / Aspect Ratio:** 1600 × 900 px @ 2x Scale Factor (Full Width ~2:1)
- **Transcribed Screen Values:**
  - **Incident Records:** 28 simulation-tagged records (`is_simulation: true`) loaded from SQLite database (`semantic_shield.db`).
  - **Sample Transcribed Incidents:**
    - `INC-SIM-001` | SIM-EML-001 | Trusting (HR) | Risk: 84 | Severity: DANGEROUS | Status: Blocked
    - `INC-SIM-002` | SIM-EML-001 | Security-Conscious (Dev) | Risk: 18 | Severity: SAFE | Status: Resolved
    - `INC-SIM-005` | SIM-EML-002 | Trusting (HR) | Risk: 84 | Severity: DANGEROUS | Status: Blocked
  - **Activity Feed Stream:** Live activity stream logging real-time detection events with timestamps.

---

### 6. `fig12_analytics_persisted.png`
- **Filename:** `paper_screenshots/fig12_analytics_persisted.png`
- **Route / Page:** `/admin/analytics` ([`Analytics.tsx`](file:///c:/Users/home/OneDrive/Desktop/Semantic_Sheild_AI/frontend/src/pages/Analytics.tsx))
- **Dimensions / Aspect Ratio:** 1600 × 900 px @ 2x Scale Factor (Full Width ~2:1)
- **Persistence Verification:** Captured after complete backend Uvicorn server restart (`task-548`).
- **Transcribed Screen Values:**
  - **Total Simulation Records:** `28`
  - **Vulnerable vs Safe Distribution:** 15 Vulnerable (53.6%), 13 Safe (46.4%)
  - **Mean AI Confidence:** `98.0%`
  - **Risk Level Breakdown:** Critical/Dangerous: 15, Low/Safe: 13.

---

## Observations & UI Inconsistencies Log

1. **Gemini Model Name Alignment:**
   - Legacy model strings (`gemini-1.5-flash`, `gemini-2.0-flash`) return `404 NOT_FOUND` on Google GenAI API endpoint. Code was updated to `gemini-3.5-flash` which executed 100% of live runs successfully with zero fallbacks.
2. **Bimodal Discrete Risk Scores:**
   - The engine's score synthesis maps `[VULNERABLE]` to risk score `84` and `[SAFE]` to risk score `18`. This yields exactly two discrete values (`18` and `84`) across all 28 runs.
3. **Profile Consistency:**
   - The `trusting` profile yields `VULNERABLE` on 100% of scenarios (7/7).
   - The `security_conscious` profile yields `SAFE` on 100% of scenarios (7/7).
   - The `overwhelmed` and `executive` profiles produce mixed decisions depending on attack subtlety.
