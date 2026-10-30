import re
from typing import Dict, Any, List

def analyze_content(page_text: str) -> Dict[str, Any]:
    """
    Scans the visible page text for manipulative language patterns,
    threats, and piracy signals.
    """
    if not page_text or len(page_text.strip()) < 50:
        return {
            "score": 0,
            "reasons": ["Insufficient content for analysis"],
            "matched_patterns": [],
            "threat_categories": []
        }

    text_lower = page_text.lower()
    total_score: int = 0
    reasons: List[str] = []
    matched_patterns: List[str] = []
    threat_categories: List[str] = []

    # --- 1. URGENCY PHRASES (+15 each) ---
    urgency_phrases = [
        "act now", "immediate action", "expires in", "limited time", 
        "24 hours", "account will be suspended", "verify immediately", 
        "unauthorized access", "suspicious activity", "confirm your identity"
    ]
    urgency_matches = [p for p in urgency_phrases if re.search(r'\b' + re.escape(p) + r'\b', text_lower)]
    for match in urgency_matches:
        total_score += 15
        matched_patterns.append(match)
    if urgency_matches:
        reasons.append(f"Urgency/Pressure language: {', '.join(urgency_matches)}")
        threat_categories.append("social_engineering")

    # --- 2. CREDENTIAL HARVESTING (+25 each) ---
    credential_phrases = [
        "enter your password", "confirm your password", 
        "enter your credit card", "social security", "enter your ssn",
        "billing information", "payment details", "verify your account"
    ]
    credential_matches = [p for p in credential_phrases if re.search(r'\b' + re.escape(p) + r'\b', text_lower)]
    for match in credential_matches:
        total_score += 25
        matched_patterns.append(match)
    if credential_matches:
        reasons.append(f"Credential harvesting request: {', '.join(credential_matches)}")
        threat_categories.append("phishing")

    # --- 3. FEAR/THREAT LANGUAGE (+20 each) ---
    fear_phrases = [
        "account will be closed", "legal action", 
        "permanently disabled", "device has been hacked", "virus detected"
    ]
    fear_matches = [p for p in fear_phrases if re.search(r'\b' + re.escape(p) + r'\b', text_lower)]
    for match in fear_matches:
        total_score += 20
        matched_patterns.append(match)
    if fear_matches:
        reasons.append(f"Threat/Fear language: {', '.join(fear_matches)}")

    # --- 5. DECEPTIVE DOWNLOADS (+25 each, max 3) ---
    deceptive_download_phrases = [
        "click allow to continue", "update required to watch",
        "download to continue", "install to watch", "free download now",
        "no registration required", "no credit card required",
        "create a free account", "watch for free"
    ]
    deceptive_matches = [p for p in deceptive_download_phrases if re.search(r'\b' + re.escape(p) + r'\b', text_lower)]
    for match in deceptive_matches[:3]:
        total_score += 30
        matched_patterns.append(match)
    if deceptive_matches:
        reasons.append(f"Deceptive conversion/download prompt: {', '.join(deceptive_matches)}")
        threat_categories.append("malware_distribution")

    # --- 6. PIRACY SIGNALS (+55 each, max 3) ---
    piracy_phrases = [
        "watch free online", "full movie free", "download free movie",
        "camrip", "dvdscr", "123movies", "fmovies", "gomovies",
        "putlocker", "streaming for free", "watch online in hd",
        "unlimited streaming"
    ]
    piracy_matches = [p for p in piracy_phrases if re.search(r'\b' + re.escape(p) + r'\b', text_lower)]
    for match in piracy_matches[:3]:
        total_score += 55
        matched_patterns.append(match)
    if piracy_matches:
        reasons.append(f"High-risk piracy content detected: {', '.join(piracy_matches)}")
        threat_categories.append("piracy")

    final_score = min(total_score, 100)
    
    threat_categories = list(set(threat_categories))

    return {
        "score": final_score,
        "reasons": reasons,
        "matched_patterns": matched_patterns,
        "threat_categories": threat_categories
    }
