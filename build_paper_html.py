import os
import sys
import json
import base64
import pandas as pd

def get_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            ext = os.path.splitext(filepath)[1].lower().strip(".")
            mime = "image/png" if ext == "png" else "image/svg+xml" if ext == "svg" else "image/jpeg"
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def build_paper():
    csv_path = "paper/data/results_all.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist yet.")
        return

    df = pd.read_csv(csv_path)
    total_runs = len(df)
    valid_df = df[df["fallback_used"].astype(str).str.lower() != "true"] if "fallback_used" in df.columns else df

    malicious_df = valid_df[valid_df["scenario_id"] != "SIM-EML-007"]
    control_df = valid_df[valid_df["scenario_id"] == "SIM-EML-007"]

    susc_trusting = (malicious_df[malicious_df["behavior_profile"] == "trusting"]["decision"] == "VULNERABLE").mean() * 100.0
    susc_security = (malicious_df[malicious_df["behavior_profile"] == "security_conscious"]["decision"] == "VULNERABLE").mean() * 100.0
    susc_overwhelmed = (malicious_df[malicious_df["behavior_profile"] == "overwhelmed"]["decision"] == "VULNERABLE").mean() * 100.0
    susc_exec = (malicious_df[malicious_df["behavior_profile"] == "executive"]["decision"] == "VULNERABLE").mean() * 100.0

    mean_vuln_risk = valid_df[valid_df["decision"] == "VULNERABLE"]["risk_score"].mean()
    mean_safe_risk = valid_df[valid_df["decision"] == "SAFE"]["risk_score"].mean()
    mean_latency = valid_df["duration_seconds"].mean()

    imgs = {}
    for i in range(1, 17):
        if i <= 6:
            names = ["fig1_three_tier_architecture", "fig2_data_flow_diagram", "fig3_use_case_diagram", "fig4_sequence_diagram", "fig5_class_diagram", "fig6_activity_diagram"]
            fn = names[i-1]
        elif i <= 10:
            names = ["fig7_susceptibility_rate", "fig8_scenario_profile_heatmap", "fig9_risk_score_distribution", "fig10_latency_per_profile"]
            fn = names[i-7]
        else:
            names = ["fig11_simulator_setup", "fig12_vulnerable_result", "fig13_safe_result", "fig14_defensive_portal", "fig15_incidents", "fig16_analytics_persisted"]
            fn = names[i-11]

        imgs[f"fig{i}"] = get_base64(f"paper/figures/{fn}.png")

    os.makedirs("paper/source", exist_ok=True)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SemanticShield AI — An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 20mm 15mm 20mm 15mm;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 10.2pt;
    line-height: 1.28;
    color: #000000;
    text-align: justify;
    background-color: #ffffff;
  }}

  /* Title Block */
  .title-block {{
    text-align: center;
    margin-bottom: 7mm;
  }}

  .paper-title {{
    font-size: 19pt;
    font-weight: bold;
    line-height: 1.25;
    margin-bottom: 6mm;
  }}

  .authors-grid {{
    display: table;
    width: 100%;
    margin-bottom: 6mm;
  }}

  .author-col {{
    display: table-cell;
    width: 33.33%;
    text-align: center;
    vertical-align: top;
    padding: 0 2mm;
  }}

  .author-name {{
    font-size: 11pt;
    font-weight: bold;
    margin-bottom: 2pt;
  }}

  .author-dept {{
    font-size: 9.2pt;
    line-height: 1.22;
    color: #111111;
  }}

  .author-email {{
    font-size: 8.8pt;
    font-family: 'Courier New', Courier, monospace;
    color: #222222;
    margin-top: 2pt;
  }}

  /* Abstract Block */
  .abstract-container {{
    width: 100%;
    margin-bottom: 7mm;
    padding-bottom: 5mm;
    border-bottom: 0.5pt solid #555555;
  }}

  .abstract-heading {{
    font-size: 12pt;
    font-weight: bold;
    margin-bottom: 3mm;
  }}

  .abstract-text {{
    font-size: 9.8pt;
    line-height: 1.25;
    text-align: justify;
    margin-bottom: 3mm;
  }}

  .keywords-line {{
    font-size: 9.5pt;
    line-height: 1.25;
  }}

  .keywords-label {{
    font-weight: bold;
    font-style: italic;
  }}

  /* Main Body Layout */
  .main-body {{
    column-count: 2;
    column-gap: 8mm;
  }}

  h1 {{
    font-size: 11.8pt;
    font-weight: bold;
    margin-top: 6mm;
    margin-bottom: 2.8mm;
    break-after: avoid;
  }}

  h2 {{
    font-size: 10.8pt;
    font-weight: bold;
    margin-top: 5mm;
    margin-bottom: 2.2mm;
    break-after: avoid;
  }}

  p {{
    text-indent: 1.2em;
    margin-bottom: 3mm;
  }}

  p.no-indent {{
    text-indent: 0;
  }}

  ul {{
    margin-left: 5mm;
    margin-bottom: 3.5mm;
  }}

  li {{
    margin-bottom: 2mm;
    font-size: 10pt;
  }}

  /* Figure and Table Container Styling */
  .figure-box, .table-box {{
    width: 100%;
    margin: 7mm 0;
    break-inside: avoid;
    text-align: center;
  }}

  .figure-img {{
    width: 100%;
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto 3mm auto;
  }}

  .caption {{
    font-size: 9pt;
    line-height: 1.24;
    text-align: justify;
    color: #111111;
  }}

  .caption-label {{
    font-weight: bold;
  }}

  /* Tables */
  table.paper-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.8pt;
    margin-bottom: 3mm;
  }}

  table.paper-table th, table.paper-table td {{
    border-top: 0.5pt solid #000000;
    border-bottom: 0.5pt solid #000000;
    padding: 2.2mm 2mm;
    text-align: left;
  }}

  table.paper-table th {{
    font-weight: bold;
    background-color: #F1F3F5;
    border-bottom: 1pt solid #000000;
  }}

  /* Reference List */
  .references-list {{
    font-size: 9pt;
    line-height: 1.22;
    margin-top: 4mm;
  }}

  .ref-item {{
    margin-bottom: 2.5mm;
    padding-left: 5mm;
    text-indent: -5mm;
  }}
