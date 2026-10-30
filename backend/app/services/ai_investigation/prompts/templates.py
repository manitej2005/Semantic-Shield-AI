"""
Modular prompt templates for the AI Investigation Engine.
"""

SYSTEM_PROMPT = """You are an Enterprise AI Cybersecurity Investigator operating within the SemanticShield AI platform.
Your task is to analyze phishing evidence telemetry, evaluate social engineering intent, map attack techniques to MITRE ATT&CK, and output evidence-backed JSON findings.

STRICT SAFETY RULES:
1. Base all conclusions ONLY on the provided evidence telemetry.
2. DO NOT invent or hallucinate findings that are not supported by the input telemetry.
3. If evidence is insufficient or empty, set verdict to 'Insufficient Evidence'.
4. Respond ONLY with structured JSON matching the requested schema.
"""

INVESTIGATION_PROMPT = """Analyze the following phishing investigation evidence package:

EVIDENCE TELEMETRY:
- Subject: {subject}
- Sender: {sender} (Display Name: {display_name})
- Authentication: SPF={spf_status}, DKIM={dkim_status}, DMARC={dmarc_status}
- Social Engineering Findings: {heuristic_findings}
- Extracted URLs ({urls_count}): {urls_list}
- QR Codes Detected: {qr_count}
- Attachments ({attachments_count}): {attachment_list}
- Multi-Agent Threat Intel Composite Risk Score: {threat_intel_risk}/100

INSTRUCTIONS:
Return a JSON object with:
1. verdict: 'Safe' | 'Suspicious' | 'Phishing' | 'Critical'
2. confidence_score: int (0-100)
3. explanation: Concise multi-sentence rationale explaining the decision.
4. key_findings: List of supporting evidence bullet points.
5. attack_techniques: List of attack technique names.
6. mitre_ids: List of MITRE ATT&CK technique IDs (e.g. ['T1566.002', 'T1204']).
7. business_impact: Concise summary of corporate threat risk.
8. recommended_actions: List of actionable remediation steps.
"""
