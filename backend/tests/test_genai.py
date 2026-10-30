"""
Standalone Diagnostic Test for Google GenAI / Gemini Provider Integration.
"""

import sys
import os
import logging
from dotenv import load_dotenv

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("test_genai")

# 1. Load backend/.env
env_path = os.path.join(os.path.dirname(__file__), ".env")
loaded = load_dotenv(env_path)
logger.info(f"Loaded .env from '{env_path}': {loaded}")

raw_key = os.getenv("GEMINI_API_KEY", "")
masked_key = raw_key[:6] + "******" if len(raw_key) >= 6 else "(none/too short)"
logger.info(f"GEMINI_API_KEY detected: {masked_key} (length: {len(raw_key)})")

def main():
    try:
        from app.services.llm.gemini_provider import GeminiProvider
        from app.services.llm.provider_factory import ProviderFactory

        logger.info("Testing ProviderFactory instantiation...")
        provider = ProviderFactory.get_provider("gemini")
        logger.info(f"Provider successfully created: {provider.provider_name}")

        import asyncio

        async def run_test():
            logger.info("Sending test prompt: 'Say hello.'")
            prompt = "Say hello and respond ONLY with raw JSON in format {\"greeting\": \"hello\"}."
            res = await provider.generate_json(prompt=prompt)
            logger.info(f"Test response received: {res}")
            print("\n--- TEST SUCCESS ---")
            print(f"Response: {res}\n")

        asyncio.run(run_test())

    except Exception as e:
        logger.error(f"--- TEST FAILURE ---: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

