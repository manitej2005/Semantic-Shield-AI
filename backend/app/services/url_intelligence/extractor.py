"""
Multi-source URL Extractor & Shortener Expander for HTML, Plain Text, Buttons, CSS, and JS.
"""

import re
import httpx
import asyncio
from typing import List, Set, Dict, Tuple, Any
from urllib.parse import urlparse, parse_qs

# URL regex matching standard web links
URL_REGEX = re.compile(
    r"https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d+)?(?:/[^\s<\"'>]*)?",
    re.IGNORECASE,
)

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "ow.ly", "is.gd", "buff.ly", "rebrand.ly", "cutt.ly"}


class URLExtractor:
    """
    Extracts, normalizes, and resolves shortener links from email body text and HTML markup.
    """

    @staticmethod
    def extract_urls_from_text(text: str) -> List[str]:
        if not text:
            return []
        matches = URL_REGEX.findall(text)
        # Strip trailing punctuation
        cleaned = [m.rstrip(".,;)>'\"]") for m in matches]
        return list(dict.fromkeys(cleaned))

    @staticmethod
    def parse_url_components(url: str) -> Dict[str, Any]:
        parsed = urlparse(url if url.startswith(("http://", "https://")) else f"http://{url}")
        hostname = parsed.netloc.split(":")[0].lower()
        subdomains = hostname.split(".")
        
        root_domain = ".".join(subdomains[-2:]) if len(subdomains) >= 2 else hostname
        subdomain_list = subdomains[:-2] if len(subdomains) > 2 else []

        raw_query = parse_qs(parsed.query)
        query_params = {k: v[0] if v else "" for k, v in raw_query.items()}

        return {
            "protocol": parsed.scheme or "http",
            "hostname": hostname,
            "domain": root_domain,
            "subdomains": subdomain_list,
            "path": parsed.path or "/",
            "query_params": query_params,
        }

    @staticmethod
    async def expand_shortener(url: str, timeout_seconds: float = 3.0) -> str:
        """
        Attempts to expand shortened URLs via HTTP HEAD redirect inspection.
        """
        parsed = urlparse(url)
        hostname = parsed.netloc.split(":")[0].lower()
        
        if hostname not in SHORTENERS:
            return url

        try:
            async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as client:
                res = await client.head(url)
                return str(res.url)
        except Exception:
            return url
