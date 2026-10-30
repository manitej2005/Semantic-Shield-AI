import os
import sys
from dotenv import load_dotenv

# 1. Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("=== SematicSheld AI Diagnostic ===")
print(f"Python Version: {sys.version}")

# 2. Check which libraries are installed
try:
    import google.generativeai as legacy_genai
    print("Found legacy library: google.generativeai")
except ImportError:
    legacy_genai = None
    print("Legacy library (google-generativeai) NOT found.")

try:
    from google import genai as modern_genai
    print("Found modern library: google-genai")
except ImportError:
    modern_genai = None
    print("Modern library (google-genai) NOT found.")

if not api_key:
    print("ERROR: No GEMINI_API_KEY found in .env")
    exit()

print(f"API Key: {api_key[:10]}...")

# 3. Try to list models with Legacy SDK
if legacy_genai:
    print("\n--- Listing models with LEGACY SDK ---")
    try:
        legacy_genai.configure(api_key=api_key)
        models = list(legacy_genai.list_models())
        print(f"Found {len(models)} models.")
        for m in models:
            print(f"  - {m.name}")
    except Exception as e:
        print(f"Legacy SDK List Error: {e}")

# 4. Try to list models with Modern SDK
if modern_genai:
    print("\n--- Listing models with MODERN SDK ---")
    try:
        client = modern_genai.Client(api_key=api_key)
        count = 0
        for m in client.models.list():
            print(f"  - {m.name}")
            count += 1
        print(f"Found {count} models.")
    except Exception as e:
        print(f"Modern SDK List Error: {e}")

if not legacy_genai and not modern_genai:
    print("\nERROR: No Gemini SDKs installed.")
