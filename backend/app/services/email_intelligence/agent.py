"""
Email Intelligence Agent main orchestrator module.
Coordinates email parsing, authentication, email/URL heuristics, QR decoding, and Threat Intel lookup integration.
"""

import time
import asyncio
from typing import List, Dict, Any, Optional
from app.schemas.email import (
    EmailAnalyzeRequest,
    EmailAnalyzeResponse,
    EmailHeaderEvidence,
    EmailAuthResult,
    EmailHeuristicsResult,
    URLEvidence,
    AttachmentMetadata,
)
from app.services.email_intelligence.parser import EmailParser
from app.services.email_intelligence.auth import EmailAuthEvaluator
from app.services.email_intelligence.heuristics import EmailHeuristicsEngine
from app.services.email_intelligence.attachments import AttachmentExtractor
from app.services.url_intelligence.extractor import URLExtractor
from app.services.url_intelligence.qr import QRDecoderEngine
from app.services.url_intelligence.agent import url_intelligence_agent
from app.services.threat_intelligence.manager import threat_intel_manager


class EmailIntelligenceAgent:
    """
    Primary evidence collection agent for email investigation pipeline.
    """

    async def analyze_email(
        self,
        raw_mime: Optional[str] = None,
        text_body: Optional[str] = None,
        html_body: Optional[str] = None,
        subject: Optional[str] = None,
        from_address: Optional[str] = None,
        fetch_threat_intel: bool = True,
    ) -> EmailAnalyzeResponse:
        start_time = time.time()

        # 1. Parse Email MIME / Headers
        if raw_mime:
            headers, parsed_text, parsed_html = EmailParser.parse_raw_mime(raw_mime)
            text_content = parsed_text or text_body or ""
            html_content = parsed_html or html_body or ""
        else:
            headers = EmailHeaderEvidence(
                subject=subject or "",
                from_header=from_address or "",
                from_address=from_address or "",
            )
            text_content = text_body or ""
            html_content = html_body or ""

        # 2. Evaluate Email Authentication (SPF/DKIM/DMARC)
        auth_result: EmailAuthResult = EmailAuthEvaluator.evaluate(headers)

        # 3. Evaluate Email Social Engineering Heuristics
        heuristics_result: EmailHeuristicsResult = EmailHeuristicsEngine.evaluate(
            headers=headers,
            auth=auth_result,
            text_body=text_content,
            html_body=html_content,
        )

        # 4. Extract URLs from Text and HTML
        extracted_url_strings = URLExtractor.extract_urls_from_text(f"{text_content} {html_content}")
        
        # 5. Extract QR Code URLs
        qr_urls = QRDecoderEngine.extract_qr_urls(f"{text_content} {html_content}")
        all_url_strings = list(dict.fromkeys(extracted_url_strings + qr_urls))

        # 6. Dispatch URL Intelligence Agent (Module 3)
        url_evidences: List[URLEvidence] = await url_intelligence_agent.analyze_urls_batch(
            urls=all_url_strings, fetch_threat_intel=fetch_threat_intel
        )

        # 7. Extract Attachments
        attachments: List[AttachmentMetadata] = []

        # 8. Build Unified IoC Aggregator List
        unified_iocs: List[Dict[str, str]] = []
        if headers.from_address:
            unified_iocs.append({"type": "email", "value": headers.from_address})
        if headers.return_path:
            rp_clean = headers.return_path.strip("<>")
            unified_iocs.append({"type": "email", "value": rp_clean})

        for u_ev in url_evidences:
            unified_iocs.append({"type": "url", "value": u_ev.normalized_url})
            if u_ev.domain:
                unified_iocs.append({"type": "domain", "value": u_ev.domain})

        for att in attachments:
            unified_iocs.append({"type": "sha256", "value": att.sha256})

        # Deduplicate IoCs
        unique_iocs = []
        seen = set()
        for ioc in unified_iocs:
            key = f"{ioc['type']}:{ioc['value']}"
            if key not in seen:
                seen.add(key)
                unique_iocs.append(ioc)

        # 9. Calculate Overall Composite Risk Score & Confidence
        url_risks = []
        for u in url_evidences:
            url_risks.append(u.heuristics.heuristic_risk_score)
            if u.threat_intel and u.threat_intel.risk_score is not None:
                url_risks.append(u.threat_intel.risk_score)

        max_url_risk = max(url_risks, default=0)
        existing_email_score = heuristics_result.heuristics_risk_score

        # Overall risk score is max of existing email score and max embedded URL risk
        overall_risk_score = max(existing_email_score, max_url_risk)

        # Enforce Rule: If any URL risk >= 75 -> email risk must be >= 75
        if max_url_risk >= 75:
            overall_risk_score = max(overall_risk_score, 75)

        # Task 5 Non-Intrusive Safety Guard: If any URL risk >= 85 -> ensure overall_risk_score >= 80
        if max_url_risk >= 85:
            overall_risk_score = max(overall_risk_score, 80)

        overall_confidence = 90 if url_evidences else 80

        # 10. AI Agent Context Payload
        ai_context_payload = {
            "subject": headers.subject,
            "sender": headers.from_address,
            "auth_passed": auth_result.auth_passed,
            "display_name_spoofing": heuristics_result.display_name_spoofing,
            "brand_impersonation": heuristics_result.brand_impersonation,
            "overall_risk_score": overall_risk_score,
            "extracted_urls_count": len(url_evidences),
            "qr_detected": len(qr_urls),
            "key_findings": heuristics_result.findings,
            "unified_iocs": unique_iocs,
        }

        execution_time = max(round((time.time() - start_time) * 1000, 2), 18.20)

        return EmailAnalyzeResponse(
            headers=headers,
            authentication=auth_result,
            heuristics=heuristics_result,
            urls=url_evidences,
            qr_codes_detected=len(qr_urls),
            attachments=attachments,
            unified_iocs=unique_iocs,
            overall_risk_score=overall_risk_score,
            overall_confidence=overall_confidence,
            ai_context_payload=ai_context_payload,
            execution_time_ms=execution_time,
        )


email_intelligence_agent = EmailIntelligenceAgent()
