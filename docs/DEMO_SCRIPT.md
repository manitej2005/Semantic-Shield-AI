# 🎬 SemanticShield AI – Live Demonstration & Presentation Script

> **Beginner-friendly, step-by-step presentation guide for demonstrating the full capability of SemanticShield AI to stakeholders, clients, or evaluators.**

---

## ⚡ 1. Pre-Demo Setup & Launch Instructions

Before starting the presentation, launch all services using two terminal windows:

### Terminal 1: Launch Backend Gateway
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*Verify backend API docs are live at `http://127.0.0.1:8000/docs`.*

### Terminal 2: Launch React Frontend
```bash
cd frontend
npm install
npm run dev
```
*Access frontend application at `http://localhost:5173`.*

### Chrome Browser: Load Sentinel Web Guard Extension
1. Open Chrome browser and navigate to `chrome://extensions`.
2. Enable **Developer Mode** (top-right toggle switch).
3. Click **Load unpacked** (top-left button).
4. Select the `extension/` directory from the repository.

---

## 🎭 Step-by-Step Demonstration Walkthrough

---

### Step 1: Platform Login
- **What to open**: Navigate to `http://localhost:5173` in Google Chrome.
- **What to click**: Click **Login to Platform** or access `http://localhost:5173/login`. Enter email `admin@semanticshield.ai` and password `admin123`.
- **What to say**: *"We begin by accessing the SemanticShield AI portal. The platform features role-based access control for Tier-3 lead security analysts."*
- **Expected Output**: User is authenticated and redirected to the Executive SOC Dashboard.

---

### Step 2: Executive SOC Dashboard Overview
- **What to open**: Executive SOC Dashboard (`http://localhost:5173/admin`).
- **What to click**: Point cursor to the high-level KPI cards and telemetry widgets.
- **What to say**: *"Here in the Executive Security Operations Center dashboard, security leads get a real-time summary of network health, including total scans, threat velocity, detection accuracy (99.4%), and operational telemetry across WHOIS, DNS, and Threat Intel provider plugins."*
- **Expected Output**: Gauges, charts, active incident cards, and provider health statuses display dynamically.

---

### Step 3: Open Phishing Simulation Lab
- **What to open**: Phishing Simulation Lab (`http://localhost:5173/simulator`).
- **What to click**: Click **Phishing Simulation Lab** in the primary navigation sidebar.
- **What to say**: *"Next, let's explore our offensive-defensive training environment: the Phishing Simulation Lab. This educational sandbox trains employees to recognize zero-day social engineering vectors before real attacks occur."*
- **Expected Output**: Grid of interactive attack scenarios (Credential Harvest, HR Scam, M365 Impersonation, MFA Fatigue) appears.

---

### Step 4: Select an Interactive Attack Vector
- **What to open**: Scenario card (e.g. **"M365 Urgent Password Reset & Credential Harvest"**).
- **What to click**: Click **Interactive Simulation**.
- **What to say**: *"Let's open a spear-phishing attack vector targeting employee Microsoft 365 credentials. Notice how realistic the raw email header and body content appear."*
- **Expected Output**: Simulated inbox modal opens displaying sender headers, subject line, and body payload.

---

### Step 5: Demonstrate Behavioral Threat Analysis
- **What to open**: Simulated Inbox Modal.
- **What to click**: Click decision control buttons: first **[Verify Sender]**, then **[Open Link]** or **[Report Phishing]**.
- **What to say**: *"As an employee interacts with this email, our Behavioral Threat Analysis engine evaluates their decision choices in real time. For instance, clicking an unverified link triggers a Critical Risk warning, whereas reporting the message awards exemplary defensive behavior."*
- **Expected Output**: Behavioral threat assessment card updates immediately with risk levels and actionable recommendations.

---

### Step 6: 1-Click Handoff to Defensive AI
- **What to open**: Bottom right of the Simulation Modal.
- **What to click**: Click **Analyze with Defensive AI**.
- **What to say**: *"Now, with one click, we transfer this exact payload from our offensive lab into our multi-agent defensive AI engine for instant deep technical inspection."*
- **Expected Output**: User is automatically navigated to `UserDashboard.tsx` with the payload pre-populated in the text area and scanning triggered.

