"""
Controlled SOC Threat Simulation Engine & Campaign Orchestrator.
Generates realistic SOC attack patterns: Burst Traffic, Multi-Stage Campaigns, Domain Correlation, & Noise Injection.
All events are explicitly labeled with [SIMULATION] and is_simulation=True for absolute honesty.
"""

import asyncio
import random
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.domain.models.request import AnalyzeRequest
from app.orchestrator.supervisor import SupervisorAgent
from app.services.activity.feed import activity_feed_manager
from app.services.incident_management.manager import incident_manager
from app.services.websocket.manager import websocket_manager

logger = logging.getLogger("app.services.simulation")


# ==========================================
# ADVANCED SCENARIO & NOISE CATALOG
# ==========================================
ADVANCED_SCENARIOS: List[Dict[str, Any]] = [
    # 1. High-Risk Malicious Phishing Vectors
    {
        "id": "SIM-EMAIL-01",
        "category": "Email Phishing",
        "type": "malicious",
        "title": "Microsoft 365 Credential Harvester",
        "vector": "email",
        "domain": "login-microsoftonline.com-auth365.xyz",
        "url": "https://login-microsoftonline.com-auth365.xyz/login",
        "page_text": "URGENT: Your Microsoft 365 password expires in 1 hour! Re-verify your credentials immediately.",
        "target": "Finance Officer <finance@corporate.com>",
        "base_severity": "Critical"
    },
    {
        "id": "SIM-EMAIL-02",
        "category": "Email Phishing",
        "type": "malicious",
        "title": "Urgent CEO Wire Transfer Request",
        "vector": "email",
        "domain": "wire-transfer-express.top",
        "url": "https://wire-transfer-express.top/pay",
        "page_text": "CONFIDENTIAL: Urgent international wire transfer request from CEO Office. Process payment of $45,000 immediately.",
        "target": "Treasury Lead <treasury@corporate.com>",
        "base_severity": "High"
    },
    {
        "id": "SIM-URL-01",
        "category": "URL Attack",
        "type": "malicious",
        "title": "Typosquatted PayPal Verification Portal",
        "vector": "website",
        "domain": "paypal-security-auth-check.com",
        "url": "https://paypal-security-auth-check.com/verify-account",
        "page_text": "PayPal Alert: Suspicious login detected from Luxemburg. Click here to confirm identity.",
        "target": "Corporate User Inbox",
        "base_severity": "High"
    },
    # 2. Benign Background Noise & False Positives
    {
        "id": "SIM-NOISE-01",
        "category": "Internal Activity",
        "type": "benign",
        "title": "Internal Confluence Knowledge Base",
        "vector": "website",
        "domain": "wiki.internal.corporate.com",
        "url": "https://wiki.internal.corporate.com/pages/viewpage.action?pageId=9021",
        "page_text": "Welcome to the Engineering Architecture Wiki. Documentation for deployment guidelines and microservice API specs.",
        "target": "Software Engineer Workstation",
        "base_severity": "Low"
    },
    {
        "id": "SIM-NOISE-02",
        "category": "False Positive Candidate",
        "type": "false_positive",
        "title": "Marketing Newsletter Urgency Flag",
        "vector": "email",
        "url": "https://marketing.hubspot.com/event-register",
        "page_text": "LAST CHANCE! Only 24 hours left to register for the Annual Cloud Security Webinar. Sign up now!",
        "target": "Marketing Operations <marketing@corporate.com>",
        "base_severity": "Low"
    }
]

SIMULATION_SCENARIOS = ADVANCED_SCENARIOS


