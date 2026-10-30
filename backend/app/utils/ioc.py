"""
Unified IoC (Indicator of Compromise) Normalization & Validation Utility.
Standardizes URLs, Domains, IPv4/v6, Hashes, and Email Addresses into a reusable domain model.
"""

import re
import hashlib
from typing import Optional, Literal
from urllib.parse import urlparse
from pydantic import BaseModel

IOCType = Literal["url", "domain", "ipv4", "ipv6", "md5", "sha1", "sha256", "email", "unknown"]

IPV4_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)
IPV6_REGEX = re.compile(
    r"^(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$|^::1$"
)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)
MD5_REGEX = re.compile(r"^[a-fA-F0-9]{32}$")
SHA1_REGEX = re.compile(r"^[a-fA-F0-9]{40}$")
SHA256_REGEX = re.compile(r"^[a-fA-F0-9]{64}$")


class IOC(BaseModel):
    """
    Standardized Indicator of Compromise domain model.
    """
    raw_indicator: str
    normalized_value: str
    type: IOCType
    hash_key: str
    domain: Optional[str] = None
    ip: Optional[str] = None
    url_scheme: Optional[str] = None


class IOCNormalizer:
    """
    Normalizes raw string inputs into typed IOC models.
    """
    @staticmethod
    def detect_type(indicator: str) -> IOCType:
        val = indicator.strip()
        
        if IPV4_REGEX.match(val):
            return "ipv4"
        if IPV6_REGEX.match(val):
            return "ipv6"
        if MD5_REGEX.match(val):
            return "md5"
        if SHA1_REGEX.match(val):
            return "sha1"
        if SHA256_REGEX.match(val):
            return "sha256"
        if EMAIL_REGEX.match(val):
            return "email"
        if val.startswith(("http://", "https://", "ftp://")):
            return "url"
        if DOMAIN_REGEX.match(val):
            return "domain"
        if "/" in val or "." in val:
            return "url"
            
        return "unknown"

    @classmethod
    def normalize(cls, indicator: str, force_type: Optional[str] = None) -> IOC:
        val = indicator.strip()
        ioc_type = (force_type.lower() if force_type else cls.detect_type(val))  # type: ignore

        if ioc_type not in ["url", "domain", "ipv4", "ipv6", "md5", "sha1", "sha256", "email", "unknown"]:
            ioc_type = cls.detect_type(val)

        domain = None
        ip = None
        scheme = None
        norm_val = val

        if ioc_type == "url":
            if not val.startswith(("http://", "https://", "ftp://")):
                val = f"http://{val}"
            parsed = urlparse(val)
            scheme = parsed.scheme
            hostname = parsed.netloc.split(":")[0].lower()
            if IPV4_REGEX.match(hostname):
                ip = hostname
            else:
                domain = hostname
            norm_val = parsed.geturl().lower()
        elif ioc_type == "domain":
            norm_val = val.lower()
            domain = norm_val
        elif ioc_type in ["ipv4", "ipv6"]:
            norm_val = val.lower()
            ip = norm_val
        elif ioc_type == "email":
            norm_val = val.lower()
            if "@" in norm_val:
                domain = norm_val.split("@")[1]
        elif ioc_type in ["md5", "sha1", "sha256"]:
            norm_val = val.lower()

        hash_key = hashlib.sha256(f"{ioc_type}:{norm_val}".encode("utf-8")).hexdigest()

        return IOC(
            raw_indicator=indicator,
            normalized_value=norm_val,
            type=ioc_type,  # type: ignore
            hash_key=hash_key,
            domain=domain,
            ip=ip,
            url_scheme=scheme,
        )
