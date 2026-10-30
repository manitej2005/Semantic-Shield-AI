"""
Google Gemini LLM Adapter for live AI Investigation reasoning.
"""

import json
import logging
from typing import Dict, Any
from app.core.config import settings
from app.services.ai_investigation.adapters.base import BaseLLMAdapter
from app.services.ai_investigation.adapters.mock_adapter import MockLLMAdapter
from app.services.ai_investigation.prompts.templates import SYSTEM_PROMPT, INVESTIGATION_PROMPT

logger = logging.getLogger("app.services.ai_investigation")


class GeminiLLMAdapter(BaseLLMAdapter):
    """
    Live Google Gemini LLM reasoning adapter with Mock fallback when API key is unconfigured.
    """

    def __init__(self):
        super().__init__(
            model_name="gemini-2.5-pro",
            api_key=settings.GEMINI_API_KEY,
        )
        self.mock_fallback = MockLLMAdapter()

    async def investigate(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        if settings.THREAT_INTEL_MOCK_MODE or not self.api_key:
            logger.info("[GeminiAdapter] Using MockLLMAdapter (Mock Mode active or API key unconfigured)")
            return await self.mock_fallback.investigate(evidence)

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                system_instruction=SYSTEM_PROMPT,
            )

            prompt = INVESTIGATION_PROMPT.format(
                subject=evidence.get("subject", ""),
                sender=evidence.get("sender", ""),
                display_name=evidence.get("display_name", ""),
                spf_status=evidence.get("spf_status", "None"),
                dkim_status=evidence.get("dkim_status", "None"),
                dmarc_status=evidence.get("dmarc_status", "None"),
                heuristic_findings=", ".join(evidence.get("key_findings", [])),
                urls_count=evidence.get("extracted_urls_count", 0),
                urls_list=str(evidence.get("unified_iocs", [])),
                qr_count=evidence.get("qr_detected", 0),
                attachments_count=0,
                attachment_list="[]",
                threat_intel_risk=evidence.get("overall_risk_score", 0),
            )

            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"},
            )

            raw_text = response.text
            parsed_json = json.loads(raw_text)
            return parsed_json

        except Exception as exc:
            logger.warning(f"[GeminiAdapter] Live Gemini call failed ({exc}). Falling back to MockLLMAdapter.")
            return await self.mock_fallback.investigate(evidence)
