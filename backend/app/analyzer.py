import re
from email import message_from_string


class PhishingAnalyzer:
    """Analyzes an email and returns a phishing score plus a list of reasons."""

    def __init__(self):
        self.phishing_indicators = []
        self.score = 0
        self.severity_levels = {"critical": 5, "high": 3, "medium": 2, "low": 1}

    def analyze(self, email_content):
        self.phishing_indicators = []
        self.score = 0

        try:
            msg = message_from_string(email_content)
        except Exception as e:
            return {"error": f"Failed to parse email: {str(e)}",
                    "is_phishing": None, "phishing_score": 0}

        self._check_sender(msg)
        self._check_urls(msg)
        self._check_content(msg)
        self._check_attachments(msg)
        self._check_urgency(msg)
        self._check_authentication(msg)

        phishing_score = min(100, self.score * 5)
        is_phishing = phishing_score > 40

        return {
            "sender": msg.get("From", "Unknown"),
            "subject": msg.get("Subject", "No Subject"),
            "phishing_score": round(phishing_score, 1),
            "is_phishing": is_phishing,
            "indicators": self.phishing_indicators,
            "indicators_count": len(self.phishing_indicators),
            "critical_issues": len([i for i in self.phishing_indicators
                                    if i["severity"] == "critical"]),
            "recommendation": self._get_recommendation(phishing_score),
        }

    def _check_sender(self, msg):
        from_header = msg.get("From", "")
        reply_to = msg.get("Reply-To", "")
        if not from_header:
            self._add("Missing From Header", "Email lacks a sender.", "critical")
            return
        from_email = self._extract_email(from_header)
        reply_email = self._extract_email(reply_to)
        if reply_to and reply_email and reply_email != from_email:
            self._add("Sender Mismatch",
                      f"Reply-To ({reply_email}) differs from From ({from_email}).",
                      "high")
        if "@" in from_email:
            domain = from_email.split("@")[1]
            if self._suspicious_domain(domain):
                self._add("Suspicious Domain",
                          f"Domain {domain} looks suspicious.", "high")

    def _check_urls(self, msg):
        body = self._body(msg)
        for url in re.findall(r"https?://[^\s\)\"<>']+", body):
            self._check_one_url(url)

    def _check_one_url(self, url):
        if len(url) > 100:
            self._add("Long URL", "Very long URL may hide its destination.", "medium")
        for pattern in [r"amaz[0o]n", r"paypa[l1]", r"goog[l1]e",
                        r"faceb[0o]ok", r"micr[0o]soft"]:
            if re.search(pattern, url, re.IGNORECASE):
                self._add("Typosquatting", "URL mimics a well-known brand.", "high")
        if re.search(r"https?://\d+\.\d+\.\d+\.\d+", url):
            self._add("IP Address URL", "URL uses a raw IP instead of a domain.", "high")
        if any(s in url.lower() for s in ["bit.ly", "tinyurl", "goo.gl", "ow.ly"]):
            self._add("URL Shortener", "Shortened URL hides its destination.", "medium")

    def _check_content(self, msg):
        body = self._body(msg).lower()
        for pattern in [r"password.*confirm", r"verify.*password",
                        r"confirm.*identity", r"provide.*credit.*card"]:
            if re.search(pattern, body):
                self._add("Credential Request",
                          "Email asks for sensitive information.", "critical")
                break
        urgency = ["verify immediately", "confirm now", "act immediately",
                   "urgent action", "limited time", "account will be closed",
                   "suspended account", "unusual activity detected"]
        n = sum(1 for u in urgency if u in body)
        if n > 0:
            self._add("Urgency Language", f"Uses {n} pressure phrase(s).",
                      "high" if n > 2 else "medium")

    def _check_attachments(self, msg):
        dangerous = [".exe", ".scr", ".bat", ".cmd", ".jar", ".msi"]
        if msg.is_multipart():
            for part in msg.walk():
                fn = part.get_filename()
                if not fn:
                    continue
                low = fn.lower()
                for ext in dangerous:
                    if low.endswith(ext):
                        self._add("Dangerous Attachment",
                                  f"Attachment {fn} may be malicious.", "critical")
                if re.search(r"\.\w+\.(exe|scr|bat|com)$", low):
                    self._add("Double Extension",
                              f"Attachment {fn} hides its true type.", "critical")

    def _check_urgency(self, msg):
        subject = msg.get("Subject", "").lower()
        if any(w in subject for w in ["urgent", "immediate", "verify",
                                      "confirm", "suspended", "locked", "alert"]):
            self._add("Urgent Subject", "Subject line creates urgency.", "low")

    def _check_authentication(self, msg):
        auth = msg.get("Authentication-Results", "")
        if not auth:
            self._add("No Auth Headers", "Missing SPF/DKIM/DMARC results.", "medium")
        elif "fail" in auth.lower():
            self._add("Auth Failed", "Email failed authentication checks.", "high")

    def _add(self, title, desc, severity):
        self.phishing_indicators.append(
            {"title": title, "description": desc, "severity": severity})
        self.score += self.severity_levels.get(severity, 1)

    def _body(self, msg):
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() in ["text/plain", "text/html"]:
                    try:
                        body += part.get_payload(decode=True).decode(errors="ignore")
                    except Exception:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            except Exception:
                body = msg.get_payload()
        return body or ""

    def _extract_email(self, header):
        m = re.search(r"[\w\.-]+@[\w\.-]+", header)
        return m.group(0) if m else ""

    def _suspicious_domain(self, domain):
        return any(re.search(p, domain) for p in
                   [r"\d{1,3}\.\d{1,3}", r"temp.*mail", r"guerrillamail"])

    def _get_recommendation(self, score):
        if score >= 80:
            return "LIKELY PHISHING — do not click links or open attachments. Report it."
        if score >= 60:
            return "SUSPICIOUS — verify the sender through another channel."
        if score >= 40:
            return "POSSIBLY SUSPICIOUS — hover over links before clicking."
        return "LIKELY LEGITIMATE — but always stay cautious."