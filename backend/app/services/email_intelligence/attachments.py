"""
Attachment Metadata Extractor & Macro/Executable Detector.
Calculates SHA256 and MD5 hashes without executing binary code.
"""

import hashlib
import os
from typing import List, Any
from app.schemas.email import AttachmentMetadata

SUSPICIOUS_EXTENSIONS = {
    ".exe", ".scr", ".vbs", ".js", ".bat", ".cmd", ".ps1", ".iso", ".img",
    ".docm", ".xlsm", ".pptm", ".jar", ".hta", ".cpl", ".wsf"
}

MACRO_EXTENSIONS = {".docm", ".xlsm", ".pptm", ".dotm", ".xltm"}


class AttachmentExtractor:
    """
    Extracts metadata, hashes, and macro indicators for email attachments.
    """

    @classmethod
    def process_attachment(
        cls, filename: str, content_bytes: bytes, mime_type: str = "application/octet-stream"
    ) -> AttachmentMetadata:
        ext = os.path.splitext(filename)[1].lower() if "." in filename else ""
        size = len(content_bytes)

        md5 = hashlib.md5(content_bytes).hexdigest()
        sha256 = hashlib.sha256(content_bytes).hexdigest()

        is_suspicious = ext in SUSPICIOUS_EXTENSIONS
        has_macros = ext in MACRO_EXTENSIONS

        return AttachmentMetadata(
            filename=filename,
            extension=ext,
            mime_type=mime_type,
            size_bytes=size,
            md5=md5,
            sha256=sha256,
            has_macros=has_macros,
            is_suspicious_extension=is_suspicious,
            is_password_protected=False,
            embedded_urls=[],
        )
