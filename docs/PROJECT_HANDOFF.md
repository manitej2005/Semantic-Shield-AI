# Project Handoff Document

# An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis

> **SemanticShield AI** — Comprehensive Cybersecurity Platform for Real-Time Threat Analysis, Multi-Agent AI Phishing Detection, and Controlled Simulation.

---

## 📌 Project Overview & Title

**Project Title**: *An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis*  
**Platform Name**: SemanticShield AI  
**Architecture Style**: Clean Architecture (FastAPI Backend) + React Single-Page Application (Frontend) + Manifest V3 Browser Extension  

---

## 📊 Current Status

| Milestone | Scope & Description | Status |
| :--- | :--- | :---: |
| **Milestone 1** | Core Threat Intelligence Engine, Multi-Agent Supervisor, Manifest V3 Extension & FastAPI Backend | `✓ Completed` |
| **Milestone 2** | Enterprise SOC Integration, Dashboard Aggregator, Real-time WebSockets, Threat Feed & Health Telemetry | `✓ Completed` |
| **Milestone 3** | Phishing Simulation Lab, Behavioral Analysis, AI Security Assistant & Advanced Reporting | `✓ Completed / In Progress` |

---

## 🚀 Existing Major Features

1. **Authentication & User Context**: User login state management and authenticated dashboard session control.
2. **SOC Executive Dashboard**: Real-time KPI summaries, threat velocity metrics, recent security alerts, and subsystem telemetry cards.
3. **URL Scanner**: Deep technical heuristic analysis combined with Gemini LLM semantic verification for suspicious web URLs.
4. **Email Scanner**: Full raw MIME EML header and body parsing, evaluating display name spoofing, SPF/DKIM flags, and harvesting links.
5. **File Scanner**: Static payload inspection, entropy calculation, sha256 IoC hash matching against threat databases.
6. **Multi-Agent AI Analysis**: Autonomous multi-agent pipeline (Supervisor Agent, Semantic Analysis Agent, Behavior Analysis Agent, URL Intelligence Agent).
7. **WHOIS Lookup Plugin**: Live and mock domain registration date, registrar reputation, and domain age verification.
8. **DNS Analysis Plugin**: Mail server MX record validation, SPF policy checks, and IP resolve inspection.
9. **SSL / TLS Analysis**: Transport security certificate validation, issuer trustworthiness, and expiry evaluation.
10. **IoC Extraction**: Automated extraction of domain indicators, IPv4 addresses, and cryptographic file hashes.
11. **Reports & PDF Export**: Executive and technical threat reports with risk matrix, key indicators, and mitigation steps.
12. **Scan History**: Full historical log of evaluated URLs, emails, and files with downloadable audit trails.
13. **Threat Analytics & Visualization**: Visual graphs rendering threat distribution, risk level breakdowns, and accuracy trends.
14. **AI Security Assistant**: Interactive conversational cybersecurity chatbot providing real-time guidance on active threats.
15. **Phishing Simulation Lab**: Controlled educational training scenarios (OAuth Grant Abuse, Spear-Phishing Credential Harvest, CEO Fraud) for user awareness.
16. **Behavioral Threat Analysis**: Psychological coercion detection evaluating artificial urgency, fear tactics, and authority abuse.
17. **Sentinel Web Guard (Browser Extension)**: Manifest V3 Chrome extension providing real-time DOM scraping, warning banner injection, and quick score popups.

---

## 🎯 Current Development Direction & Principles

1. **Keep Analysis Real**: Prioritize real dynamic heuristics and live/verifiable AI model scoring over hardcoded static output.
2. **Avoid Hardcoded Scan Results**: Every scanner (URL, Email, File) executes actual heuristic pipelines and Gemini API calls (or structured fallback algorithms when unconfigured).
3. **Preserve Existing APIs**: Maintain backward compatibility across root gateway endpoints (`/analyze`, `/health`, `/status`) and versioned endpoints (`/api/v1/*`).
4. **Browser Extension Focus**: The Chrome browser extension (`extension/`) is a pivotal demonstration asset — keep DOM scraping and backend communication intact.
5. **Controlled Phishing Simulations**: Phishing simulation scenarios must remain strictly educational, safe, and confined to the local sandbox.
6. **Local Execution & Privacy**: The full platform is optimized to run locally on developer workstations (`127.0.0.1`) without external cloud lock-in.
7. **Maintain Lean Scope**: Do not introduce unnecessary enterprise bloat or cloud infrastructure dependencies; maintain a clean, modular structure.

---

## 📁 Repository Structure Summary

```
SemanticShield-AI/
├── frontend/             # React SPA (Vite + TypeScript + Tailwind CSS)
├── backend/              # FastAPI Python Backend (Clean Architecture)
├── extension/            # Manifest V3 Chrome Extension (Sentinel Web Guard)
├── docs/                 # Platform Architecture, Setup Guides & Scripts
├── tests/                # Top-Level & Integration Tests
├── .env.example          # Environment Variable Configuration Template
├── .gitignore            # Master Project GitIgnore Rules
├── README.md             # Project Master Documentation
└── DEMO_SCRIPT.md        # Comprehensive 13-Step Live Demonstration Guide
```
