"""
Email Heuristics Engine detecting Display Name Spoofing, Reply-To mismatches, and social engineering themes.
"""

import re
from typing import List, Optional
from app.schemas.email import EmailHeaderEvidence, EmailAuthResult, EmailHeuristicsResult

URGENCY_KEYWORDS = [
    "urgent", "immediate action", "account suspended", "24 hours", "15 minutes",
    "unauthorized access", "terminate", "final notice", "critical alert"
]

FINANCIAL_KEYWORDS = [
    "wire transfer", "invoice", "payment", "bank account", "payroll", "direct deposit",
    "remittance", "financial department", "w-2", "tax form"
]

CREDENTIAL_KEYWORDS = [
    "password reset", "verify credentials", "mfa reset", "2fa verification",
    "login immediately", "session expired", "security update", "update password"
]

BRAND_PATTERNS = {
    "Microsoft 365": ["microsoft", "office365", "outlook", "entra", "azure"],
    "Google Workspace": ["google", "gmail", "workspace"],
    "Banking / Financial": ["bank", "chase", "wells fargo", "citi", "payroll"],
    "HR / Personnel": ["human resources", "hr department", "benefits", "employee portal"],
}


class EmailHeuristicsEngine:
    """
    Evaluates email header and body heuristics to detect social engineering and spoofing.
    """

    @classmethod
    def evaluate(
        cls,
        headers: EmailHeaderEvidence,
        auth: EmailAuthResult,
        text_body: str,
        html_body: str,
    ) -> EmailHeuristicsResult:
        findings: List[str] = []
        score = 0

        combined_text = f"{headers.subject} {text_body} {html_body}".lower()

        # 1. Display Name Spoofing Check
        display_name_spoofing = False
        if headers.display_name:
            # Check if display name contains executive keywords or email addresses
            for brand_key, keywords in BRAND_PATTERNS.items():
                if any(kw in headers.display_name.lower() for kw in keywords):
                    if not any(kw in headers.from_address.lower() for kw in keywords):
                        display_name_spoofing = True
                        findings.append(f"Display Name Spoofing: Claims '{headers.display_name}' but sent from '{headers.from_address}'")
                        score += 35
                        break

        # 2. Reply-To Mismatch Check
        reply_to_mismatch = False
        if headers.reply_to and headers.from_address:
            reply_domain = headers.reply_to.split("@")[-1].lower() if "@" in headers.reply_to else ""
            from_domain = headers.from_address.split("@")[-1].lower() if "@" in headers.from_address else ""

            if reply_domain and from_domain and reply_domain != from_domain:
                reply_to_mismatch = True
                findings.append(f"Reply-To Mismatch: From domain '{from_domain}' differs from Reply-To domain '{reply_domain}'")
                score += 30

        # 3. Return-Path Mismatch Check
        return_path_mismatch = False
        if headers.return_path and headers.from_address:
            rp_domain = headers.return_path.strip("<>").split("@")[-1].lower() if "@" in headers.return_path else ""
            from_domain = headers.from_address.split("@")[-1].lower() if "@" in headers.from_address else ""

            if rp_domain and from_domain and rp_domain != from_domain:
                return_path_mismatch = True
                findings.append(f"Return-Path Mismatch: Return-Path '{headers.return_path}' differs from From address '{headers.from_address}'")
                score += 20

        # 4. Brand Impersonation Check
        detected_brand: Optional[str] = None
        for brand, keywords in BRAND_PATTERNS.items():
            if any(kw in combined_text for kw in keywords):
                from_dom = headers.from_address.split("@")[-1].lower() if "@" in headers.from_address else ""
                if not any(kw in from_dom for kw in keywords):
                    detected_brand = brand
                    findings.append(f"Brand Impersonation Threat: Email text references '{brand}' but originates from external domain '{from_dom}'")
                    score += 30
                    break

        # 5. Urgency Detection
        urgency_detected = any(kw in combined_text for kw in URGENCY_KEYWORDS)
        if urgency_detected:
            findings.append("High-pressure Urgency Language Detected")
            score += 15

        # 6. Financial Request Detection
        financial_detected = any(kw in combined_text for kw in FINANCIAL_KEYWORDS)
        if financial_detected:
            findings.append("Financial Request / Wire Transfer / Invoice Theme Detected")
            score += 20

        # 7. Credential Request Detection
        credential_detected = any(kw in combined_text for kw in CREDENTIAL_KEYWORDS)
        if credential_detected:
            findings.append("Credential Harvesting / Password Reset Theme Detected")
            score += 25

        # 8. Invoice Theme
        invoice_theme = "invoice" in combined_text or "receipt" in combined_text

        # 9. MFA Reset Theme
        mfa_theme = "mfa" in combined_text or "2fa" in combined_text or "token" in combined_text

        # 10. Failed Auth score penalty
        if not auth.auth_passed:
            findings.append("Email Authentication Failure (SPF/DKIM/DMARC flags)")
            score += 25

        final_risk_score = min(100, score)

        return EmailHeuristicsResult(
            display_name_spoofing=display_name_spoofing,
            reply_to_mismatch=reply_to_mismatch,
            return_path_mismatch=return_path_mismatch,
            unicode_spoofing=False,
            brand_impersonation=detected_brand,
            urgency_detected=urgency_detected,
            financial_request_detected=financial_detected,
            credential_request_detected=credential_detected,
            invoice_theme_detected=invoice_theme,
            mfa_reset_theme_detected=mfa_theme,
            heuristics_risk_score=final_risk_score,
            findings=findings,
        )
