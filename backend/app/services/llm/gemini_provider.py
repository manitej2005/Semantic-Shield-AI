"""
Centralized Google Gemini LLM Provider Implementation.
Model-agnostic provider adapter that communicates with Google GenAI SDK.
"""

import os
import json
import time
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

from app.domain.interfaces.base_llm_provider import BaseLLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)

# Ensure .env is loaded
load_dotenv()


class GeminiProvider(BaseLLMProvider):
    """
    Centralized provider for Google Gemini models.
    Supports automatic model fallback and structured JSON response parsing.
    """

    # Verified active models list ordered by preference & stability
    MODEL_PRIORITY: List[str] = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
    ]

    def __init__(self, api_key: Optional[str] = None):
        resolved_key = api_key or os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        self._api_key = (resolved_key or "").strip().strip('"').strip("'")
        self._client = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """
        Validates the API key and initializes the GenAI SDK client.
        Raises ValueError if key is missing or unconfigured placeholder.
        """
        key = self._api_key
        invalid_placeholders = [
            "paste_your_api_key_here",
            "aizasy_placeholder_key_here",
            "placeholder",
        ]

        if not key or any(p in key.lower() for p in invalid_placeholders):
            masked_info = (key[:6] + "******") if key else "(none)"
            logger.error(f"[GeminiProvider] API Key missing or invalid placeholder detected: {masked_info}")
            raise ValueError(
                f"Gemini API key is missing or unconfigured (key: {masked_info}). "
                "Please set a valid GEMINI_API_KEY in backend/.env file."
            )

        # Log masked key confirmation (never full key)
        masked_key = key[:6] + "******" if len(key) >= 6 else "******"
        logger.info(f"[GeminiProvider] API Key Detected: {masked_key} (length: {len(key)})")

        try:
            from google import genai  # type: ignore[import]
            self._client = genai.Client(api_key=key)
            logger.info("[GeminiProvider] Google GenAI SDK client initialized successfully.")
        except ImportError as e:
            logger.error(f"[GeminiProvider] google-genai package is not installed: {e}")
            raise ImportError(
                "google-genai package is required. Install it via pip install google-genai."
            ) from e
        except Exception as e:
            logger.error(f"[GeminiProvider] Client initialization failed: {e}", exc_info=True)
            raise RuntimeError(f"Failed to initialize Gemini Client: {e}") from e

    @property
    def provider_name(self) -> str:
        return "google-gemini"

    async def generate_json(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends prompt to Gemini model and returns parsed JSON object.
        Iterates over MODEL_PRIORITY list if model_name is not explicitly supplied.
        """
        if not self._client:
            self._initialize_client()

        models_to_try = [model_name] if model_name else self.MODEL_PRIORITY
        last_error: Optional[str] = None

        full_contents = prompt
        if system_instruction:
            full_contents = f"System Instruction: {system_instruction}\n\nTask:\n{prompt}"

        for model in models_to_try:
            try:
                logger.info(f"[GeminiProvider] Selected model: {model}")
                logger.info(f"[GeminiProvider] Request sent to model '{model}' (prompt length: {len(prompt)} chars)...")
                
                def _call():
                    return self._client.models.generate_content(
                        model=model,
                        contents=full_contents
                    )

                response = await asyncio.wait_for(asyncio.to_thread(_call), timeout=6.0)

                if not response or not response.text:
                    logger.warning(f"[GeminiProvider] Model '{model}' returned empty response. Retrying next model...")
                    continue

                logger.info(f"[GeminiProvider] Response received from model '{model}'. Parsing JSON response...")
                raw_text = response.text.strip()
                
                # Strip markdown code fences if present
                if raw_text.startswith("```"):
                    lines = raw_text.split("\n")
                    if len(lines) > 2:
                        raw_text = "\n".join(lines[1:-1])
                    else:
                        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

                parsed_json = json.loads(raw_text)
                logger.info(f"[GeminiProvider] Successfully generated and parsed JSON from model '{model}'.")
                return parsed_json

            except asyncio.TimeoutError:
                logger.warning(f"[GeminiProvider] Model '{model}' execution timed out after 10s.")
                last_error = "Timeout (10s)"
                continue

            except json.JSONDecodeError as e:
                logger.warning(f"[GeminiProvider] JSON decode failed for model '{model}': {e}")
                last_error = f"JSON decode error: {e}"
                continue

            except Exception as e:
                error_msg = str(e)
                logger.warning(f"[GeminiProvider] Request to model '{model}' failed: {error_msg}")
                last_error = error_msg

                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    logger.warning(f"[GeminiProvider] Rate limit / quota exhausted for '{model}'. Retrying next model...")
                
                continue

        logger.error(f"[GeminiProvider] All candidate models failed. Last error: {last_error}")
        raise RuntimeError(f"Gemini API generation failed across all models. Last error: {last_error}")
