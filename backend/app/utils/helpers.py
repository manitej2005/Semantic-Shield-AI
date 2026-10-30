"""
General utility functions and string helpers.
"""

import urllib.parse
from typing import Optional


def sanitize_url(url: str) -> str:
    """
    Ensures a clean, normalized URL format with scheme.
    """
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url


def extract_base_domain(url: str) -> str:
    """
    Extracts netloc host domain from URL string.
    """
    parsed = urllib.parse.urlparse(sanitize_url(url))
    domain = parsed.netloc.lower()
    if ":" in domain:
        domain = domain.split(":")[0]
    return domain
