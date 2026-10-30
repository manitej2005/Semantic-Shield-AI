"""
Email Authentication Evaluator analyzing SPF, DKIM, and DMARC headers.
"""

from typing import Dict
from app.schemas.email import EmailAuthResult, EmailHeaderEvidence


class EmailAuthEvaluator:
    """
    Evaluates SPF, DKIM, and DMARC verification headers.
    """

    @classmethod
    def evaluate(cls, headers: EmailHeaderEvidence) -> EmailAuthResult:
        spf_status = "None"
        dkim_status = "None"
        dmarc_status = "None"
        details: Dict[str, str] = {}

        auth_results_hdr = headers.x_headers.get("Authentication-Results") or headers.x_headers.get("X-Authentication-Results")
        received_spf_hdr = headers.x_headers.get("Received-SPF")

        # Evaluate SPF
        if received_spf_hdr:
            spf_lower = received_spf_hdr.lower()
            if "pass" in spf_lower:
                spf_status = "Pass"
            elif "fail" in spf_lower:
                spf_status = "Fail" if "softfail" not in spf_lower else "SoftFail"
            elif "neutral" in spf_lower:
                spf_status = "Neutral"
            details["Received-SPF"] = received_spf_hdr

        # Evaluate Authentication-Results header
        if auth_results_hdr:
            auth_lower = auth_results_hdr.lower()
            details["Authentication-Results"] = auth_results_hdr

            if "spf=pass" in auth_lower:
                spf_status = "Pass"
            elif "spf=fail" in auth_lower:
                spf_status = "Fail"
            elif "spf=softfail" in auth_lower:
                spf_status = "SoftFail"

            if "dkim=pass" in auth_lower:
                dkim_status = "Pass"
            elif "dkim=fail" in auth_lower:
                dkim_status = "Fail"

            if "dmarc=pass" in auth_lower:
                dmarc_status = "Pass"
            elif "dmarc=fail" in auth_lower:
                dmarc_status = "Fail"

        statuses = [spf_status, dkim_status, dmarc_status]

        # Auth Evaluation Rules:
        # 1. If all (spf, dkim, dmarc) are None -> auth_passed = False
        # 2. If any explicitly fail -> auth_passed = False
        # 3. If at least one passes (and none fail) -> auth_passed = True
        if all(s == "None" for s in statuses):
            auth_passed = False
        elif any(s in ["Fail", "SoftFail"] for s in statuses):
            auth_passed = False
        elif any(s == "Pass" for s in statuses):
            auth_passed = True
        else:
            auth_passed = False

        return EmailAuthResult(
            spf_status=spf_status,
            dkim_status=dkim_status,
            dmarc_status=dmarc_status,
            details=details,
            auth_passed=auth_passed,
        )