class SimulationEngine:
    """
    Advanced SOC Threat Simulation Engine.
    Orchestrates Burst Attacks, Multi-Stage Campaigns, Domain Correlation, & Noise Injection.
    """

    def __init__(self):
        self._is_running: bool = False
        self._task: Optional[asyncio.Task] = None
        self._interval_seconds: int = 8
        self._events_generated_count: int = 0
        self._last_event_time: Optional[str] = None
        self._domain_target_tracker: Dict[str, int] = {} #Correlation map
        self._supervisor = SupervisorAgent()

    @property
    def is_running(self) -> bool:
        return self._is_running

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self._is_running,
            "interval_seconds": self._interval_seconds,
            "events_generated_count": self._events_generated_count,
            "last_event_time": self._last_event_time,
            "tracked_correlated_domains": len(self._domain_target_tracker),
            "mode": "REALISTIC_SOC_SIMULATION",
            "capabilities": ["Burst Traffic", "Multi-Stage Campaigns", "Domain Correlation", "Noise Injection"]
        }

    async def execute_scenario(
        self,
        scenario: Dict[str, Any],
        correlation_domain: Optional[str] = None,
        stage: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a single simulation scenario with correlation tracking and real-time broadcasting.
        """
        now = datetime.now(timezone.utc).isoformat()
        self._events_generated_count += 1
        self._last_event_time = now

        req = AnalyzeRequest(
            url=scenario["url"],
            page_text=scenario["page_text"]
        )

        res = await self._supervisor.process_analysis(req)

        url = scenario["url"]
        domain = correlation_domain or scenario.get("domain", url.split("/")[2] if "/" in url else url)
        
        # Track correlation hit count for domain
        hit_count = self._domain_target_tracker.get(domain, 0) + 1
        self._domain_target_tracker[domain] = hit_count

        raw_score = res.get("risk_score", 40)
        
        # Escalate score if domain hit multiple users (Correlation Rule)
        if hit_count >= 3 and scenario.get("type") == "malicious":
            raw_score = min(100, raw_score + 15)
            logger.info(f"[Simulation Correlation] Escalating risk score for domain {domain} (Hit count: {hit_count})")

        classification = "High Risk" if raw_score >= 70 else "Suspicious" if raw_score >= 40 else "Safe"
        reasons = res.get("reasons", ["Simulation vector analysis completed."])

        if hit_count > 1:
            reasons.append(f"[Correlation Engine] Same target domain '{domain}' hit {hit_count} corporate targets")

        stage_tag = f" [{stage}]" if stage else ""
        title = f"[SIMULATION]{stage_tag} {scenario['title']}"

        # 1. Log Activity Item
        severity = "critical" if raw_score >= 85 else "high" if raw_score >= 70 else "warning" if raw_score >= 40 else "info"
        act_item = activity_feed_manager.log_activity(
            category="Offensive Simulation Executed",
            title=title,
            details=f"Vector: {scenario['category']} | Target: {scenario.get('target', url)} | Score: {raw_score}/100",
            severity=severity,
            actor="Simulation Engine"
        )

        # 2. Auto-create Incident if score >= 40
        inc = await incident_manager.create_from_scan(
            url=url,
            risk_score=raw_score,
            classification=classification,
            reasons=reasons,
            source="Simulation Engine",
            is_simulation=True
        )

        # 3. Broadcast WebSocket Telemetry
        scan_event_data = {
            "id": act_item.activity_id,
            "url": url,
            "title": title,
            "classification": classification,
            "risk_score": raw_score,
            "reasons": reasons,
            "timestamp": act_item.timestamp,
            "is_simulation": True,
            "correlated_hits": hit_count,
            "incident_id": inc.incident_id if inc else None
        }

        await websocket_manager.broadcast_event("SCAN_COMPLETED", scan_event_data, channel="dashboard")
        await websocket_manager.broadcast_event("ACTIVITY_LOGGED", act_item.dict(), channel="activity")

        if inc:
            await websocket_manager.broadcast_event("INCIDENT_CREATED", inc.dict(), channel="incidents")

        return {
            "status": "simulation_executed",
            "is_simulation": True,
            "scenario": scenario,
            "correlated_hits": hit_count,
            "result": res,
            "activity": act_item,
            "incident": inc
        }

    async def execute_burst_attack(self, count: int = 10, delay_ms: int = 150) -> Dict[str, Any]:
        """
        Burst Pattern: Sends N rapid threat events within 2 seconds to stress-test SOC velocity.
        """
        logger.info(f"[SimulationEngine] Launching Burst Attack: {count} events with {delay_ms}ms delay...")
        results = []
        for i in range(count):
            scenario = random.choice(ADVANCED_SCENARIOS)
            res = await self.execute_scenario(scenario, stage=f"BURST {i+1}/{count}")
            results.append(res)
            await asyncio.sleep(delay_ms / 1000.0)

        return {
            "status": "burst_completed",
            "total_burst_events": len(results),
            "is_simulation": True
        }

    async def execute_campaign(self, campaign_type: str = "spear_phish_escalation") -> Dict[str, Any]:
        """
        Multi-Stage Campaign Pattern:
        Stage 1: Initial Reconnaissance / Phishing Mail
        Stage 2: Credential Harvester Access on Same Domain
        Stage 3: Privilege Escalation / OAuth Token Theft
        """
        domain = "auth-corp-login-update.xyz"
        stages = [
            {
                "stage": "STAGE 1: Initial Access",
                "target": "HR Manager <hr@corporate.com>",
                "scenario": {
                    "id": "SIM-CAMP-01",
                    "category": "Initial Access Phish",
                    "title": "Corporate Policy Update Notice",
                    "url": f"https://{domain}/notice",
                    "page_text": "Please review the updated 2026 employee handbook and confirm your account login."
                }
            },
            {
                "stage": "STAGE 2: Credential Harvest",
                "target": "IT Administrator <admin@corporate.com>",
                "scenario": {
                    "id": "SIM-CAMP-02",
                    "category": "Credential Harvest",
                    "title": "Active Directory Password Reset Intercept",
                    "url": f"https://{domain}/sso-verify",
                    "page_text": "Your Active Directory session has expired. Enter master domain password to restore SSO token."
                }
            },
            {
                "stage": "STAGE 3: Privilege Escalation",
                "target": "CEO Office <executive@corporate.com>",
                "scenario": {
                    "id": "SIM-CAMP-03",
                    "category": "Lateral Movement",
                    "title": "Executive Board OAuth Consent Request",
                    "url": f"https://{domain}/oauth/authorize",
                    "page_text": "Grant full read/write permissions for Google Workspace Domain Admin scope to untrusted app."
                }
            }
        ]

        results = []
        for stage_info in stages:
            res = await self.execute_scenario(
                stage_info["scenario"],
                correlation_domain=domain,
                stage=stage_info["stage"]
            )
            results.append(res)
            await asyncio.sleep(1.5) # 1.5s delay between campaign stages

        return {
            "status": "campaign_completed",
            "campaign_domain": domain,
            "total_stages": len(results),
            "is_simulation": True
        }

    async def _loop(self):
        """
        Background loop generating realistic SOC traffic (Mix of malicious attacks, stealth events, & noise).
        """
        logger.info(f"[SimulationEngine] Realistic SOC loop started with base interval {self._interval_seconds}s")
        while self._is_running:
            try:
                # 70% chance malicious, 30% chance benign noise/false positive
                if random.random() < 0.3:
                    scenario = next((s for s in ADVANCED_SCENARIOS if s["type"] != "malicious"), ADVANCED_SCENARIOS[0])
                else:
                    scenario = random.choice([s for s in ADVANCED_SCENARIOS if s["type"] == "malicious"])

                await self.execute_scenario(scenario)
            except Exception as exc:
                logger.error(f"[SimulationEngine] Error in loop: {exc}", exc_info=True)

            delay = max(3, self._interval_seconds + random.randint(-2, 4))
            await asyncio.sleep(delay)

    def start(self, interval_seconds: int = 8) -> Dict[str, Any]:
        if self._is_running:
            return {"status": "already_running", "message": "Simulation engine is active."}

        self._interval_seconds = interval_seconds
        self._is_running = True
        self._task = asyncio.create_task(self._loop())
        logger.info("[SimulationEngine] Realistic SOC worker activated.")
        return {"status": "started", "interval_seconds": interval_seconds}

    def stop(self) -> Dict[str, Any]:
        if not self._is_running:
            return {"status": "not_running", "message": "Simulation engine is not running."}

        self._is_running = False
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("[SimulationEngine] Realistic SOC worker stopped.")
        return {"status": "stopped"}


simulation_engine = SimulationEngine()
