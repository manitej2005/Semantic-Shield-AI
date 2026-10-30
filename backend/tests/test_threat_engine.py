"""
Integration test suite for Threat Intelligence Engine (Milestone 2 - Module 1).
"""

import sys
import asyncio
import json
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.threat_intelligence.manager import threat_intel_manager
from app.services.threat_intelligence.provider_health import health_monitor_instance
from app.services.threat_intelligence.providers.registry import provider_registry


async def run_tests():
    print("==================================================", flush=True)
    print("[TEST] SEMANTIC SHIELD AI - THREAT INTEL ENGINE TESTS", flush=True)
    print("==================================================", flush=True)

    # 1. Test Provider Registry
    providers = provider_registry.get_registered_providers()
    print(f"\n[1] Provider Registry Check: {len(providers)} providers registered:", flush=True)
    for p in providers:
        print(f"  - {p.provider_name} (Mock Mode: {p.is_mock_mode})", flush=True)
    assert len(providers) >= 5, "Fewer than 5 providers registered!"

    # 2. Test URL Investigation
    test_url = "http://login-secure-payroll-verify.com/auth/harvest"
    print(f"\n[2] Testing URL Analysis: '{test_url}'", flush=True)
    url_res = await threat_intel_manager.analyze_indicator(test_url)
    print(f"  -> Indicator Type: {url_res.type}", flush=True)
    print(f"  -> Composite Risk Score: {url_res.risk_score}/100", flush=True)
    print(f"  -> Confidence Score: {url_res.confidence}/100", flush=True)
    print(f"  -> Reputation Label: {url_res.reputation}", flush=True)
    print(f"  -> Recommended Action: {url_res.recommendation}", flush=True)
    print(f"  -> AI Context Summary: {url_res.ai_context.get('summary')}", flush=True)
    print(f"  -> Provider Count: {len(url_res.providers)}", flush=True)
    assert url_res.risk_score >= 70, "URL analysis failed risk score threshold!"

    # 3. Test Cache Hit
    print(f"\n[3] Testing Cache Hit for URL Analysis...", flush=True)
    cache_res = await threat_intel_manager.analyze_indicator(test_url)
    print(f"  -> Cache Hit Flag: {cache_res.cache_hit} (Execution Time: {cache_res.execution_time_ms}ms)", flush=True)
    assert cache_res.cache_hit is True, "Cache hit failed!"

    # 4. Test IP Investigation
    test_ip = "185.220.101.5"
    print(f"\n[4] Testing IP Analysis: '{test_ip}'", flush=True)
    ip_res = await threat_intel_manager.analyze_indicator(test_ip)
    print(f"  -> Indicator Type: {ip_res.type}", flush=True)
    print(f"  -> Risk Score: {ip_res.risk_score}/100 | Confidence: {ip_res.confidence}/100", flush=True)
    print(f"  -> Reputation: {ip_res.reputation}", flush=True)

    # 5. Test File Hash Investigation
    test_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    print(f"\n[5] Testing File Hash Analysis: '{test_hash[:16]}...'", flush=True)
    hash_res = await threat_intel_manager.analyze_indicator(test_hash)
    print(f"  -> Indicator Type: {hash_res.type}", flush=True)
    print(f"  -> Risk Score: {hash_res.risk_score}/100 | Confidence: {hash_res.confidence}/100", flush=True)

    # 6. Test Provider Health Telemetry
    health_list = await health_monitor_instance.get_all_health()
    print(f"\n[6] Provider Health Telemetry Status ({len(health_list)} records):", flush=True)
    for h in health_list:
        print(f"  - {h.provider}: Status={h.status}, Reachable={h.reachability}, AvgMs={h.avg_response_time_ms}ms", flush=True)

    print("\n==================================================", flush=True)
    print("[SUCCESS] ALL THREAT INTELLIGENCE ENGINE TESTS PASSED!", flush=True)
    print("==================================================", flush=True)


if __name__ == "__main__":
    asyncio.run(run_tests())
