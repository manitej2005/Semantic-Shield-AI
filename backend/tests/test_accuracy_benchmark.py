"""
SemanticShield AI - Phishing & Threat Detection Accuracy Benchmark
Tests 15 diverse web targets (Phishing, Piracy, Deceptive Downloads, Legitimate)
"""

import asyncio
import logging
from app.domain.models.request import AnalyzeRequest
from app.orchestrator.supervisor import SupervisorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("accuracy_benchmark")

BENCHMARK_SITES = [
    # --- MALICIOUS / PHISHING / PIRACY / DECEPTIVE VECTORS ---
    {
        "url": "https://netmirror.center/watch-free-movies",
        "text": "NetMirror - Watch Movies Online Free. Stream full HD movies, TV shows, series online without registration. Click Allow to download HD player.",
        "expected": "High Risk",
        "category": "Piracy / Deceptive Download"
    },
    {
        "url": "https://login-microsoftonline.com-auth365.xyz/login",
        "text": "URGENT: Your Microsoft 365 password expires in 1 hour! Re-verify your credentials immediately to avoid account closure. Enter password.",
        "expected": "High Risk",
        "category": "Credential Phishing"
    },
    {
        "url": "https://paypal-security-auth-check.com/verify-account",
        "text": "PayPal Security Alert: Unauthorized access attempt detected. Confirm your credit card details and billing information now to restore access.",
        "expected": "High Risk",
        "category": "Financial Phishing"
    },
    {
        "url": "https://123movies-free-hd.top/stream",
        "text": "123Movies - Watch Free Online Movies in HD. Update Chrome Flash Player required to play video. Free download no registration.",
        "expected": "High Risk",
        "category": "Piracy / Drive-by Malware"
    },
    {
        "url": "https://movierulz-hd.live/watch",
        "text": "MovieRulz Free Streaming online. Click Allow to continue watching. Free account registration required.",
        "expected": "High Risk",
        "category": "Piracy / Popunder Trap"
    },
    {
        "url": "https://chase-bank-verify-alert.site/login",
        "text": "Chase Bank Account Suspended! Enter SSN and Online Banking Password immediately to unlock your debit card.",
        "expected": "High Risk",
        "category": "Banking Phishing"
    },
    {
        "url": "https://auth-corp-login-update.xyz/notice",
        "text": "IT Security Notice: Mandatory password update required for all employee accounts. Click here to verify credentials.",
        "expected": "High Risk",
        "category": "Spear Phishing"
    },
    {
        "url": "https://meta-facebook-copyright-claim.site/appeal",
        "text": "Your Facebook Business Page will be deleted due to copyright infringement. Submit login details within 24 hours to appeal.",
        "expected": "High Risk",
        "category": "Social Engineering"
    },

    # --- LEGITIMATE SITES (SAFE VECTORS) ---
    {
        "url": "https://www.microsoft.com/en-us/",
        "text": "Microsoft Official Site. Explore Surface devices, Windows 11, Microsoft 365, Copilot, Xbox, and Office apps for home and business.",
        "expected": "Safe",
        "category": "Legitimate Corporate"
    },
    {
        "url": "https://www.paypal.com/us/home",
        "text": "PayPal - Pay, Send Money and Accept Payments. Simple, secure digital wallet and online payment processing.",
        "expected": "Safe",
        "category": "Legitimate Financial"
    },
    {
        "url": "https://www.netflix.com/browse",
        "text": "Netflix - Watch TV Shows Online, Watch Movies Online. Unlimited movies, TV shows, and more. Cancel anytime.",
        "expected": "Safe",
        "category": "Legitimate Streaming"
    },
    {
        "url": "https://github.com/about",
        "text": "GitHub is where over 100 million developers shape the future of software, together. Build, ship, and maintain software.",
        "expected": "Safe",
        "category": "Legitimate Developer Portal"
    },
    {
        "url": "https://www.wikipedia.org/",
        "text": "Wikipedia is a free online encyclopedia, created and edited by volunteers around the world and hosted by the Wikimedia Foundation.",
        "expected": "Safe",
        "category": "Legitimate Educational"
    }
]

async def run_benchmark():
    supervisor = SupervisorAgent()
    print("\n==========================================================================================")
    print("                    SEMANTICSHIELD AI ACCURACY BENCHMARK EVALUATION                       ")
    print("==========================================================================================\n")
    
    total = len(BENCHMARK_SITES)
    correct = 0

    for idx, item in enumerate(BENCHMARK_SITES, 1):
        req = AnalyzeRequest(url=item["url"], page_text=item["text"])
        res = await supervisor.process_analysis(req)
        
        classification = res.get("classification", "Safe")
        score = res.get("risk_score", 0)
        agents = res.get("agents", {})
        
        sem_score = agents.get("semantic", {}).get("score", 0)
        beh_score = agents.get("behavior", {}).get("score", 0)
        url_score = agents.get("url", {}).get("score", 0)
        
        is_threat_expected = item["expected"] in ("High Risk", "Suspicious")
        is_threat_detected = classification in ("High Risk", "Suspicious")
        passed = (is_threat_expected == is_threat_detected)
        
        if passed:
            correct += 1
            status_str = "PASS [OK]"
        else:
            status_str = "FAIL [X]"
            
        print(f"[{idx:02d}/{total:02d}] [{status_str}] Category: {item['category']}")
        print(f"      URL: {item['url']}")
        print(f"      Result: {classification} (Score: {score}/100) | Expected: {item['expected']}")
        print(f"      Agent Scores -> Semantic: {sem_score}/100 | Behavior: {beh_score}/100 | URL Intel: {url_score}/100")
        print("-" * 90)

    accuracy = (correct / total) * 100
    print(f"\nFINAL ACCURACY SCORE: {correct}/{total} ({accuracy:.1f}%)\n")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
