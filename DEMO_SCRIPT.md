# 🎬 SemanticShield AI Live Demonstration Script

> **Master step-by-step presentation guide for demonstrating SemanticShield AI.**  
> *For full script details and word-for-word presentation prompts, see [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md).*

---

## ⚡ Quick Startup Order

1. **Backend**: `cd backend` -> `python -m uvicorn app.main:app --reload` (Runs on `http://127.0.0.1:8000`)
2. **Frontend**: `cd frontend` -> `npm run dev` (Runs on `http://localhost:5173`)
3. **Extension**: Open `chrome://extensions` -> **Load unpacked** -> Select `extension/` directory.

---

## 🎭 13-Step Demonstration Summary

1. **Login**: Access `http://localhost:5173` with analyst credentials (`admin@semanticshield.ai` / `admin123`).
2. **SOC Dashboard**: Review real-time SOC metrics, threat velocity gauge, and subsystem telemetry cards (`/admin`).
3. **Phishing Simulation Lab**: Open the educational simulation sandbox (`/simulator`).
4. **Select Scenario**: Choose an interactive attack vector (e.g. M365 Password Reset / Wire Transfer Fraud).
5. **Behavioral Analysis**: Demonstrate interactive decision choices ([Verify Sender], [Open Link], [Report Phishing]) and view real-time behavioral risk scoring.
6. **1-Click AI Handoff**: Click **"Analyze with Defensive AI"** to transfer payload to the defensive scanner.
7. **Defensive AI Scan**: Execute multi-agent analysis (Supervisor, Semantic/Gemini, Behavior, URL Agents).
8. **Risk Score & Rationale**: View composite risk score (0–100), classification (`Critical`/`Phishing`), and AI reasoning.
9. **Executive & SOC Reports**: Click **View Full Report** to view and export reports in PDF, Markdown, CSV, or STIX 2.1 format.
10. **Scan History**: Show that completed scan automatically synchronized to the historical audit trail (`/incidents`).
11. **Browser Extension**: Activate Sentinel Web Guard Chrome extension on an active web page.
12. **Extension Alert Banner**: Show real-time risk score popup and injected red warning banner on high-risk pages.
13. **Dashboard Bridge**: Click **"Open Full Audit in Dashboard"** inside the extension popup to bridge directly back to the React Executive SOC Dashboard.