---

### Step 7: Multi-Agent Deep Scan Execution
- **What to open**: User Defensive Portal (`UserDashboard.tsx`).
- **What to click**: Watch the scanner process the sample payload.
- **What to say**: *"Our multi-agent orchestrator dispatches the payload to specialized AI agents operating concurrently: the Semantic Agent evaluates LLM intent, the Behavior Agent checks psychological coercion, and the URL Agent checks domain heuristics."*
- **Expected Output**: Spinner animation finishes and the **Defensive AI Classification** card appears.

---

### Step 8: View Composite Risk Score & AI Explanation
- **What to open**: Scan Results Card.
- **What to click**: Highlight the Composite Risk Score gauge (e.g. **88/100 - CRITICAL**) and AI Explanation box.
- **What to say**: *"Unlike black-box security tools, SemanticShield AI provides complete explainability. It highlights exact risk factors, confidence scores, and an executive summary explaining why the attack was flagged."*
- **Expected Output**: Clear human-readable summary detailing display name spoofing, unverified link origins, and high-pressure urgency keywords.

---

### Step 9: Inspect Flagged Indicators & Generate Incident Report
- **What to open**: Scan Results Card actions.
- **What to click**: Click **View Full Report**.
- **What to say**: *"Analysts can instantly generate and export comprehensive Executive Summaries and Technical SOC Reports in PDF, Markdown, or STIX 2.1 threat intelligence format."*
- **Expected Output**: `ReportModal` opens displaying executive summary, technical breakdown, IoCs, and download/export buttons.

---

### Step 10: Review Scan History & Audit Trail
- **What to open**: Navigation Sidebar -> **Scan History** (`http://localhost:5173/incidents`).
- **What to click**: Click **Scan History / Incidents**.
- **What to say**: *"Notice that our completed scan has automatically synced across the entire application context into the central Scan History audit trail."*
- **Expected Output**: Searchable incidents table displays the newly evaluated threat alongside historical entries.

---

### Step 11: Activate Sentinel Web Guard Chrome Extension
- **What to open**: A new browser tab navigating to a test website or local HTML page.
- **What to click**: Click the **SemanticShield AI (Sentinel Web Guard)** icon in the Chrome extension toolbar.
- **What to say**: *"Now let's examine real-time edge browser protection using our Sentinel Web Guard Manifest V3 Chrome Extension."*
- **Expected Output**: Extension popup opens displaying real-time page threat score, classification badge, and key reasons.

---

### Step 12: Demonstrate Injected Warning Banner
- **What to open**: A suspicious or high-risk test page (where risk score >= 70).
- **What to click**: Observe the top of the browser viewport.
- **What to say**: *"If a user navigates to a high-risk phishing page, Sentinel Web Guard automatically injects an unignorable red warning banner directly at the top of the page, preventing credential submission before harm occurs."*
- **Expected Output**: High-visibility red alert banner renders with buttons **"Leave This Page"** and **"Dismiss Risk"**.

---

### Step 13: Bridge Extension Back to SOC Dashboard
- **What to open**: Chrome Extension Popup.
- **What to click**: Click **Open Full Audit in Dashboard**.
- **What to say**: *"Finally, clicking 'Open Full Audit' inside the browser extension instantly bridges the end user back into the executive SOC dashboard for deep investigation."*
- **Expected Output**: Chrome opens/focuses the React Dashboard (`http://localhost:5173/admin`).

---

## 🏆 Demonstration Conclusion

Conclude presentation with these 3 summary points:
1. **Dynamic Multi-Agent Intelligence**: Replaces static blocklists with real-time semantic and psychological threat scoring powered by Gemini LLMs.
2. **End-to-End Synergy**: Connects offensive employee simulation directly to defensive SOC investigation and edge browser protection.
3. **Transparent Explainability**: Provides clear human-readable AI reasoning and automated STIX 2.1 report generation.
