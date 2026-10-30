"""
Reputation mapping and security recommendation generator.
"""

from typing import Tuple, List


def get_reputation_label(risk_score: int) -> str:
    """
    Maps 0-100 risk score to standard security reputation labels.
    """
    if risk_score >= 85:
        return "Critical Malicious"
    if risk_score >= 70:
        return "Malicious"
    if risk_score >= 40:
        return "Suspicious"
    if risk_score >= 15:
        return "Neutral"
    return "Harmless / Clean"


def get_recommended_action(risk_score: int, indicator_type: str, flags: List[str]) -> str:
    """
    Generates actionable operational security recommendations.
    """
    if risk_score >= 85:
        if indicator_type == "url":
            return "Block URL immediately across firewall, email gateway, and browser extensions. Quarantine user sessions."
        if indicator_type in ["ipv4", "ipv6"]:
            return "Block IP address across boundary routers and revoke active authentication tokens."
        if indicator_type in ["sha256", "md5", "sha1"]:
            return "Execute EDR host isolation and purge malicious binary hash across all enterprise endpoints."
        return "Block indicator immediately across enterprise SOC perimeter."

    if risk_score >= 70:
        return "Flag as malicious threat. Enforce MFA re-authentication and restrict user outbound network access."

    if risk_score >= 40:
        return "Assign to SOC analyst queue for manual inspection. Monitor network telemetry for anomalous outbound connections."

    return "No immediate action required. Indicator verified clean across active threat intelligence providers."
