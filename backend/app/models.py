from app import db
from datetime import datetime
import json


class Analysis(db.Model):
    """One row per analyzed email. Defines the 'analyses' database table."""
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)
    email_sender = db.Column(db.String(255))
    email_subject = db.Column(db.String(255))
    phishing_score = db.Column(db.Float, default=0)
    is_phishing = db.Column(db.Boolean, default=False)
    indicators_count = db.Column(db.Integer, default=0)
    critical_issues = db.Column(db.Integer, default=0)
    indicators_json = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_indicators(self, indicators):
        self.indicators_json = json.dumps(indicators)

    def get_indicators(self):
        if self.indicators_json:
            return json.loads(self.indicators_json)
        return []

    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.email_sender,
            "subject": self.email_subject,
            "phishing_score": self.phishing_score,
            "is_phishing": self.is_phishing,
            "indicators_count": self.indicators_count,
            "critical_issues": self.critical_issues,
            "indicators": self.get_indicators(),
            "recommendation": self.recommendation,
            "timestamp": self.created_at.isoformat(),
        }