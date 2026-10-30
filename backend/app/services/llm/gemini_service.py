import os
import json
import time
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

# Gemini SDK Import & Client Initialization
try:
    from google import genai as _genai  # type: ignore[import]
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    if GEMINI_API_KEY and "placeholder" not in GEMINI_API_KEY.lower():
        _client: Optional[Any] = _genai.Client(api_key=GEMINI_API_KEY)
        logger.info("[Gemini] Client initialized successfully.")
    else:
        logger.warning("[Gemini] GEMINI_API_KEY missing or invalid placeholder.")
        _client = None
except ImportError:
    logger.error("[Gemini] google-genai library not found in environment.")
    _client = None
except Exception as e:
    logger.error(f"[Gemini] Unexpected initialization error: {e}")
    _client = None

MODEL_PRIORITY: List[str] = [
    "gemini-2.5-flash-preview-04-17",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

_quota_exhausted_until: float = 0.0
_QUOTA_COOLDOWN_SECONDS: int = 120

async def get_gemini_phishing_score(url: str, page_text_summary: str) -> Dict[str, Any]:
    """
    Primary AI analysis service using the Google GenAI SDK with timeout & fallback resilience.
    Returns a 0-100 phishing probability with fallback fields.
    """
    global _quota_exhausted_until

    DEFAULT_FALLBACK: Dict[str, Any] = {
        "analysis": "Fallback heuristic analysis",
        "risk_score": 50,
        "score": 50,
        "reasoning": "Fallback heuristic analysis — AI engine offline or quota exceeded",
        "confidence": "low"
    }

    if _client is None:
        logger.info("[Gemini] Client not configured. Returning fallback response.")
        return DEFAULT_FALLBACK

    if time.time() < _quota_exhausted_until:
        logger.info("[Gemini] Cooldown active. Returning fallback response.")
        return DEFAULT_FALLBACK

    prompt = (
        "You are a cybersecurity expert specializing in phishing detection.\n"
        "Analyze this webpage and rate its phishing probability.\n\n"
        f"URL: {url}\n"
        f"Page Content: {page_text_summary[:500]}\n\n"
        "Respond with ONLY a raw JSON object. No markdown. No code fences. No extra text.\n"
        'Exact format: {"phishing_probability": <integer 0-100>, '
        '"reasoning": "<one sentence>", "confidence": "<high|medium|low>"}'
    )

    quota_failures = 0
    last_error: Optional[str] = None

    for model_name in MODEL_PRIORITY:
        try:
            # Wrap SDK call in thread with a 10s timeout to prevent asyncio loop blocking
            def _call_model():
                return _client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

            response = await asyncio.wait_for(asyncio.to_thread(_call_model), timeout=10.0)

            raw_text: str = response.text.strip() if response and response.text else ""
            if not raw_text:
                continue

            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                if len(lines) > 2:
                    raw_text = "\n".join(lines[1:-1])
                else:
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

            parsed: Dict[str, Any] = json.loads(raw_text)

            _quota_exhausted_until = 0.0
            score = int(parsed.get("phishing_probability", 0))
            reasoning = str(parsed.get("reasoning", "Analysis complete"))
            confidence = str(parsed.get("confidence", "medium"))

            result = {
                "analysis": reasoning,
                "risk_score": score,
                "score": score,
                "reasoning": reasoning,
                "confidence": confidence
            }

            # Debug log short version
            logger.debug(f"[Gemini] AI response generated: model={model_name}, score={score}, reasoning={reasoning[:50]}...")
            return result

        except asyncio.TimeoutError:
            logger.warning(f"[Gemini] Request to model '{model_name}' timed out after 10s.")
            last_error = "Timeout (10s)"
            continue

        except json.JSONDecodeError as e:
            logger.warning(f"[Gemini] JSON decode error for model '{model_name}': {e}")
            last_error = f"JSONDecodeError: {e}"
            continue

        except Exception as e:
            error_str = str(e)
            last_error = error_str

            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                quota_failures += 1
                continue

            if "404" in error_str or "NOT_FOUND" in error_str:
                continue

            continue

    if quota_failures > 0:
        _quota_exhausted_until = time.time() + _QUOTA_COOLDOWN_SECONDS
        logger.warning(f"[Gemini] Quota hit: {quota_failures} models failed. Freezing for 120s.")
    else:
        logger.error(f"[Gemini] All models failed. Returning fallback response. Last error: {last_error}")

    return DEFAULT_FALLBACK
