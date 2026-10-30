import asyncio
from app.services.llm.gemini_service import get_gemini_phishing_score

async def main():
    """
    Diagnostic script to verify the new Google GenAI SDK overhaul.
    Tests both a known safe page and a simulated phishing page.
    """
    print("\n--- Test 1: SAFE ---")
    r1 = await get_gemini_phishing_score(
        "https://www.google.com",
        "Google search engine homepage"
    )
    print(f"Score: {r1['score']} | Confidence: {r1['confidence']}")
    print(f"Reasoning: {r1['reasoning']}")
    
    print("\n--- Test 2: PHISHING ---")
    r2 = await get_gemini_phishing_score(
        "http://secure-paypa1-login.verify-now.com",
        "Dear customer your account will be suspended in 24 hours. Enter your password immediately to confirm your identity."
    )
    print(f"Score: {r2['score']} | Confidence: {r2['confidence']}")
    print(f"Reasoning: {r2['reasoning']}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Test Execution Error: {e}")
