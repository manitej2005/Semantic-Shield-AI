# ⚡ SemanticShield AI — FastAPI Backend Service

> **Enterprise Clean Architecture FastAPI backend providing real-time multi-agent threat analysis, threat intelligence provider plugins, and executive dashboard metrics.**

---

## 🏗️ Backend Directory Structure

```
backend/
├── app/                      # Clean Architecture Python Application Package
│   ├── main.py               # FastAPI Application Entrypoint & Middleware Setup
│   ├── api/                  # API Endpoints (v1 Router, Threats, Emails, URLs, Incidents, Reports)
│   ├── services/             # Business Services, Threat Intel Registry & Aggregator
│   ├── agents/               # Multi-Agent Orchestrator (Supervisor, Semantic, URL, Behavior)
│   ├── domain/               # Core Entities, Models, Enums & System Interfaces
│   ├── schemas/              # Pydantic Schemas for Request/Response Validation
│   ├── core/                 # App Settings, Security Configuration & Logging
│   ├── engines/              # Heuristic Risk Assessment Engines & Builders
│   ├── middleware/           # CORS Setup & HTTP Request Logging Middleware
│   ├── orchestrator/         # Multi-Agent Parallel Execution Pipeline
│   └── utils/                # Helper Formatting & Sanitization Utilities
│
├── tests/                    # Unit, Integration & Automated Test Suite
├── analyzers/                # Backward Compatibility Analyzer Shim
├── services/                 # Backward Compatibility Service Shim
├── main.py                   # Root Gateway Gateway Entrypoint Shim (`from app.main import app`)
├── requirements.txt          # Python Dependencies Manifest
└── README.md                 # Backend Documentation
```

---

## 🚀 Quick Start & Setup

### 1. Environment Setup
```bash
python -m venv venv
```
Activate virtual environment:
- **Windows**: `.\venv\Scripts\activate`
- **Linux/macOS**: `source venv/bin/activate`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI Server
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Interactive API Documentation
Once running, open your browser:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 🧪 Running Tests

Run backend tests from the `backend/` directory:
```bash
python tests/test_soc_integration.py
python tests/test_threat_engine.py
python tests/test_incident_management.py
python tests/test_email_url_engine.py
python tests/test_ai_investigation.py
```
