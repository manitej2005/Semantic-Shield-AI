# 🛡️ SemanticShield AI

**An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis**

SemanticShield AI simulates how different types of employees react to the same phishing email, then classifies the resulting threat. The same email can be harmless to a security-aware developer and dangerous to a trusting HR manager. This project makes that difference visible and measurable.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Behavioral Profiles](#-behavioral-profiles)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Team](#-team)
- [Disclaimer](#-disclaimer)

---

## 🔍 Overview

Most phishing tools only answer one question: *"Is this email malicious?"*
SemanticShield AI also asks: ***"Who would fall for it, and why?"***

The system has two parts:

1. **Phishing Simulation Agent:** An LLM-driven agent (Gemini) role-plays an employee with a specific job role and behavioral profile, reads a phishing email, and reasons out loud before deciding whether it is **VULNERABLE** or **SAFE**.
2. **Behavioral Threat Analysis:** The simulation result goes through a multi-agent risk engine that categorizes the threat, scores its severity, and logs it as an incident for review.

---

## ✨ Key Features

- 🎭 **4 behavioral employee profiles** that react differently to the same email
- 🧠 **Real-time streaming** of the agent's reasoning, so you see it think step by step
- 📊 **Multi-agent risk scoring** (Semantic + Behavior + URL Intelligence)
- 🚨 **Automatic incident creation**, with simulations flagged separately from real threats
- 📡 **Live updates** over WebSockets
- 🗂️ **Activity feed and audit trail** for every simulation run
- 🧱 **Clean Architecture**: domain, services, orchestrator and API layers are separated

---

## ⚙️ How It Works

```
Scenario + Role + Profile + Email
              │
              ▼
   Phishing Simulation Engine
              │
              ▼
   Gemini API (streamed reasoning)
              │
              ▼
   Decision: [VULNERABLE] / [SAFE]
              │
              ▼
   Risk Engine (weighted multi-agent scoring)
              │
              ▼
   Incident Manager + Activity Feed
              │
              ▼
   WebSocket broadcast → React UI
```

**Risk Engine weights**

| Agent | Weight |
|---|---|
| Semantic Analysis | 40% |
| Behavior Analysis | 25% |
| URL Intelligence | 35% |

**Risk thresholds**

| Score | Level |
|---|---|
| ≥ 65 | 🔴 Dangerous |
| ≥ 35 | 🟡 Suspicious |
| < 35 | 🟢 Safe |

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, FastAPI |
| LLM | Google Gemini API |
| Validation | Pydantic v2 |
| Database | SQLite (SQLAlchemy + Alembic migrations) |
| Frontend | React |
| Real-time | WebSockets |

---

## 📁 Project Structure

```
SemanticShield-AI/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   │   └── phishing_simulation.py
│   │   ├── engines/
│   │   │   └── risk_engine.py
│   │   ├── orchestrator/
│   │   │   └── supervisor.py
│   │   ├── schemas/
│   │   │   └── phishing_simulation.py
│   │   ├── services/
│   │   │   ├── phishing_simulation/
│   │   │   │   ├── engine.py
│   │   │   │   ├── gemini_handler.py
│   │   │   │   └── system_prompts.py
│   │   │   ├── incident_management/
│   │   │   ├── activity/
│   │   │   ├── websocket/
│   │   │   └── storage/
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   └── package.json
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- A [Gemini API key](https://aistudio.google.com/) (the free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/SemanticShield-AI.git
cd SemanticShield-AI
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env      # then add your API keys
uvicorn app.main:app --reload
```

The backend runs at `http://localhost:8000`. Interactive API docs are at `http://localhost:8000/docs`.

### 3. Set up the frontend

```bash
cd frontend
npm install
npm start
```

The frontend runs at `http://localhost:3000`.

---

## 🔐 Environment Variables

Create a `.env` file inside `backend/`:

```env
GEMINI_API_KEY=your_gemini_api_key
VIRUSTOTAL_API_KEY=your_key_optional
ABUSEIPDB_API_KEY=your_key_optional
URLSCAN_API_KEY=your_key_optional
WHOIS_API_KEY=your_key_optional

ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
SECRET_KEY=change_this_to_a_random_string
ALLOWED_ORIGINS=http://localhost:3000
```

> ⚠️ **Never commit your `.env` file.** Only `.env.example` (with empty values) belongs in the repo.

---

## 📡 API Reference

### Run a phishing simulation

`POST /api/v1/phishing-simulation/simulate`

**Request**

```json
{
  "scenario": "Microsoft 365 Credential Harvest",
  "employee_role": "HR Manager",
  "behavior_profile": "trusting",
  "email_subject": "Urgent: Verify Your Account",
  "email_body": "Your account will be suspended in 24 hours..."
}
```

**Response**

```json
{
  "simulation_id": "uuid",
  "agent_reasoning": "Full step-by-step reasoning from the agent...",
  "agent_decision": "VULNERABLE",
  "threat_category": "Phishing - Credential Harvest",
  "threat_severity": "CRITICAL",
  "confidence_score": 94,
  "duration_seconds": 3.2,
  "is_simulation": true
}
```

**Status codes:** `200` success · `400` invalid input · `503` LLM unavailable · `504` LLM timeout

### Other endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/status` | System status |
| GET | `/api/v1/incidents` | List incidents |
| WS | `/api/dashboard/ws/*` | Live dashboard, incident and activity channels |

---

## 🎭 Behavioral Profiles

| Profile | Role | Typical behavior |
|---|---|---|
| **Trusting** | HR Manager | Assumes internal-looking emails are legitimate |
| **Security-Conscious** | Developer | Inspects sender domains, headers and links |
| **Overwhelmed** | Finance Manager | Rushes under workload and time pressure |
| **Executive** | VP | Acts on authority and urgency, delegates checks |

**Attack scenarios:** Microsoft 365 credential harvest · Wire transfer fraud · Executive impersonation · QR code phishing

---

## 🖼️ Screenshots

> Add your screenshots to a `docs/screenshots/` folder and link them here.

| Simulation Setup | Live Analysis |
|---|---|
| ![Setup](docs/screenshots/setup.png) | ![Analysis](docs/screenshots/analysis.png) |

---

## 🗺️ Roadmap

- [x] Multi-agent risk engine and incident management
- [x] Phishing simulation module with 4 behavioral profiles
- [x] Streaming agent reasoning
- [x] SQLite persistence with migrations
- [x] Two-panel simulation UI
- [ ] Migrate SQLite → Supabase
- [ ] Authentication and multi-user support
- [ ] Exportable training reports per employee profile
- [ ] Cloud deployment

---

## 👥 Team

**Malla Reddy University** · Dept. of Cyber Security, ECE & IoT

- K. Mani Tej Kumar
- Ch. Avinash
- K. Kowshik

---

## ⚠️ Disclaimer

SemanticShield AI is built for **educational and defensive security research only**. The phishing scenarios are simulations intended to improve security awareness. Do not use this tool to target real individuals or organizations.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
