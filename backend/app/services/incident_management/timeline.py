"""
Timeline and Audit Event Generator for Incident Lifecycle tracking.
"""

from datetime import datetime, timezone
from app.schemas.incident import TimelineEvent


class TimelineGenerator:
    """
    Generates structured audit timeline milestone events.
    """

    @staticmethod
    def create_event(event_type: str, description: str, actor: str = "System") -> TimelineEvent:
        return TimelineEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            description=description,
            actor=actor,
        )

    @classmethod
    def initial_investigation_timeline(cls) -> list[TimelineEvent]:
        now = datetime.now(timezone.utc).isoformat()
        return [
            TimelineEvent(timestamp=now, event_type="Email Received", description="Inbound RFC822 MIME email parsed by Email Intelligence Agent", actor="Email Agent"),
            TimelineEvent(timestamp=now, event_type="Threat Intelligence Completed", description="Multi-agent IoC reputation checks completed across VirusTotal, WHOIS, RDAP, AbuseIPDB, URLScan", actor="Threat Intel Manager"),
            TimelineEvent(timestamp=now, event_type="AI Investigation Completed", description="AI Investigation Engine evaluated social engineering intent and MITRE ATT&CK tactics", actor="AI Investigation Engine"),
            TimelineEvent(timestamp=now, event_type="Incident Auto-Created", description="Security incident automatically created in SOC platform", actor="System Guard"),
        ]
