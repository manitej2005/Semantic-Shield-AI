# 🏗️ SemanticShield AI Architecture & Technical Overview

> **Deep-dive architectural documentation for developers detailing system design, communication protocols, API specifications, state synchronization, and Chrome Extension internals.**

---

## 1. System Architecture Overview

SemanticShield AI employs an **Agentic Clean Architecture** split across three decoupled tiers:

1. **Frontend Tier (React + Vite + TypeScript)**: Single-page executive SOC dashboard and user defensive portal.
2. **Backend Tier (Python FastAPI + Clean Architecture)**: Asynchronous multi-agent threat engine, supervisor orchestrator, and threat intelligence provider registry.
3. **Client Extension Tier (Manifest V3 Chrome Extension)**: Edge browser security guard intercepting active DOM content and rendering real-time safety badges and warning banners.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CHROME BROWSER EXTENSION                         │
│  [content.js] ──(DOM Text)──> [background.js] ──(POST /analyze)──┐      │
└──────────────────────────────────────────────────────────────────│──────┘
                                                                   │
┌──────────────────────────────────────────────────────────────────│──────┐
│                         REACT FRONTEND                           │      │
│  [UserDashboard.tsx] ──(REST POST /api/v1/url/analyze)───────────┤      │
│  [AdminDashboard.tsx] <──(WebSocket /ws/dashboard)───────────────┼──────┤
│  [DashboardContext.tsx] (Central Reactive State)                 │      │
└──────────────────────────────────────────────────────────────────│──────┘
                                                                   │
                                                                   v
┌─────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND GATEWAY                         │
│                         (backend/app/main.py)                           │
│                                  │                                      │
│                     [app/orchestrator/supervisor.py]                    │
│                        (SupervisorAgent Orchestrator)                   │
│                                  │                                      │
│       ┌──────────────────────────┼──────────────────────────┐           │
│       │ (asyncio.gather)         │ (asyncio.gather)         │           │
│       v                          v                          v           │
│ [SemanticAgent]           [BehaviorAgent]            [URLIntelAgent]    │
│ (Gemini API LLM)          (Coercion Engine)          (Heuristics & TI)  │
│       │                          │                          │           │
│       └──────────────────────────┼──────────────────────────┘           │
│                                  v                                      │
│                       [Risk & Explainability Engine]                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. API Endpoints Specification

Below are the primary API endpoints exposed by the FastAPI backend gateway:

### Core Analysis Endpoints
- **`POST /analyze` & `POST /api/v1/analyze`**: Primary endpoint used by the Chrome Extension and general clients. Accepts `AnalyzeRequest` (`url`, `page_text`) and returns full multi-agent risk evaluation.
- **`POST /api/v1/url/analyze`**: Dedicated endpoint for URL technical heuristics, WHOIS, DNS, SSL, and threat intelligence lookup.
- **`POST /api/v1/email/analyze`**: Endpoint for analyzing raw MIME email headers, text body, SPF/DKIM flags, and display name spoofing.
- **`POST /api/v1/email/upload`**: Multipart file upload handler accepting RFC822 `.eml` files.

### SOC & Dashboard Endpoints
- **`GET /api/dashboard`**: Unified master SOC dashboard payload containing stats, recent incidents, activity feed, and provider health.
- **`GET /api/dashboard/summary`**: High-level SOC KPI metrics.
- **`GET /api/dashboard/activity`**: Recent system activity timeline logs.
- **`GET /api/dashboard/analytics`**: Operational analytics and threat type distributions.
- **`GET /api/dashboard/health`**: Unified operational health telemetry.
- **`GET /api/dashboard/providers`**: Latency and health metrics for threat intelligence providers.
- **`GET /api/incidents`**: List of active security incidents.

### Investigation & Reporting Endpoints
- **`POST /api/investigation/analyze`**: Correlates email and URL evidence, maps MITRE ATT&CK techniques (T1566), and generates verdict.
- **`POST /api/investigation/explain`**: Generates human-readable reasoning and key supporting evidence rationale.
- **`POST /api/reports/export`**: Exports incident telemetry or reports in `json`, `markdown`, `csv`, or `stix` (STIX 2.1) format.

### Real-Time WebSocket Channels
- **`WS /ws/dashboard`**: Persistent channel broadcasting live dashboard telemetry.
- **`WS /ws/incidents`**: Live security alerts and incident updates.
- **`WS /ws/activity`**: Real-time activity feed events.

---

## 3. How Scans are Triggered & Processed

