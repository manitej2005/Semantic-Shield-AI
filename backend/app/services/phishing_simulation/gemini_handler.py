"""
Gemini Handler for Phishing Simulation Agent.
Handles streaming Gemini API calls, retry logic with exponential backoff,
decision extraction ([VULNERABLE] or [SAFE]), threat scoring, and AgentResponsePayload creation.
"""

import os
import re
import time
import asyncio
import logging
from typing import AsyncGenerator, Dict, Any, List, Optional, Tuple
from app.core.config import settings
from app.domain.models.response import AgentResponsePayload

logger = logging.getLogger("app.services.phishing_simulation.gemini_handler")


class GeminiSimulationHandler:
    """
    Handles streaming Gemini LLM execution and response processing for Phishing Simulation.
    """

    def __init__(self, api_key: Optional[str] = None):
        resolved_key = api_key or os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        self._api_key = (resolved_key or "").strip().strip('"').strip("'")
        self._client = None
        self._has_valid_key = False
        self._initialize_client()

    def _initialize_client(self):
        invalid_placeholders = ["paste_your_api_key_here", "placeholder", "aizasy_placeholder"]
        key = self._api_key
        if key and not any(p in key.lower() for p in invalid_placeholders) and len(key) > 10:
            self._has_valid_key = True
            try:
                from google import genai  # type: ignore[import]
                self._client = genai.Client(api_key=key)
                logger.info("[GeminiSimulationHandler] Google GenAI SDK client initialized successfully.")
            except Exception as exc:
                logger.warning(f"[GeminiSimulationHandler] GenAI SDK init error: {exc}. Will use fallback engine.")
                self._has_valid_key = False
        else:
            logger.info("[GeminiSimulationHandler] No valid Gemini API key configured. Using intelligent mock streaming engine.")
            self._has_valid_key = False

    def build_user_message(self, employee_role: str, behavior_profile: str, email_subject: str, email_body: str) -> str:
        """
        Constructs the structured user message for the simulation agent.
        """
        return f"""You are a {employee_role} with {behavior_profile} personality characteristics.

You just received this email:
Subject: {email_subject}
Body: {email_body}

Analyze this email thinking out loud. What signals do you notice? Would you:
- Open the email?
- Click the link?
- Enter credentials?
- Forward to colleagues?

Respond as if you're making this decision right now. Think step-by-step.
Include your reasoning about risks you notice (even if you dismiss them).

Format: Use bullet points.
End with your final decision on a new line: [VULNERABLE] (if you would click the link or enter credentials) or [SAFE] (if you would not click the link, ignore, or report the email)."""

    async def stream_simulation_response(
        self, system_prompt: str, user_message: str, max_retries: int = 1
    ) -> AsyncGenerator[str, None]:
        """
        Streams simulation response chunks from Gemini API with retry logic.
        Falls back to realistic streaming if API fails, times out, or key is missing.
        """
        if self._has_valid_key and self._client:
            models_to_try = [
                "gemini-3.5-flash-lite",
                "gemini-3.5-flash",
                "gemini-3.8-flash",
                "gemini-3.6-flash",
                "gemini-flash-latest",
            ]
            
            for model_name in models_to_try:
                for attempt in range(max_retries + 2):
                    try:
                        logger.info(f"[GeminiSimulationHandler] Requesting stream from model '{model_name}' (attempt {attempt + 1})...")
                        full_prompt = f"System Instruction:\n{system_prompt}\n\nTask:\n{user_message}"
                        
                        def _get_stream():
                            return self._client.models.generate_content_stream(
                                model=model_name,
                                contents=full_prompt,
                            )

                        response_stream = await asyncio.wait_for(asyncio.to_thread(_get_stream), timeout=15.0)
                        chunk_count = 0

                        def _get_next_chunk(it):
                            try:
                                return next(it)
                            except StopIteration:
                                return None

                        it = iter(response_stream)
                        while True:
                            chunk = await asyncio.to_thread(_get_next_chunk, it)
                            if chunk is None:
                                break
                            text = getattr(chunk, "text", "") or ""
                            if text:
                                chunk_count += 1
                                yield text
                                
                        if chunk_count > 0:
                            logger.info(f"[GeminiSimulationHandler] Stream complete from '{model_name}' ({chunk_count} chunks).")
                            return

                    except Exception as exc:
                        logger.warning(f"[GeminiSimulationHandler] Stream attempt on '{model_name}' failed/timed out: {exc}")
                        if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc) or "503" in str(exc) or "UNAVAILABLE" in str(exc):
                            await asyncio.sleep(2.0 * (attempt + 1))
                            continue
                        break

        # Fallback Stream for fast local simulation execution
        logger.info("[GeminiSimulationHandler] Executing fallback streaming agent...")
        async for chunk in self._generate_fallback_stream(user_message, system_prompt):
            yield chunk
        async for chunk in self._generate_fallback_stream(user_message, system_prompt):
            yield chunk

    async def _generate_fallback_stream(self, user_message: str, system_prompt: str) -> AsyncGenerator[str, None]:
        """
        Generates contextual reasoning stream when Gemini API is offline or unconfigured.
        """
        is_trusting = "trusting" in system_prompt.lower()
        is_security = "security_conscious" in system_prompt.lower()
        is_overwhelmed = "overwhelmed" in system_prompt.lower()
        is_exec = "executive" in system_prompt.lower()

        lower_msg = user_message.lower()
        has_phish_signals = any(kw in lower_msg for kw in ["urgent", "verify", "password", "expire", "wire", "login", "bank", "mfa", "click"])

        if is_security:
            vulnerable = False
        elif is_trusting:
            vulnerable = has_phish_signals
        elif is_overwhelmed:
            vulnerable = has_phish_signals
        elif is_exec:
            vulnerable = "urgent" in lower_msg or "wire" in lower_msg or "login" in lower_msg
        else:
            vulnerable = has_phish_signals

        chunks = [
            "• Scanning incoming email headers and subject line...\n",
            f"• Sender domain and branding evaluated against expected profile behavior.\n",
            "• Analyzing email body for urgency markers, credential requests, or unusual links...\n",
        ]

        if vulnerable:
            chunks.extend([
                "• I notice the urgent request, but given my workload and official-looking branding, I feel compelled to act quickly.\n",
                "• I am skipping detailed header verification to keep up with my inbox schedule.\n",
                "• Action taken: Proceeding to click link and follow instructions.\n\n",
                "[VULNERABLE]"
            ])
        else:
            chunks.extend([
                "• I noticed suspicious urgency language and domain mismatch upon closer inspection.\n",
                "• I will not click any embedded links or enter credentials.\n",
                "• Action taken: Reporting email to IT Security team immediately.\n\n",
                "[SAFE]"
            ])

        for chunk in chunks:
            yield chunk
            await asyncio.sleep(0.08)

    def extract_decision_from_response(self, text: str) -> str:
        """
        Extracts [VULNERABLE] or [SAFE] decision from accumulated response text using regex.
        Falls back to keyword search or returns 'SAFE' default.
        """
        if not text:
            return "SAFE"

        match = re.search(r'\[(VULNERABLE|SAFE)\]', text, re.IGNORECASE)
        if match:
            return match.group(1).upper()

        # Keyword fallback
        text_upper = text.upper()
        if "VULNERABLE" in text_upper:
            return "VULNERABLE"
        elif "SAFE" in text_upper:
            return "SAFE"

        # Heuristic fallback if explicitly clicked link
        if any(phrase in text.lower() for phrase in ["would click", "proceed to click", "enter credentials", "click the link"]):
            return "VULNERABLE"

        return "SAFE"

    def compute_threat_score(self, decision: str) -> float:
        """
        Converts agent decision to threat score for RiskEngine (0.0 to 100.0).
        VULNERABLE -> 85.0
        SAFE -> 15.0
        """
        return 85.0 if decision.upper() == "VULNERABLE" else 15.0

    def compute_confidence_score(self, text: str, decision: str, signals: List[str]) -> int:
        """
        Calculates confidence score (0-100) based on reasoning depth and signal density.
        """
        base_confidence = 75

        if len(text) > 500:
            base_confidence += 10
        elif len(text) < 150:
            base_confidence -= 10

        if len(signals) >= 3:
            base_confidence += 10

        if f"[{decision}]" in text:
            base_confidence += 5

        return max(50, min(98, base_confidence))

    def extract_signals(self, text: str) -> List[str]:
        """
        Extracts bullet point signals and risk indicators from text.
        """
        signals = []
        for line in text.split("\n"):
            cleaned = line.strip().lstrip("•*- ").strip()
            if cleaned and len(cleaned) > 10 and not cleaned.startswith("["):
                signals.append(cleaned)
        return signals[:5] if signals else ["Simulation behavioral evaluation completed."]

    def build_agent_response_payload(
        self,
        employee_role: str,
        behavior_profile: str,
        decision: str,
        reasoning_text: str,
        scenario: str
    ) -> AgentResponsePayload:
        """
        Constructs standardized AgentResponsePayload object required by RiskEngine.
        """
        threat_score = self.compute_threat_score(decision)
        signals = self.extract_signals(reasoning_text)
        confidence_pct = self.compute_confidence_score(reasoning_text, decision, signals)
        confidence_float = round(confidence_pct / 100.0, 2)

        return AgentResponsePayload(
            agent_name="phishing_simulation_agent",
            threat_score=threat_score,
            confidence=confidence_float,
            threat_categories=["phishing", "social_engineering"],
            detected_signals=signals,
            reasoning=reasoning_text,
            flags={
                "employee_role": employee_role,
                "behavior_profile": behavior_profile,
                "decision": decision,
                "scenario": scenario
            }
        )


gemini_simulation_handler = GeminiSimulationHandler()
