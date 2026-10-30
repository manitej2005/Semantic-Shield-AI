import sys
import json
import time

sys.path.insert(0, ".")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_qa_suite():
    print("=== STARTING QA END-TO-END VALIDATION SUITE ===")
    
    # 1. Measure API latency
    t0 = time.time()
    res = client.post("/analyze", json={
        "url": "https://test-phishing-qa.com/login",
        "page_text": "URGENT: Password expired. Log in immediately to verify."
    })
    api_latency_ms = round((time.time() - t0) * 1000, 2)
    print(f"1. /analyze Endpoint Latency: {api_latency_ms} ms | Status: {res.status_code}")

    # 2. Measure Simulation Latency
    t1 = time.time()
    sim_res = client.post("/api/dashboard/simulate")
    sim_latency_ms = round((time.time() - t1) * 1000, 2)
    print(f"2. /api/dashboard/simulate Latency: {sim_latency_ms} ms | Status: {sim_res.status_code}")

    # 3. Test Activity retrieval
    act_res = client.get("/api/dashboard/activity")
    print(f"3. /api/dashboard/activity Items: {len(act_res.json())} | Status: {act_res.status_code}")

    # 4. Test Incidents retrieval
    inc_res = client.get("/api/dashboard/incidents")
    print(f"4. /api/dashboard/incidents Items: {len(inc_res.json())} | Status: {inc_res.status_code}")

    # 5. Test Burst simulation
    t2 = time.time()
    burst_res = client.post("/api/dashboard/simulator/burst?count=5&delay_ms=50")
    burst_latency_ms = round((time.time() - t2) * 1000, 2)
    print(f"5. Burst Simulation Latency: {burst_latency_ms} ms | Status: {burst_res.status_code}")

    print("\n=== QA SUITE METRICS COMPLETE ===")

if __name__ == "__main__":
    run_qa_suite()