```
[User Action or Extension Event]
              │
              v
 [HTTP POST Payload Sent to Backend]
              │
              v
   [SupervisorAgent Orchestrator]
              │
   ┌──────────┴──────────┐
   │ Parallel Fan-Out    │ (asyncio.gather)
   v                     v
[Semantic Agent]  [Behavior Agent]  [URL Intel Agent]
(Gemini API)      (Psychological)   (Heuristics/WHOIS)
   │                     │                 │
   └──────────┬──────────┘                 │
              v                            │
     [Risk Assessment Engine] <────────────┘
     (Computes Weighted Score 0-100)
              │
              v
 [Explainability Engine]
 (Generates AI Reasons & Mitigations)
              │
              v
 [Unified JSON Response Returned]
```

1. **Trigger**: A scan is initiated either automatically by the Chrome Extension upon navigating to a website, or manually by a user in `UserDashboard.tsx`.
2. **Dispatch**: The backend endpoint receives the request payload and hands it to `SupervisorAgent` (`app/orchestrator/supervisor.py`).
3. **Parallel Agent Execution**: The Supervisor Agent uses `asyncio.gather()` to concurrently trigger:
   - `SemanticAnalysisAgent`: Evaluates text intent using Google Gemini API.
   - `BehaviorAnalysisAgent`: Analyzes coercion keywords, authority pressure, and urgency.
   - `URLIntelligenceAgent`: Checks domain age (WHOIS), DNS SPF records, SSL certificates, and threat intel feeds.
4. **Scoring & Rationale**: The `RiskEngine` calculates a composite score (0–100) and maps it to a classification (`High Risk`, `Suspicious`, `Safe`). The `ExplainabilityEngine` generates transparent reasoning steps.
5. **Response Delivery**: Output is packaged as JSON and returned to the client.

---

## 4. Frontend `DashboardContext` State Synchronization

The React frontend utilizes a central state provider (`frontend/src/contexts/DashboardContext.tsx`) to keep all UI views synchronized:

- **State Sync Loop**:
  1. When a scan completes in `UserDashboard.tsx`, the resulting payload is passed to `addCompletedScan()`.
  2. `addCompletedScan()` updates `stats` (incrementing total threats / critical threats), adds a new `ThreatIncident` to `incidents` (updating Scan History in `Incidents.tsx`), inserts an entry into `activities` (updating live activity feeds), and triggers a `ToastNotification`.
  3. All dependent components (`AdminDashboard`, `Incidents`, `Analytics`, `UserDashboard`) re-render reactively without requiring page reloads.

---

## 5. Chrome Extension Architecture & Backend Communication

The browser extension (`extension/`) operates under Manifest V3 specifications:

- **`manifest.json`**: Defines permissions (`activeTab`, `scripting`, `storage`, `webNavigation`) and host permissions for `http://127.0.0.1:8000/*`.
- **`background.js`**:
  1. Listens for `chrome.webNavigation.onCompleted` events for main frames (`frameId === 0`).
  2. Injects `content.js` into the tab.
  3. Sends an `extractText` message to `content.js` with a 1.5-second timeout safeguard.
  4. Sends an HTTP `POST` request to `http://127.0.0.1:8000/analyze` containing `{url, page_text}`.
  5. Caches the result in `chrome.storage.local` under key `tab_<tabId>`.
  6. If the score is >= 70 or classification is High Risk, sends a `showWarningBanner` message to `content.js`.
- **`content.js`**:
  1. Extracts up to 2,000 characters of visible DOM text (`document.body.innerText`).
  2. Upon receiving `showWarningBanner`, injects a fixed red warning banner (`z-index: 2147483647`) pushing body content down and displaying options to "Leave This Page" or "Dismiss Risk".
- **`popup/`**:
  1. Queries `background.js` via `getResult` message.
  2. Displays real-time risk score badge, classification, top risk reasons, and a button to **"Open Full Audit in Dashboard"** (`http://localhost:5173`).

---

## 6. Phishing Simulation Handoff to Analysis

```
┌──────────────────────────────────────────────────────────┐
│                  Phishing Simulation Lab                 │
│                      (Simulator.tsx)                     │
│                                                          │
│  1. User selects scenario & tests decision choice        │
│  2. Behavioral Assessment evaluates risk level           │
│  3. User clicks "Analyze with Defensive AI"              │
└────────────────────────────┬─────────────────────────────┘
                             │
                             v
                context.setTransferredSample(sample)
                             │
                             v
┌──────────────────────────────────────────────────────────┐
│                 Defensive AI User Portal                 │
│                    (UserDashboard.tsx)                   │
│                                                          │
│  1. Detects transferredSample in DashboardContext       │
│  2. Auto-prepopulates text area                          │
│  3. Triggers 1-click Defensive AI scan                   │
│  4. Renders composite score, rationale & IoCs            │
└──────────────────────────────────────────────────────────┘
```

This seamless 1-click transition bridges offensive educational scenarios directly into defensive multi-agent analysis for demonstration and auditing purposes.