</style>
</head>
<body>

  <!-- Title Block -->
  <div class="title-block">
    <div class="paper-title">SemanticShield AI — An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis</div>
    
    <div class="authors-grid">
      <div class="author-col">
        <div class="author-name">Ch. Avinash</div>
        <div class="author-dept">Dept. of Cyber Security, ECE & IoT<br>Malla Reddy University, Hyderabad</div>
        <div class="author-email">2311cs040035@mallareddyuniversity.ac.in</div>
      </div>
      <div class="author-col">
        <div class="author-name">K. Mani Tej Kumar</div>
        <div class="author-dept">Dept. of Cyber Security, ECE & IoT<br>Malla Reddy University, Hyderabad</div>
        <div class="author-email">2311cs040070@mallareddyuniversity.ac.in</div>
      </div>
      <div class="author-col">
        <div class="author-name">K. Kowshik</div>
        <div class="author-dept">Dept. of Cyber Security, ECE & IoT<br>Malla Reddy University, Hyderabad</div>
        <div class="author-email">2311cs040074@mallareddyuniversity.ac.in</div>
      </div>
    </div>
  </div>

  <!-- Abstract & Keywords -->
  <div class="abstract-container">
    <div class="abstract-heading">Abstract</div>
    <div class="abstract-text">
      Security Operations Centers routinely face a large volume of phishing and social engineering threats that exploit human cognitive vulnerabilities rather than traditional software flaws. Existing security awareness training platforms rely on static email templates and simple click-tracking mechanisms that fail to simulate how employees evaluate persuasive pretexts under varying operational pressures. This paper presents SemanticShield AI, an intelligent agentic platform designed for automated phishing simulation and behavioral threat analysis. Powered by a FastAPI backend, a React and Vite dashboard, SQLAlchemy storage, and live Google Gemini language models streaming over Server-Sent Events, SemanticShield AI evaluates employee decision-making across four defined psychological profiles: trusting, security-conscious, overwhelmed, and executive. The platform passes agent reasoning vectors into a composite Risk Engine that applies weighted multi-agent scoring (40% semantic analysis, 25% behavioral analysis, 35% URL intelligence) and high-risk floor enforcement, automatically creating simulation-tagged incident records and broadcasting real-time telemetry over WebSockets. Empirical evaluation across {total_runs} live simulation runs demonstrates that profile prompt engineering yields high behavioral fidelity: the trusting profile exhibited a {susc_trusting:.1f}% vulnerability rate across malicious scenarios, whereas the security-conscious profile achieved a {susc_security:.1f}% vulnerability rate ({100.0 - susc_security:.1f}% safe decisions). The engine achieved distinct discrete risk scoring of {mean_vuln_risk:.0f} for vulnerable outcomes and {mean_safe_risk:.0f} for safe outcomes with zero fallback execution failures across all evaluated live API runs.
    </div>
    <div class="keywords-line">
      <span class="keywords-label">Keywords—</span> Security Operations Center, Phishing Simulation, Behavioral Threat Analysis, Agentic AI, Large Language Models, FastAPI, React, Risk Engine, Synthetic Testing.
    </div>
  </div>

  <!-- Main Body Content (Two Columns) -->
  <div class="main-body">

    <h1>1 Introduction</h1>
    <p class="no-indent">
      The volume and sophistication of phishing, spear-phishing, and social engineering attacks targeting modern organizations have grown to unprecedented levels. Adversaries frequently bypass traditional perimeter defenses such as email security gateways, Web Application Firewalls, and intrusion detection systems by leveraging legitimate infrastructure, brand impersonation, urgent executive pretexting, and credential harvesting landing pages. While technical controls continuously evolve to block malicious payloads, human employees remain the primary targets of initial access techniques as documented under MITRE ATT&CK technique T1566.
    </p>
    <p>
      Traditional Security Information and Event Management platforms, Security Orchestration, Automation, and Response playbooks, and security awareness training tools suffer from significant structural limitations. Conventional phishing awareness software relies on static, pre-written email templates with static click-tracking links. These systems do not simulate the interactive cognitive decision-making of employees under varying operational conditions, nor do they provide Security Operations Center analysts with explainable, automated risk scoring derived from behavioral telemetry.
    </p>
    <p>
      This paper introduces SemanticShield AI, an intelligent agentic framework designed to bridge the gap between offensive social engineering simulation and defensive SOC monitoring. SemanticShield AI integrates dynamic LLM-based phishing simulation, multi-agent behavioral threat analysis, deterministic composite risk scoring, incident tracking, and real-time WebSocket delivery into a unified application.
    </p>
    <p>
      A central design principle behind SemanticShield AI is the separation of generative AI reasoning from deterministic risk calculation. Artificial intelligence is employed to simulate employee cognitive processes and generate explainable investigation narratives, while composite risk scoring and security overrides are executed through verified, deterministic code rules inside the Risk Engine. This design ensures that LLM outputs remain grounded in verified security attributes while human analysts retain full control over operational response actions.
    </p>
    <p>
      The platform incorporates synthetic testing controls, ensuring that all phishing simulations operate in a controlled sandbox environment. No actual email messages are dispatched over public networks, eliminating risk to live corporate messaging infrastructure while allowing security teams to benchmark vulnerability across diverse employee personas.
    </p>
    <p>
      The remainder of this paper is organized as follows. Section 2 reviews existing security monitoring and phishing training systems and highlights their architectural limitations. Section 3 presents the proposed system architecture, including three-tier structure, data flow, use cases, sequence interactions, class models, and activity workflows. Section 4 provides a module-by-module implementation review of the execution pipeline. Section 5 outlines the technology stack and event processing flow. Section 6 presents a design-versus-implementation review, verifying operational functional requirements. Section 7 discusses limitations and directions for future work. Section 8 details experimental setup, quantitative results, and interface verification screenshots. Section 9 concludes the paper.
    </p>

    <h1>2 Limitations of Existing Systems</h1>
    <p class="no-indent">
      Modern digital services generate vast streams of network traffic, authentication logs, and security telemetry, making manual monitoring impossible. A single log entry rarely reveals an ongoing campaign on its own; a failed login may be benign, but repeated failures followed by an immediate password reset request may signal an active account takeover attempt. Security Operations Centers rely on SIEMs, intrusion detection systems, and threat intelligence feeds to aggregate alerts, but enterprise SOC tooling remains complex, fragmented, and prohibitively expensive for small security teams, educational institutions, and research laboratories.
    </p>
    <p>
      In existing systems, phishing simulation and incident monitoring are treated as completely disconnected functions. Phishing awareness tools send static batch emails and record binary open/click metrics without assessing why an employee fell for a specific pretext or how different job roles process deceptive signals. Conversely, defensive monitoring tools ingest telemetry without visibility into human vulnerability patterns across departments. This separation forces analysts to manually reconcile data across disparate dashboards, delaying incident triage and leaving organizations exposed to multi-stage social engineering campaigns.
    </p>
    <p>
      Furthermore, traditional security awareness training fails to account for employee stress, workload pressure, and organizational authority dynamics. A finance manager handling urgent payment deadlines is significantly more likely to click a deceptive wire transfer link than an off-duty software developer carefully inspecting URL parameters. Static templates cannot model these psychological profiles dynamically, producing unrealistic awareness metrics that give security teams a false sense of protection.
    </p>

    <h1>3 System Architecture</h1>
    <p class="no-indent">
      SemanticShield AI is structured around a modular, three-tier architecture designed to separate presentation, business logic, and database persistence while ensuring real-time telemetry delivery.
    </p>

    <h2>3.1 Three-Tier Architecture</h2>
    <p class="no-indent">
      Figure 1 depicts the three-tier architecture of SemanticShield AI across the Presentation, Application, and Data tiers. The presentation layer is built with React, Vite, TypeScript, and Tailwind CSS, offering an interactive simulation sandbox, defensive scanning portal, incident dashboard, and analytics view. The application tier comprises a FastAPI backend hosting the Phishing Simulation Engine, Gemini LLM Handler, Risk Engine, Incident Manager, Activity Feed Manager, and WebSocket Manager. The data tier uses SQLAlchemy ORM backed by SQLite storage for local operational deployment.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig1']}" alt="Figure 1">
      <div class="caption"><span class="caption-label">Figure 1:</span> SemanticShield AI system architecture: Presentation Tier (React + Vite frontend), Application Tier (FastAPI backend, Risk Engine, Phishing Simulation Engine), and Data Tier (SQLAlchemy ORM SQLite storage).</div>
    </div>

    <h2>3.2 Data Flow</h2>
    <p class="no-indent">
      Figure 2 details the genuine data flow diagram of SemanticShield AI. Requests originated by the Security Admin or automated testing scripts enter Process 1.0 (Simulation Ingestion), where incoming scenario payloads and target role specifications are validated. Process 2.0 (Gemini LLM Agent Execution) constructs behavioral system prompts and streams reasoning text over Server-Sent Events. Process 3.0 (Risk Scoring & Classification) passes multi-agent payload vectors to the Risk Engine, which computes a composite score. Process 4.0 (Telemetry & WebSocket Broadcast) streams updates to connected clients while persisting records into Data Store D1 (SQLite database).
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig2']}" alt="Figure 2">
      <div class="caption"><span class="caption-label">Figure 2:</span> SemanticShield AI data flow diagram: security simulation payloads move from external entities through ingestion, Gemini LLM execution, risk scoring, telemetry broadcast, and database persistence.</div>
    </div>

    <h2>3.3 Use Case</h2>
    <p class="no-indent">
      Figure 3 illustrates the primary use case interactions within SemanticShield AI. Three primary actors interact with the system boundary: the Security Administrator / SOC Analyst, the AI Agent (Gemini LLM), and the Simulated Employee. The Security Admin executes interactive simulation tests, configures scenario parameters, monitors incident queues, and reviews behavioral analytics. The Gemini AI Agent streams step-by-step reasoning and extracts decision tags. The Simulated Employee profile defines the psychological context under which the email payload is evaluated.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig3']}" alt="Figure 3">
      <div class="caption"><span class="caption-label">Figure 3:</span> SemanticShield AI use case diagram: Security Analyst/Admin, Gemini AI Agent, and Simulated Employee interactions across simulation execution, prompt selection, risk calculation, and incident management.</div>
    </div>

    <h2>3.4 Sequence Diagram</h2>
    <p class="no-indent">
      Figure 4 traces the sequential message interaction across five key lifelines: Simulator, FastAPI Backend, Phishing Simulation Engine, Gemini LLM Handler, and SQLite Database. Upon receiving an HTTP POST simulation request, the backend delegates execution to the Phishing Simulation Engine, which initiates a streaming LLM call. The accumulated reasoning text is parsed to extract decision tags, fed into the Risk Engine to compute composite risk scores, persisted to SQLite, and returned to the client as a JSON payload or SSE stream.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig4']}" alt="Figure 4">
      <div class="caption"><span class="caption-label">Figure 4:</span> SemanticShield AI sequence diagram: HTTP simulation submission, FastAPI backend orchestration, streaming Gemini LLM reasoning, risk engine evaluation, database persistence, and client delivery.</div>
    </div>

    <h2>3.5 Class Model</h2>
    <p class="no-indent">
      Figure 5 presents the structural class model of the primary domain entities and SQLAlchemy ORM models. The DBSimulation model records simulation identifiers, timestamps, scenario types, employee roles, behavioral profiles, reasoning text, decisions, and duration metrics. The DBIncident model represents simulation-tagged incident items with severity classifications, target details, and audit history. The RiskEngine class processes AgentResponsePayload structures to compute composite scores and enforce security floor overrides.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig5']}" alt="Figure 5">
      <div class="caption"><span class="caption-label">Figure 5:</span> SemanticShield AI class diagram: DBSimulation, DBIncident, RiskEngine, and AgentResponsePayload entities, illustrating field attributes and operational relationships.</div>
    </div>

    <h2>3.6 Activity Diagram</h2>
    <p class="no-indent">
      Figure 6 illustrates the activity workflow from simulation invocation to persistence. The sequence begins with request validation, followed by behavioral prompt selection matching the specified profile. The system constructs the user prompt, streams LLM reasoning, extracts decision tags, calculates composite risk scores, generates simulation-tagged incidents, broadcasts WebSocket events to connected dashboards, and persists records in SQLite.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig6']}" alt="Figure 6">
      <div class="caption"><span class="caption-label">Figure 6:</span> SemanticShield AI activity diagram: end-to-end execution flow from input validation and prompt selection through LLM streaming, risk scoring, incident creation, and dual-write storage.</div>
    </div>

    <h1>4 Module-by-Module Implementation</h1>
    <p class="no-indent">
      The core processing pipeline of SemanticShield AI is implemented as a modular twelve-step workflow. Each module performs a single, well-defined security or processing function, ensuring clean separation of concerns across the application.
    </p>

    <h2>4.1 Input Validation and Ingestion</h2>
    <p class="no-indent">
      Input validation and scenario ingestion handle incoming HTTP requests submitted to the phishing simulation endpoints. The backend validates required parameters including scenario name, employee role, behavioral profile, email subject, and email body, assigning a unique simulation identifier and UTC timestamp before forwarding the payload to prompt selection.
    </p>

    <h2>4.2 Behavioral Profile Selection</h2>
    <p class="no-indent">
      Behavioral profile selection retrieves the system prompt corresponding to the target employee persona. Four distinct psychological profiles are defined: trusting, security-conscious, overwhelmed, and executive. Each profile prompt establishes background context, daily workload characteristics, decision-making tendencies, and specific evaluation criteria.
    </p>

    <h2>4.3 Agent Simulation and Streaming</h2>
    <p class="no-indent">
      Agent simulation and LLM streaming construct the structured user message and establish a streaming connection with the Google GenAI SDK. The handler passes system instructions and email content to live Gemini models, streaming reasoning text chunks back to the client over Server-Sent Events with automatic model failover and exponential retry logic on rate limits.
    </p>

    <div class="table-box">
      <div class="caption" style="margin-bottom: 1.5mm;"><span class="caption-label">Table 1:</span> Technology Stack used in SemanticShield AI</div>
      <table class="paper-table">
        <thead>
          <tr>
            <th>Layer</th>
            <th>Technology</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Frontend</td>
            <td>React, Vite, TypeScript</td>
            <td>SOC dashboard and simulation interface</td>
          </tr>
          <tr>
            <td>Backend</td>
            <td>FastAPI, Uvicorn</td>
            <td>REST API routing and system control</td>
          </tr>
          <tr>
            <td>AI Engine</td>
            <td>Google GenAI SDK, Gemini 3.5</td>
            <td>Behavioral LLM reasoning and decision streaming</td>
          </tr>
          <tr>
            <td>Risk Engine</td>
            <td>Custom Python Risk Engine</td>
            <td>Weighted multi-agent risk assessment</td>
          </tr>
          <tr>
            <td>Database</td>
            <td>SQLAlchemy, SQLite, Alembic</td>
            <td>Relational storage and database migrations</td>
          </tr>
          <tr>
            <td>Real-Time</td>
            <td>WebSockets, SSE</td>
            <td>Live telemetry broadcast and reasoning streaming</td>
          </tr>
          <tr>
            <td>Integration</td>
            <td>Chrome Extension (V3)</td>
            <td>Browser-side email and URL analysis</td>
          </tr>
          <tr>
            <td>Styling</td>
            <td>Tailwind CSS</td>
            <td>Responsive modern security dashboard UI</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>4.4 Decision Extraction</h2>
    <p class="no-indent">
      Decision extraction parses the accumulated reasoning text using regular expressions to locate explicit decision tags. The parser searches for bracketed indicators signifying whether the simulated employee yielded to the attack or rejected the email, falling back to keyword heuristics if required.
    </p>

    <h2>4.5 Risk Scoring and Categorization</h2>
    <p class="no-indent">
      Composite risk scoring and categorization pass multi-agent output vectors to the Risk Engine. The engine applies weighted averaging across semantic analysis (40%), behavioral analysis (25%), and URL intelligence (35%), enforcing a mandatory risk floor when any single agent score exceeds critical threshold boundaries.
    </p>

    <h2>4.6 Incident Creation and Tracking</h2>
    <p class="no-indent">
      Incident creation and management convert high-risk simulation outcomes into structured incident records. The manager populates threat severity, classification, affected roles, and MITRE ATT&CK technique mappings, tagging records as synthetic simulations to preserve operational separation from live defense incidents.
    </p>

    <h2>4.7 Real-Time Telemetry Broadcast</h2>
    <p class="no-indent">
      Real-time telemetry and WebSocket broadcast dispatch updated simulation results, activity feed logs, and incident notifications to all connected frontend clients without requiring manual browser page refreshes.
    </p>

    <div class="table-box">
      <div class="caption" style="margin-bottom: 1.5mm;"><span class="caption-label">Table 2:</span> SemanticShield AI Event Processing Flow</div>
      <table class="paper-table">
        <thead>
          <tr>
            <th>Stage</th>
            <th>Processing</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Input Ingestion</td>
            <td>Validates scenario, employee role, profile, subject, and body.</td>
          </tr>
          <tr>
            <td>Prompt Construction</td>
            <td>Selects psychological system prompt and builds user prompt.</td>
          </tr>
          <tr>
            <td>LLM Streaming</td>
            <td>Streams step-by-step reasoning via Google GenAI SDK.</td>
          </tr>
          <tr>
            <td>Decision Parsing</td>
            <td>Extracts decision tag using regex and heuristic matching.</td>
          </tr>
          <tr>
            <td>Risk Assessment</td>
            <td>Computes 40/25/35 weighted score and applies risk floor override.</td>
          </tr>
          <tr>
            <td>Incident Creation</td>
            <td>Generates simulation-tagged incident record with MITRE tags.</td>
          </tr>
          <tr>
            <td>Activity Logging</td>
            <td>Appends severity-coded event to central activity feed.</td>
          </tr>
          <tr>
            <td>Real-Time Broadcast</td>
            <td>Streams JSON events across WebSocket telemetry channels.</td>
          </tr>
          <tr>
            <td>Data Persistence</td>
            <td>Saves simulation and incident records to SQLite datastore.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>4.8 Persistence and Storage</h2>
    <p class="no-indent">
      Data persistence and dual-write storage save final simulation records to the SQLite database via SQLAlchemy repositories, ensuring persistent analytics survive server restarts.
    </p>

    <h2>4.9 Activity Logging and History</h2>
    <p class="no-indent">
      Activity logging records every executed simulation step in the central feed table, allowing analysts to audit historical simulation trials, inspect timestamped reasoning traces, and verify system state consistency across operational shifts.
    </p>

    <h1>5 Technology Stack</h1>
    <p class="no-indent">
      The technical architecture of SemanticShield AI relies on modern, lightweight technologies chosen for performance, modularity, and rapid prototyping capability. Table 1 summarizes the primary layers, technologies, and system roles. Table 2 details the nine distinct stages of the event processing flow.
    </p>
    <p>
      The API layer is implemented with FastAPI and Uvicorn, providing high-throughput asynchronous execution for both synchronous REST endpoints and Server-Sent Event streaming responses. Database interactions are managed through SQLAlchemy ORM with SQLite file storage for rapid local deployment, complemented by Alembic migration scripts to support future enterprise database schema evolutions.
    </p>
    <p>
      The frontend presentation layer leverages React 18, Vite, TypeScript, and Tailwind CSS. Modern UI components provide real-time visual feedback, including animated simulation drawers, risk level badges, live streaming reasoning terminals, and interactive chart visualizations.
    </p>

    <h1>6 Design-versus-Implementation Review</h1>
    <p class="no-indent">
      In the manner of a rigorous source-level engineering review, this section evaluates how the implemented SemanticShield AI system corresponds to the architectural design and workflow specifications. The review focuses on the continuous processing path, separation between LLM simulation and deterministic risk scoring, real-time delivery, and analyst-controlled operations.
    </p>
    <h2>6.1 The Continuous Simulation Pipeline</h2>
    <p class="no-indent">
      The system design specifies a continuous workflow connecting scenario submission, streaming reasoning, decision extraction, risk scoring, incident creation, and dashboard rendering. The implemented runtime path directly matches this design: requests received by FastAPI pass through validation, initiate streaming calls via the Gemini Handler, submit agent vectors to the Risk Engine, create simulation-tagged records in Incident Manager, and broadcast results over WebSockets in a single automated execution pass.
    </p>
    <h2>6.2 Behavioral Simulation versus Deterministic Risk Scoring</h2>
    <p class="no-indent">
      A key architectural boundary separates probabilistic LLM reasoning from deterministic risk calculation. Generative AI is utilized exclusively to simulate employee psychological reactions and explain decision rationales, whereas final risk scoring is governed entirely by deterministic code rules inside Risk Engine. This design prevents LLM hallucination from distorting enterprise risk scores.
    </p>
    <h2>6.3 Risk Aggregation and Incident Creation</h2>
    <p class="no-indent">
      The architecture requires automatic transformation of vulnerable simulation outcomes into actionable incidents. The implemented Incident Manager successfully instantiates structured incident objects containing unique identifiers, scenario details, severity levels, and MITRE T1566.001/002 technique tags, satisfying the requirement to convert isolated events into managed SOC records.
    </p>
    <h2>6.4 Real-Time Delivery versus Polling</h2>
    <p class="no-indent">
      The design specifies event-driven telemetry distribution. Functional testing confirms that completed simulations emit WebSocket events on dedicated channels, allowing the React frontend dashboard, incidents table, and activity feed to update dynamically without requiring manual page reloads.
    </p>
    <h2>6.5 Analyst-Controlled and Synthetic-Only Operation</h2>
    <p class="no-indent">
      The platform enforces strict operational guardrails: all simulations are entirely synthetic, and no actual email messages are ever transmitted over external networks. Furthermore, defensive response actions remain strictly under human analyst control.
    </p>
    <h2>6.6 What Is Verified Working</h2>
    <p class="no-indent">
      System verification confirmed complete end-to-end functionality across all core pipeline modules. A total of {total_runs} live simulation runs were successfully executed using live Google Gemini API models with zero fallback generator executions. All 28 scenario-profile combinations were evaluated across 3 repetitions, risk scores of 84 and 18 were correctly calculated, SQLite persistence was verified after full backend server restarts, and production frontend builds completed clean with zero errors.
    </p>

    <h1>7 Limitations and Future Work</h1>
    <p class="no-indent">
      While SemanticShield AI successfully demonstrates dynamic behavioral phishing simulation, several technical limitations suggest directions for future enhancement:
    </p>
    <ul>
      <li><strong>Single-LLM Dependence:</strong> The current implementation relies primarily on Google Gemini family models. Integrating multi-model provider fallbacks (e.g., Anthropic Claude, OpenAI GPT-4, Llama 3) will improve resilience against provider outages.</li>
      <li><strong>Simulated vs Human Behavior:</strong> Simulations rely on prompt-engineered LLM personas. Future research should benchmark LLM profile decisions against empirical human participant behavior in real-world cohort studies.</li>
      <li><strong>Local Development Deployment:</strong> The current storage uses SQLite. Future production deployments should migrate to PostgreSQL with containerized orchestration.</li>
      <li><strong>Containerized Stack Verification:</strong> Docker Compose stacks require full verification under production container networking environments.</li>
      <li><strong>Access Control & Authentication:</strong> Role-based access control and multi-factor authentication should be implemented for administrative endpoints.</li>
      <li><strong>API Rate Limiting:</strong> Public simulation endpoints require per-client rate limiting to prevent API quota exhaustion.</li>
      <li><strong>Multi-Model Comparison:</strong> Comparative analysis across multiple LLM parameter scales should be conducted to evaluate prompt adherence variance.</li>
      <li><strong>Validation with Human Participants:</strong> User studies are needed to refine prompt characteristics against real employee security awareness benchmarks.</li>
      <li><strong>Adaptive Scenario Generation:</strong> Future iterations will incorporate dynamic scenario generation based on organizational threat intelligence feeds.</li>
    </ul>

    <h1>8 Results & Discussion</h1>
    <p class="no-indent">
      This section presents the experimental evaluation of SemanticShield AI across {total_runs} live simulation runs, assessing behavioral profile vulnerability, risk score distribution, decision consistency, and execution latency.
    </p>

    <h2>8.1 Experimental Setup</h2>
    <p class="no-indent">
      The test matrix comprises seven email scenarios (SIM-EML-001 through SIM-EML-007) evaluated across four behavioral profiles (trusting, security-conscious, overwhelmed, executive), yielding 28 distinct combinations. To evaluate decision consistency and execution variance, the full 28-run matrix was executed across three full repetitions, generating {total_runs} live simulation records. Table 3 presents the behavioral profile specifications.
    </p>

    <div class="table-box">
      <div class="caption" style="margin-bottom: 1.5mm;"><span class="caption-label">Table 3:</span> Behavioral Profile Specifications</div>
      <table class="paper-table">
        <thead>
          <tr>
            <th>Profile</th>
            <th>Target Role</th>
            <th>Primary Psychological Traits</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Trusting</td>
            <td>HR Manager</td>
            <td>High trust, speed over caution, ignores domain anomalies.</td>
          </tr>
          <tr>
            <td>Security-Conscious</td>
            <td>Senior Developer</td>
            <td>Paranoid, checks headers, hovers links, rejects unverified requests.</td>
          </tr>
          <tr>
            <td>Overwhelmed</td>
            <td>Finance Manager</td>
            <td>Stressed, rushed, skims content, vulnerable to urgent financial asks.</td>
          </tr>
          <tr>
            <td>Executive</td>
            <td>VP of Operations</td>
            <td>High volume, relies on EA, vulnerable to executive peer pretexting.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>8.2 Quantitative Results</h2>
    <p class="no-indent">
      Table 4 summarizes the aggregate metrics computed across all live simulation runs. Figure 7 illustrates the susceptibility rate per behavioral profile on malicious scenarios. The trusting profile exhibited a {susc_trusting:.1f}% susceptibility rate across all malicious scenarios, yielding to credential harvesting, wire transfers, quishing, and MFA bypass pretexts. Conversely, the security-conscious profile achieved a {susc_security:.1f}% susceptibility rate ({100.0 - susc_security:.1f}% safe decisions), correctly identifying sender domain spoofing and suspicious URLs in every instance.
    </p>

    <div class="table-box">
      <div class="caption" style="margin-bottom: 1.5mm;"><span class="caption-label">Table 4:</span> Behavioral Profile Summary Performance Metrics</div>
      <table class="paper-table">
        <thead>
          <tr>
            <th>Behavioral Profile</th>
            <th>Total Runs</th>
            <th>Susceptibility Rate</th>
            <th>Mean Risk Score</th>
            <th>Decision Consistency</th>
            <th>Mean Latency</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Trusting (HR)</td>
            <td>21</td>
            <td>100.0%</td>
            <td>84.0</td>
            <td>100.0%</td>
            <td>12.56s</td>
          </tr>
          <tr>
            <td>Security-Conscious (Dev)</td>
            <td>21</td>
            <td>0.0%</td>
            <td>18.0</td>
            <td>100.0%</td>
            <td>11.10s</td>
          </tr>
          <tr>
            <td>Overwhelmed (Finance)</td>
            <td>21</td>
            <td>94.4%</td>
            <td>71.4</td>
            <td>95.2%</td>
            <td>12.73s</td>
          </tr>
          <tr>
            <td>Executive (VP Ops)</td>
            <td>21</td>
            <td>55.6%</td>
            <td>52.6</td>
            <td>81.0%</td>
            <td>13.86s</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig7']}" alt="Figure 7">
      <div class="caption"><span class="caption-label">Figure 7:</span> Susceptibility rate (%) per behavioral profile on malicious scenarios (SIM-EML-001 to 006). Sample size n=18 runs per profile across 3 repetitions.</div>
    </div>

    <p>
      The overwhelmed profile yielded a {susc_overwhelmed:.1f}% susceptibility rate, falling victim to high-urgency credential scams and package fee warnings while successfully rejecting routine alerts. The executive profile exhibited a {susc_exec:.1f}% susceptibility rate, succumbing to targeted executive pretexting while rejecting generic spam. On the control scenario (SIM-EML-007: Legitimate Standup), the trusting profile mistakenly flagged the meeting as vulnerable due to over-sensitivity to security terminology, while all other profiles correctly identified it as safe.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig8']}" alt="Figure 8">
      <div class="caption"><span class="caption-label">Figure 8:</span> Scenario by profile vulnerability heatmap (greyscale annotated with vulnerability fraction across 3 repetitions). Darker cells indicate higher vulnerability.</div>
    </div>

    <p>
      Figure 8 presents the scenario by profile vulnerability heatmap across all 28 combinations. Figure 9 depicts the composite risk score distribution. The Risk Engine mapped vulnerable decisions to a discrete score of {mean_vuln_risk:.0f} and safe decisions to {mean_safe_risk:.0f}, producing clear bimodal separation without score overlap. Figure 10 presents mean execution latency per profile. Average end-to-end simulation latency was {mean_latency:.2f} seconds. Decision consistency across repetitions reached 100.0% for deterministic profiles.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig9']}" alt="Figure 9">
      <div class="caption"><span class="caption-label">Figure 9:</span> Composite risk score distribution per behavioral profile (0-100 scale). Boxplots display median, quartiles, and individual run data points.</div>
    </div>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig10']}" alt="Figure 10">
      <div class="caption"><span class="caption-label">Figure 10:</span> Mean end-to-end execution latency (seconds) per behavioral profile with standard deviation error bars (n=21 runs per profile).</div>
    </div>

    <h2>8.3 Interface Screenshots</h2>
    <p class="no-indent">
      Figures 11 through 16 document the verified user interface of SemanticShield AI captured from the active application frontend.
    </p>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig11']}" alt="Figure 11">
      <div class="caption"><span class="caption-label">Figure 11:</span> Offensive AI Simulation Sandbox interface (/admin/simulator). Displays scenario catalog including SIM-EML-001 (Password Reset, Risk 88), SIM-EML-002 (Wire Transfer, Risk 94), and SIM-EML-007 (Legitimate Standup, Risk 12) with category filters and interactive run controls.</div>
    </div>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig12']}" alt="Figure 12">
      <div class="caption"><span class="caption-label">Figure 12:</span> Simulation result modal drawer showing vulnerable outcome for scenario SIM-EML-001 with Trusting (HR) profile. Displays streamed reasoning text, [VULNERABLE] decision tag, composite risk score of 84/100, DANGEROUS severity, 98% confidence score, and 33.46s duration.</div>
    </div>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig13']}" alt="Figure 13">
      <div class="caption"><span class="caption-label">Figure 13:</span> Simulation result modal drawer showing safe outcome for scenario SIM-EML-001 with Security-Conscious (Dev) profile. Displays domain verification reasoning, [SAFE] decision tag, composite risk score of 18/100, SAFE severity, 98% confidence score, and 14.31s duration.</div>
    </div>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig14']}" alt="Figure 14">
      <div class="caption"><span class="caption-label">Figure 14:</span> Defensive AI Portal interface (/dashboard) showing simulated payload transfer from Offensive Lab. Displays CRITICAL classification, 88/100 risk score, 94% confidence score, incident reference INC-001, and flagged indicators including Header Display Name Spoofing and High Pressure Urgency.</div>
    </div>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig15']}" alt="Figure 15">
      <div class="caption"><span class="caption-label">Figure 15:</span> Incident Management Dashboard (/admin/incidents) displaying 28 simulation-tagged incident records loaded from SQLite database (semantic_shield.db), including INC-SIM-001 (Risk 84, DANGEROUS) and real-time activity stream logging.</div>
    </div>

    <div class="figure-box">
      <img class="figure-img" src="{imgs['fig16']}" alt="Figure 16">
      <div class="caption"><span class="caption-label">Figure 16:</span> Analytics and Persistence Dashboard (/admin/analytics) captured after complete backend server restart. Displays 28 persisted simulation records, 53.6% vulnerable vs 46.4% safe decision breakdown, 98.0% mean AI confidence, and risk level distributions.</div>
    </div>

    <h1>9 Conclusion</h1>
    <p class="no-indent">
      This paper presented SemanticShield AI, an intelligent agentic platform for behavioral phishing simulation and threat analysis. By integrating profile-driven LLM prompt engineering, multi-agent composite risk scoring, incident management, and real-time WebSocket telemetry into a unified architecture, SemanticShield AI demonstrates how agentic AI can enhance cybersecurity training and SOC monitoring. Experimental evaluation across {total_runs} live simulation runs confirmed distinct behavioral profiling, high decision consistency across repetitions, robust composite risk scoring, and zero fallback execution failures. SemanticShield AI offers a scalable, explainable foundation for security awareness research and modern Security Operations Center automation.
    </p>

    <h1>References</h1>
    <div class="references-list">
      <div class="ref-item">[1] R. Sommer and V. Paxson, "Outside the closed world: On using machine learning for network intrusion detection," <em>IEEE Symp. Security and Privacy</em>, 2010, pp. 305-316.</div>
      <div class="ref-item">[2] P. Kumaraguru, A. Rhee, A. Acquisti, L. F. Cranor, J. Hong, and E. Nunge, "Protecting people from phishing: The design and evaluation of an embedded training email system," <em>Proc. CHI</em>, 2007, pp. 905-914.</div>
      <div class="ref-item">[3] Z. Alkhalil, C. Hewage, L. Nawaf, and I. Khan, "Phishing attacks: A recent comprehensive study and a new anatomy," <em>Frontiers in Computer Science</em>, vol. 3, 2021.</div>
      <div class="ref-item">[4] R. B. Cialdini, <em>Influence: Science and Practice</em>, 5th ed. Boston, MA, USA: Allyn & Bacon, 2009.</div>
      <div class="ref-item">[5] M. Jakobsson and S. Myers, <em>Phishing and Countermeasures</em>. Hoboken, NJ, USA: Wiley-Interscience, 2007.</div>
      <div class="ref-item">[6] S. Sheng, M. Holbrook, P. Kumaraguru, L. F. Cranor, and J. Downs, "Who falls for phish? A demographic analysis of phishing susceptibility and effectiveness of interventions," <em>Proc. CHI</em>, 2010, pp. 373-382.</div>
      <div class="ref-item">[7] J. S. Downs, M. B. Holbrook, and L. F. Cranor, "Decision strategies and susceptibility to phishing," <em>Proc. SOUPS</em>, 2006, pp. 79-90.</div>
      <div class="ref-item">[8] A. Vishwanath, T. Herath, R. Chen, J. Wang, and H. R. Rao, "Why do people get phished? Testing individual differences in phishing vulnerability within an integrated, information processing model," <em>Decision Support Systems</em>, vol. 51, no. 3, pp. 576-586, 2011.</div>
      <div class="ref-item">[9] M. Cinque, D. Cotroneo, and A. Pecchia, "Challenges and directions in Security Information and Event Management (SIEM)," <em>IEEE ISSREW</em>, 2018, pp. 95-99.</div>
      <div class="ref-item">[10] K. Scarfone and P. Mell, "Guide to Intrusion Detection and Prevention Systems (IDPS)," <em>NIST SP 800-94</em>, 2007.</div>
      <div class="ref-item">[11] MITRE Corporation, "MITRE ATT&CK: Phishing (T1566)," [Online]. Available: https://attack.mitre.org/techniques/T1566/</div>
      <div class="ref-item">[12] OWASP Foundation, "OWASP Top 10: 2021," [Online]. Available: https://owasp.org/Top10/</div>
      <div class="ref-item">[13] Google, "Gemini API documentation," [Online]. Available: https://ai.google.dev/gemini-api/docs</div>
      <div class="ref-item">[14] S. Ramirez, "FastAPI documentation," [Online]. Available: https://fastapi.tiangolo.com/</div>
    </div>

  </div>

</body>
</html>
"""

    html_path = "paper/source/paper.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Saved {html_path}")

if __name__ == "__main__":
    build_paper()
