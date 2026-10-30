import urllib.parse
import whois
import datetime
import concurrent.futures

# In-memory cache to prevent repeated WHOIS lookups for the same domain
# Format: { "domain.com": { "score": ..., "reasons": ..., ... } }
_DOMAIN_CACHE = {}

def extract_domain(url: str) -> str:
    """Extracts the base domain from a URL to be used for WHOIS lookup."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    
    # Remove port if present
    if ":" in domain:
        domain = domain.split(":")[0]

    return domain

def do_whois_lookup(domain: str):
    """Wrapper function to execute whois lookup for ThreadPoolExecutor."""
    return whois.whois(domain)

def analyze_domain(url: str) -> dict:
    """
    Checks how old the domain is using WHOIS data to determine phishing risk.
    New domains (<30 days) are high risk. Results are cached and timeout at 10s.
    """
    domain = extract_domain(url)
    
    # 1. Check in-memory cache first
    if domain in _DOMAIN_CACHE:
        return _DOMAIN_CACHE[domain]
        
    # 2. Setup default fallback result if lookup fails, times out, or has no date
    result = {
        "score": 30,
        "reasons": ["Domain registration data unavailable — treating as moderately cautious"],
        "domain_age_days": None,
        "creation_date": None,
        "registrar": None
    }
    
    # 3. Execute WHOIS lookup with a strict maximum 5-second timeout
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(do_whois_lookup, domain)
            w = future.result(timeout=5)
            
        if w:
            # Safely extract registrar (python-whois sometimes returns a list)
            registrar = getattr(w, 'registrar', None)
            if isinstance(registrar, list) and registrar:
                result["registrar"] = str(registrar[0])
            elif registrar:
                result["registrar"] = str(registrar)
                
            # Safely process the creation date
            creation_date = getattr(w, 'creation_date', None)
            earliest_date = None
            
            if creation_date:
                if isinstance(creation_date, list):
                    # Filter out non-datetime elements, sort, and select the earliest
                    dates = [d for d in creation_date if isinstance(d, datetime.datetime)]
                    if dates:
                        earliest_date = min(dates)
                elif isinstance(creation_date, datetime.datetime):
                    earliest_date = creation_date
                    
            if earliest_date:
                # Format creation date as ISO 8601 string for reliable JSON serialization
                result["creation_date"] = earliest_date.isoformat()
                
                # Convert timezone-aware datetimes to naive to prevent subtraction errors
                if earliest_date.tzinfo is not None:
                    earliest_date = earliest_date.replace(tzinfo=None)
                    
                now = datetime.datetime.now()
                delta = now - earliest_date
                age_days = max(0, delta.days)
                
                result["domain_age_days"] = age_days
                
                # 4. Apply scoring logic strictly mandated by the rules
                if age_days < 7:
                    result["score"] = 95
                    result["reasons"] = ["Domain registered less than a week ago — extremely high risk"]
                elif age_days < 30:
                    result["score"] = 75
                    result["reasons"] = ["Domain is less than 30 days old — common phishing indicator"]
                elif age_days <= 90:
                    result["score"] = 40
                    result["reasons"] = ["Domain is relatively new (under 3 months)"]
                else:
                    result["score"] = 5
                    result["reasons"] = []
                    
    except Exception:
        # If any error fires (TimeoutError, Network issue, parsing error), 
        # it gracefully falls back to the default result (score 30, reason: unavailable)
        pass
        
    # 5. Store the calculated result into the cache
    _DOMAIN_CACHE[domain] = result
    
    return result
