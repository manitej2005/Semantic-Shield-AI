"""
URL Heuristics Engine calculating string entropy, typosquatting, homoglyphs, and credential harvesting keywords.
"""

import math
import re
from typing import List, Tuple
from urllib.parse import urlparse
from app.schemas.email import URLHeuristicsResult

CREDENTIAL_KEYWORDS = {
    "login", "signin", "verify", "account", "security", "update", "banking",
    "password", "mfa", "2fa", "credential", "payroll", "invoice", "token",
    "confirm", "support", "office365", "microsoft", "google", "apple", "paypal", "harvest"
}

KNOWN_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "ow.ly", "is.gd", "buff.ly", "rebrand.ly", "cutt.ly"
}

LEGIT_TARGET_BRANDS = ["microsoft.com", "google.com", "apple.com", "paypal.com", "bankofamerica.com"]


class URLHeuristicsEngine:
    """
    Evaluates static and structural heuristics for URLs.
    """

    @staticmethod
    def calculate_entropy(text: str) -> float:
        """
        Calculates Shannon Entropy for string randomness detection.
        """
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
        return round(entropy, 2)

    @classmethod
    def evaluate(cls, url: str) -> URLHeuristicsResult:
        flags: List[str] = []
        score = 0
        
        parsed = urlparse(url if url.startswith(("http://", "https://")) else f"http://{url}")
        hostname = parsed.netloc.split(":")[0].lower()
        path = parsed.path.lower()
        full_url = url.lower()
        
        # 1. Check IP Address Hostname
        is_ip = bool(re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", hostname))
        if is_ip:
            flags.append("IP-based Hostname used instead of Domain")
            score += 35

        # 2. Check Shortener Services
        is_shortener = hostname in KNOWN_SHORTENERS
        if is_shortener:
            flags.append("URL Shortener Redirection Service")
            score += 20

        # 3. Subdomain Depth & Hyphenation
        subdomains = hostname.split(".")
        subdomain_count = max(0, len(subdomains) - 2)
        if subdomain_count >= 3:
            flags.append(f"Excessive Subdomain Depth ({subdomain_count} levels)")
            score += 20
            
        hyphen_count = hostname.count("-")
        if hyphen_count >= 2:
            flags.append(f"Multiple Hyphenated Domain Tokens ({hyphen_count} hyphens)")
            score += 20

        # 4. Entropy Score
        entropy = cls.calculate_entropy(hostname)
        if entropy > 4.2:
            flags.append(f"High Hostname Entropy ({entropy}) - Potential DGA / Random String")
            score += 25

        # 5. Credential Harvesting Keywords (15 pts per keyword)
        found_keywords = [kw for kw in CREDENTIAL_KEYWORDS if kw in full_url]
        has_keywords = bool(found_keywords)
        if has_keywords:
            kw_score = min(45, len(found_keywords) * 15)
            flags.append(f"Credential Harvesting Keywords Detected ({len(found_keywords)}): {', '.join(found_keywords[:3])}")
            score += kw_score

        # 6. Homoglyphs / Punycode
        has_homoglyph = "xn--" in hostname
        if has_homoglyph:
            flags.append("Punycode / Homoglyph Unicode Character Impersonation")
            score += 40

        # 7. Non-standard Port
        port = parsed.port
        if port and port not in [80, 443]:
            flags.append(f"Non-Standard Port Num ({port})")
            score += 15

        # 8. HTTPS check
        is_https = parsed.scheme == "https"
        if not is_https:
            flags.append("Insecure HTTP Protocol")
            score += 10

        # 9. Typosquatting / Brand Lookalike check
        typosquat = False
        for brand in LEGIT_TARGET_BRANDS:
            brand_name = brand.split(".")[0]
            if brand_name in hostname and not hostname.endswith(brand):
                typosquat = True
                flags.append(f"Brand Impersonation / Typosquatting of '{brand_name}'")
                score += 45
                break

        # 10. URL Length
        if len(url) > 50:
            flags.append(f"Excessive URL Length ({len(url)} chars)")
            score += 15

        final_risk_score = min(100, score)

        return URLHeuristicsResult(
            url=url,
            length=len(url),
            hostname=hostname,
            is_ip_address=is_ip,
            is_shortener=is_shortener,
            subdomain_count=subdomain_count,
            entropy_score=entropy,
            has_credential_keywords=has_keywords,
            has_homoglyphs=has_homoglyph,
            is_https=is_https,
            non_standard_port=port,
            typosquatting_detected=typosquat,
            suspicious_flags=flags,
            heuristic_risk_score=final_risk_score,
        )
