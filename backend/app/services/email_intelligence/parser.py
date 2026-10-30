"""
RFC822 and MIME Email Parser.
Extracts headers, body text, HTML markup, received chain, and embedded content.
"""

import email
from email import policy
from email.parser import BytesParser, Parser
from typing import Dict, Any, List, Tuple, Optional
from app.schemas.email import EmailHeaderEvidence


class EmailParser:
    """
    Parses raw RFC822 string or bytes into structured headers and body contents.
    """

    @classmethod
    def parse_raw_mime(cls, raw_email_str_or_bytes: Any) -> Tuple[EmailHeaderEvidence, str, str]:
        """
        Parses raw email content returning (headers, plain_text_body, html_body).
        """
        if isinstance(raw_email_str_or_bytes, bytes):
            msg = BytesParser(policy=policy.default).parsebytes(raw_email_str_or_bytes)
        else:
            msg = Parser(policy=policy.default).parsestr(str(raw_email_str_or_bytes))

        # Extract Headers
        subject = msg.get("subject", "")
        date = msg.get("date")
        message_id = msg.get("message-id")
        from_hdr = msg.get("from", "")
        sender_hdr = msg.get("sender")
        to_hdr = msg.get_all("to", [])
        cc_hdr = msg.get_all("cc", [])
        reply_to = msg.get("reply-to")
        return_path = msg.get("return-path")
        received_chain = msg.get_all("received", [])
        user_agent = msg.get("user-agent")
        mailer = msg.get("x-mailer")
        priority = msg.get("x-priority") or msg.get("importance")

        # Parse Display Name vs Email Address
        from_address = from_hdr
        display_name = ""
        if "<" in from_hdr and ">" in from_hdr:
            parts = from_hdr.split("<")
            display_name = parts[0].strip(" \"'")
            from_address = parts[1].split(">")[0].strip()

        # Collect X-Headers and Auth Headers
        x_headers = {}
        for k, v in msg.items():
            if k.lower().startswith("x-") or k.lower() in ["authentication-results", "received-spf"]:
                x_headers[k] = str(v)

        headers_obj = EmailHeaderEvidence(
            subject=subject,
            date=str(date) if date else None,
            message_id=str(message_id) if message_id else None,
            from_header=from_hdr,
            from_address=from_address,
            display_name=display_name,
            sender_address=sender_hdr,
            to_addresses=[str(t) for t in to_hdr] if to_hdr else [],
            cc_addresses=[str(c) for c in cc_hdr] if cc_hdr else [],
            reply_to=reply_to,
            return_path=return_path,
            received_chain=[str(r) for r in received_chain],
            x_headers=x_headers,
            user_agent=user_agent,
            mailer=mailer,
            priority=priority,
        )

        # Extract Body Parts
        text_body = ""
        html_body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    continue

                if content_type == "text/plain" and not text_body:
                    try:
                        text_body = part.get_content()
                    except Exception:
                        pass
                elif content_type == "text/html" and not html_body:
                    try:
                        html_body = part.get_content()
                    except Exception:
                        pass
        else:
            content_type = msg.get_content_type()
            try:
                content = msg.get_content()
                if content_type == "text/html":
                    html_body = content
                else:
                    text_body = content
            except Exception:
                text_body = str(msg.get_payload())

        return headers_obj, text_body or "", html_body or ""
