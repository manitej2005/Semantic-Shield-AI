import urllib.request
import json
import time

def helper_get(url):
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"GET {url} => {resp.status} SUCCESS: {data}")
            return True
    except Exception as e:
        print(f"GET {url} => FAILED: {e}")
        return False

def helper_post(url, payload):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"POST {url} => {resp.status} SUCCESS!")
            print(f"  Risk score: {data.get('risk_score')}")
            print(f"  Classification: {data.get('classification')}")
            print(f"  Confidence: {data.get('confidence')}")
            print(f"  Agents executed: {list(data.get('agents', {}).keys())}")
            print(f"  Reasons count: {len(data.get('reasons', []))}")
            return True
    except Exception as e:
        print(f"POST {url} => FAILED: {e}")
        return False

if __name__ == '__main__':
    print("--- TESTING GET ENDPOINTS ---")
    helper_get('http://127.0.0.1:8000/')
    helper_get('http://127.0.0.1:8000/health')
    helper_get('http://127.0.0.1:8000/status')
    helper_get('http://127.0.0.1:8000/api/v1/status')

    print("\n--- TESTING POST ENDPOINTS ---")
    payload = {
        'url': 'http://secure-paypa1-login.verify-now.com',
        'page_text': 'URGENT NOTICE: Your account has been temporarily restricted due to unauthorized login attempts. You must click here to verify your password within 24 hours or your bank balance will be frozen.'
    }

    print("\n1. Testing POST /analyze...")
    helper_post('http://127.0.0.1:8000/analyze', payload)

    print("\n2. Testing POST /api/v1/analyze...")
    helper_post('http://127.0.0.1:8000/api/v1/analyze', payload)

