# 🚀 SemanticShield AI – Complete Run & Demonstration Guide

> **The ultimate step-by-step guide to installing, configuring, running, and presenting SemanticShield AI.**  
> *Includes setup commands for Windows/Linux/macOS, browser extension setup, full demo script, and troubleshooting.*

---

## 📑 Table of Contents
1. [📋 System Requirements](#1-system-requirements)
2. [⚙️ Prerequisites & Environment Setup](#2-prerequisites--environment-setup)
3. [🚀 Step-by-Step Application Execution](#3-step-by-step-application-execution)
   - [Backend Gateway (FastAPI)](#step-31-backend-gateway-fastapi)
   - [Frontend Dashboard (React + Vite)](#step-32-frontend-dashboard-react--vite)
   - [Sentinel Web Guard (Chrome Extension)](#step-33-sentinel-web-guard-chrome-extension)
4. [🔑 Default Access Credentials & Endpoints](#4-default-access-credentials--endpoints)
5. [🎭 Complete Demonstration Walkthrough (13-Step Script)](#5-complete-demonstration-walkthrough-13-step-script)
6. [🧪 QA Validation & Test Suite Execution](#6-qa-validation--test-suite-execution)
7. [🛠️ Troubleshooting & FAQs](#7-troubleshooting--faqs)

---

## 1. 📋 System Requirements

Ensure your development environment meets the following specifications:

| Requirement | Supported Version | Notes |
| :--- | :--- | :--- |
| **Node.js** | `v18.0.0` or higher | Tested on Node v20/v23 |
| **npm** | `v9.0.0` or higher | Comes bundled with Node |
| **Python** | `v3.10` to `v3.13` | Recommended `v3.10` or higher |
| **Browser** | Google Chrome / MS Edge | Required for Manifest V3 extension |
| **Gemini API Key** | Free tier or Paid key | Obtain from [Google AI Studio](https://aistudio.google.com/app/apikey) |

---

## 2. ⚙️ Prerequisites & Environment Setup

### 2.1 Clone Repository & Prepare Directory
```bash
git clone https://github.com/YourRepo/SemanticShield_AI.git
cd SemanticShield_AI
```

### 2.2 Configure Environment Variables
Copy the template `.env.example` file to create your `.env` configuration file in the project root:

```bash
# Copy example environment configuration
cp .env.example .env
```

Open `.env` in any text editor and add your **Google Gemini API Key**:
```env
ENVIRONMENT=development
DEBUG=True
PORT=8000
HOST=127.0.0.1

# 🔑 Add your Gemini API Key here (Required for live AI reasoning)
GEMINI_API_KEY=AIzaSy...your_gemini_api_key_here

# Security & CORS Settings
SECRET_KEY=semantic_shield_secret_key_2026
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,chrome-extension://*
```

*(Note: If no API key is provided, the system operates in fallback heuristic mode).*

---

## 3. 🚀 Step-by-Step Application Execution

To run the full application ecosystem, you will need **two terminal windows** (plus Google Chrome for the extension).

### Step 3.1: Backend Gateway (FastAPI)

Open **Terminal 1** and execute the following:

#### On Windows (PowerShell):
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Start FastAPI Uvicorn Server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### On Linux / macOS (Bash/Zsh):
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

✅ **Verification:** Open your browser and navigate to `http://127.0.0.1:8000/docs` to see the live OpenAPI / Swagger documentation page.

---

### Step 3.2: Frontend Dashboard (React + Vite)

Open **Terminal 2** and execute:

```bash
# Navigate to frontend directory
cd frontend

# Install Node modules
npm install

# Launch Vite development server
npm run dev
```

✅ **Verification:** Open `http://localhost:5173` in your browser. You will be greeted by the **SemanticShield AI Login / Executive SOC Portal**.

---

### Step 3.3: Sentinel Web Guard (Chrome Extension)

1. Launch **Google Chrome** or **Microsoft Edge**.
2. Navigate to `chrome://extensions` (or `edge://extensions`).
3. Turn **ON** the **Developer mode** toggle (top-right corner).
4. Click **Load unpacked** (top-left button).
5. Browse to the root of your project directory and select the `extension/` folder.
6. Click **Select Folder**.

✅ **Verification:** You will see the **Sentinel Web Guard** extension icon pinned in your browser toolbar with Manifest V3 support.

---

## 4. 🔑 Default Access Credentials & Endpoints

| Portal / Service | URL Endpoint | Credentials / Access |
| :--- | :--- | :--- |
| **React Frontend Portal** | `http://localhost:5173` | Main Web Interface |
| **Analyst Login** | `http://localhost:5173/login` | Email: `admin@semanticshield.ai`<br>Password: `admin123` |
| **Executive SOC Dashboard** | `http://localhost:5173/admin` | Tier-3 SOC Overview & Analytics |
| **Phishing Simulation Lab** | `http://localhost:5173/simulator` | Interactive Personas & Attack Sandbox |
| **Incident Scan History** | `http://localhost:5173/admin/incidents` | Complete Audit Trail & Report Exporter |
| **FastAPI Swagger Docs** | `http://127.0.0.1:8000/docs` | Interactive REST API Documentation |
| **FastAPI Healthcheck** | `http://127.0.0.1:8000/health` | Service Telemetry Endpoint |

---

## 5. 🎭 Complete Demonstration Walkthrough (13-Step Script)

Follow these exact 13 steps when giving a live presentation or recording a demo video:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DEMONSTRATION FLOW MAP                         │
│                                                                        │
│ [1. Login] ➔ [2. Executive Dashboard] ➔ [3. Simulation Lab]            │
│                     │                                                  │
│                     ▼                                                  │
│ [4. Select Vector] ➔ [5. Behavioral Choice] ➔ [6. 1-Click Handoff]     │
│                                                       │                │
│                                                       ▼                │
│ [9. Export Report] ◄── [8. Risk Score & Rationale] ◄── [7. Deep Scan] │
│        │                                                               │
│        ▼                                                               │
│ [10. Scan History] ➔ [11. Extension Active] ➔ [12. Warning Banner]    │
│                                                     │                  │
│                                                     ▼                  │
│                                          [13. Bridge to Dashboard]     │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Analyst Login
* **URL:** `http://localhost:5173`
* **Action:** Enter `admin@semanticshield.ai` / `admin123` and click **Login to Platform**.
* **Presenter Script:** *"We begin by logging into SemanticShield AI using Tier-3 SOC Analyst credentials, demonstrating role-based access control."*
* **Expected Result:** Authenticated user is smoothly redirected to the Executive SOC Dashboard.

---

### Step 2: Executive SOC Dashboard Overview
* **URL:** `http://localhost:5173/admin`
* **Action:** Hover over KPI stats, live detection accuracy metric (**99.4%**), threat velocity gauge, and provider plugin cards.
* **Presenter Script:** *"Here on the Executive SOC Dashboard, security leaders get instant visibility into total scans, live threat velocity, and operational telemetry across DNS, WHOIS, and Threat Intel plugins."*
* **Expected Result:** Dynamic charts, live incident tables, and system health status widgets populate cleanly.

---

### Step 3: Access Phishing Simulation Lab
* **URL:** Click **Phishing Simulation Lab** on the sidebar navigation (`/simulator`).
* **Action:** View the grid of pre-built educational attack scenarios.
* **Presenter Script:** *"Now let's open our offensive-defensive training sandbox: the Phishing Simulation Lab. This module evaluates how different employee behavioral personas react to zero-day social engineering vectors."*
* **Expected Result:** Scenario cards render displaying threat vectors like Credential Harvest, Wire Transfer Fraud, and Executive Impersonation.

---

### Step 4: Select Interactive Attack Scenario
* **Action:** Click **Interactive Simulation** on the **"M365 Urgent Password Reset & Credential Harvest"** card.
* **Presenter Script:** *"We select a high-pressure spear-phishing scenario targeting Microsoft 365 credentials. Notice the raw email headers, spoofed sender address, and urgency markers."*
* **Expected Result:** Simulated inbox drawer/modal opens displaying full email payload and decision control buttons.

---

### Step 5: Test Persona Decisions & Behavioral Risk Engine
* **Action:** Select an employee persona profile (e.g. **Trusting HR Manager** vs **Security-Conscious Developer**) and click **[Open Link]** or **[Report Phishing]**.
* **Presenter Script:** *"As an employee interacts with this email, our behavioral risk engine calculates their vulnerability in real time. Notice how a trusting persona clicking an unverified link raises risk to Critical, whereas reporting awards positive defensive points."*
* **Expected Result:** Live reasoning stream logs persona decisions and updates behavioral vulnerability score.

---

### Step 6: 1-Click Handoff to Defensive AI
* **Action:** Click **Analyze with Defensive AI** at the bottom of the simulation drawer.
* **Presenter Script:** *"With a single click, we hand off this exact phishing payload from the offensive simulation lab directly into our multi-agent defensive AI engine for deep technical analysis."*
* **Expected Result:** The payload is transferred automatically to the scanning portal (`UserDashboard.tsx`) with instant analysis triggered.

---

### Step 7: Live Multi-Agent Deep Scan Execution
* **Action:** Observe the scanning spinner and multi-agent coordination progress.
* **Presenter Script:** *"Our supervisor orchestrator dispatches three specialized agents concurrently: the Semantic Agent inspects Gemini LLM intent, the Behavior Agent checks psychological urgency, and the URL Agent checks domain heuristics."*
* **Expected Result:** Real-time analysis stream renders output cards with decision classification (`VULNERABLE` / `CRITICAL` / `PHISHING`).

---

### Step 8: Review Composite Risk Score & Explainable AI Reasoning
* **Action:** Inspect the **Composite Threat Score** (e.g., `88/100 - CRITICAL`), severity badge, and AI explanation text.
* **Presenter Script:** *"Unlike opaque legacy blocklists, SemanticShield AI provides total transparency. It breaks down exact risk weights (Semantic 40%, Behavior 25%, URL 35%) and explains step-by-step why the email was flagged."*
* **Expected Result:** Plain-language summary details display-name spoofing, deceptive domain registration, and coercive language patterns.

---

### Step 9: Generate & Export Comprehensive SOC Reports
* **Action:** Click **View Full Report** on the result card.
* **Presenter Script:** *"Analysts can instantly review executive summaries and export standardized SOC technical reports in PDF, Markdown, CSV, or STIX 2.1 threat intelligence format for SIEM ingestion."*
* **Expected Result:** `ReportModal` opens with tabs for Technical Breakdown, Indicators of Compromise (IoCs), STIX 2.1 JSON, and one-click PDF download.

---

### Step 10: Verify Incident History & Audit Trail
* **Action:** Click **Scan History / Incidents** on the navigation sidebar (`/admin/incidents`).
* **Presenter Script:** *"Every scan executed across the platform automatically synchronizes with our central incident database and audit trail."*
* **Expected Result:** The newly completed scan appears as the top incident in the searchable audit table.

---

### Step 11: Activate Sentinel Web Guard Chrome Extension
* **Action:** Open a browser tab visiting a test web page and click the **Sentinel Web Guard** extension icon.
* **Presenter Script:** *"Now let's switch to real-time edge protection with our Sentinel Web Guard Manifest V3 Chrome Extension."*
* **Expected Result:** Popup window displays real-time page threat score, domain category, and security indicators.

---

### Step 12: Demonstrate Injected High-Visibility Alert Banner
* **Action:** Visit a suspicious URL payload page (risk score >= 70).
* **Presenter Script:** *"If a user navigates to a high-risk phishing URL, Sentinel Web Guard automatically injects a prominent red alert banner directly at the top of the browser viewport to block credential submission."*
* **Expected Result:** Bright red warning banner appears with **"Leave This Page"** and **"Dismiss Risk"** options.

---

### Step 13: Bridge Extension Back to SOC Dashboard
* **Action:** Click **Open Full Audit in Dashboard** inside the extension popup.
* **Presenter Script:** *"Finally, clicking 'Open Full Audit' seamlessly bridges the end user back into the central SOC dashboard for detailed forensic investigation."*
* **Expected Result:** Browser switches back to the React Executive Dashboard (`/admin`).

---

## 6. 🧪 QA Validation & Test Suite Execution

To verify code quality and database persistence prior to a live presentation, execute the automated test suites:

### 6.1 Backend PyTest Suite
Run all backend unit, integration, and SOC API tests:
```bash
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate # Linux/macOS

pytest -v
```

### 6.2 Frontend Production Build Check
Verify TypeScript compilation and Vite build optimization:
```bash
cd frontend
npm run build
```

### 6.3 Run 28-Simulation Automated Batch Script
Run the automated multi-persona evaluation engine:
```bash
python run_28_simulations.py
```

---

## 7. 🛠️ Troubleshooting & FAQs

### Q1: `GEMINI_API_KEY` is missing or invalid.
* **Symptom:** AI analysis fails or throws `401 Unauthorized`.
* **Fix:** Verify `.env` file exists in project root with valid key `GEMINI_API_KEY=AIzaSy...`. The backend automatically falls back to heuristic mode if no key is present.

### Q2: Port 8000 or Port 5173 is already in use.
* **Symptom:** `OSError: [Errno 10048] address already in use`.
* **Fix:** Kill existing process or specify custom port:
  ```powershell
  # Windows PowerShell kill process on port 8000:
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
  ```

### Q3: Chrome Extension fails to connect to backend.
* **Symptom:** Extension popup displays `Offline / Backend unreachable`.
* **Fix:** Ensure FastAPI backend is running on `http://127.0.0.1:8000`. Check that `ALLOWED_ORIGINS` in `.env` includes `chrome-extension://*`.

### Q4: Database tables missing.
* **Symptom:** SQLite error `no such table: incidents`.
* **Fix:** Run database initialization / migration script:
  ```bash
  cd backend
  python -m app.db.init_db
  ```

---

### 🌟 Quick Command Summary
```bash
# 1. Start Backend
cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload

# 2. Start Frontend
cd frontend && npm run dev

# 3. Load Extension in Chrome
chrome://extensions -> Load unpacked -> select extension/
```
