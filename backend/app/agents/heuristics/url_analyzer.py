import urllib.parse
import math
import re
from typing import Dict, Any, List, Optional

def calculate_shannon_entropy(data: str) -> float:
    """
    Calculates the Shannon entropy of a string.
    High entropy suggests random or obfuscated strings.
    """
    if not data:
        return 0.0
    entropy = 0.0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        entropy -= p_x * math.log(p_x, 2)
    return entropy

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings to find lookalikes.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def analyze_url(url: str) -> Dict[str, Any]:
    """
    Analyzes the URL for suspicious characteristics to measure phishing risk.
    """
    score: int = 0
    reasons: List[str] = []
    flags: Dict[str, Any] = {}

    # Ensure URL has a scheme for reliable parsing
    if not url.startswith("http://") and not url.startswith("https://"):
        parsed_url = urllib.parse.urlparse("http://" + url)
    else:
        parsed_url = urllib.parse.urlparse(url)

    domain = parsed_url.netloc.lower()
    path = parsed_url.path.lower()
    query = parsed_url.query.lower()

    # Remove port from domain if present
    if ":" in domain:
        domain = domain.split(":")[0]

    path_and_query = path
    if query:
        path_and_query += "?" + query

    # --- 1. URL LENGTH CHECK ---
    url_length = len(url)
    flags["length"] = url_length
    if url_length > 100:
        score += 20
        reasons.append(f"URL is very long ({url_length} characters)")
    elif url_length > 75:
        score += 10
        reasons.append(f"URL length is suspicious ({url_length} characters)")

    # --- 2. SHANNON ENTROPY CHECK ---
    entropy = calculate_shannon_entropy(url)
    flags["entropy"] = entropy
    if entropy > 4.2:
        score += 15
        reasons.append(f"High character entropy ({entropy:.2f}), suggesting obfuscation")

    # --- 3. SUSPICIOUS KEYWORDS ---
    suspicious_keywords = [
        "login", "verify", "update", "secure", "account", "banking", 
        "confirm", "password", "signin", "authenticate", "wallet", 
        "suspended", "unusual", "alert", "paypal", "amazon", "google", 
        "microsoft", "apple", "netflix", "ebay", "instagram", "facebook"
    ]
    found_keywords = [kw for kw in suspicious_keywords if kw in path_and_query]
    flags["found_keywords"] = found_keywords
    if found_keywords:
        score += 15
        reasons.append(f"Suspicious keywords in path: {', '.join(found_keywords)}")

    # --- 4. EXCESSIVE SUBDOMAINS ---
    subdomains = domain.split(".")
    subdomain_count = len(subdomains) - 2 if len(subdomains) > 2 else 0
    flags["subdomain_count"] = subdomain_count
    if subdomain_count >= 3:
        score += 15
        reasons.append(f"Excessive subdomains ({subdomain_count})")

    # --- 5. IP ADDRESS AS HOST ---
    is_ip = bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain))
    flags["is_ip_host"] = is_ip
    if is_ip:
        score += 25
        reasons.append("URL uses an IP address instead of a domain name")

    # --- 6. SPECIAL CHARACTERS IN DOMAIN ---
    num_hyphens = domain.count("-")
    has_at_symbol = "@" in url
    flags["domain_hyphens"] = num_hyphens
    flags["has_at_symbol"] = has_at_symbol
    
    if num_hyphens > 2:
        score += 10
        reasons.append(f"Excessive hyphens in domain ({num_hyphens})")
    if has_at_symbol:
        score += 20
        reasons.append("URL contains nested credentials/redirection character '@'")

    # --- 7. LOOKALIKE DOMAIN DETECTION ---
    brands = [
        "paypal", "amazon", "google", "microsoft", "apple", "netflix", 
        "facebook", "instagram", "ebay", "bank", "chase", "wellsfargo",
        "citibank", "linkedin", "twitter", "youtube", "gmail", "yahoo"
    ]
    parts_to_check = subdomains[:-1] if len(subdomains) > 1 else subdomains
    lookalike_found: Optional[str] = None
    min_dist_found: Optional[int] = None
    
    for part in parts_to_check:
        for brand in brands:
            if part == brand:
                continue 
            dist = levenshtein_distance(part, brand)
            if 1 <= dist <= 2: # Tighter threshold for accuracy
                lookalike_found = brand
                min_dist_found = dist
                break
        if lookalike_found:
            break
            
    flags["lookalike_brand"] = lookalike_found
    flags["lookalike_distance"] = min_dist_found
    if lookalike_found:
        score += 30
        reasons.append(f"Domain highly resembles known brand '{lookalike_found}'")

    # --- 8. HTTP vs HTTPS ---
    is_http = url.startswith("http://")
    flags["is_http"] = is_http
    if is_http:
        score += 15
        reasons.append("Connection uses unencrypted HTTP")

    # --- 9. SUSPICIOUS TLD CHECK ---
    high_risk_tlds = {
        ".xyz", ".top", ".club", ".online", ".site", ".live",
        ".tk", ".ml", ".ga", ".cf", ".gq", ".pw", ".zip", ".mov",
        ".md", ".ws", ".to", ".se", ".li", ".me", ".tv", ".cc", ".su"
    }
    domain_tld = "." + domain.rsplit(".", 1)[-1] if "." in domain else ""
    flags["suspicious_tld"] = domain_tld if domain_tld in high_risk_tlds else None
    if domain_tld in high_risk_tlds:
        score += 25
        reasons.append(f"Domain uses a high-risk TLD ({domain_tld})")

    # --- 10. PIRACY / PROXY KEYWORDS ---
    piracy_proxy_keywords = [
        "movie", "movies", "watch", "stream", "download", "free", "torrent",
        "mirror", "proxy", "bypass", "unblock", "flix", "putlocker", "series",
        "episode", "hdmovie", "watchfree", "movierulz", "123movies"
    ]
    domain_and_path = domain + path
    piracy_kw_found = [kw for kw in piracy_proxy_keywords if kw in domain_and_path]
    flags["piracy_proxy_keywords"] = piracy_kw_found
    if piracy_kw_found:
        score += 45
        reasons.append(f"High-risk piracy keywords: {', '.join(piracy_kw_found)}")

    # --- 11. NUMERIC DOMAIN PATTERN ---
    numeric_match = re.search(r'\d{1,}', domain)
    flags["has_numeric_pattern"] = bool(numeric_match)
    if numeric_match:
        score += 15
        reasons.append(f"Suspicious numeric pattern: '{numeric_match.group()}'")

    final_score = min(max(int(score), 0), 100)
    
    return {
        "score": final_score,
        "reasons": reasons,
        "flags": flags
    }
