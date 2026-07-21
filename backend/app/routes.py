from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Analysis
from app.analyzer import PhishingAnalyzer

api_bp = Blueprint("api", __name__)
analyzer = PhishingAnalyzer()


@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0",
                    "timestamp": datetime.utcnow().isoformat()})


@api_bp.route("/analyze", methods=["POST"])
def analyze_email():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        email_content = file.read().decode("utf-8", errors="ignore")
        result = analyzer.analyze(email_content)

        analysis = Analysis(
            email_sender=result.get("sender"),
            email_subject=result.get("subject"),
            phishing_score=result.get("phishing_score"),
            is_phishing=result.get("is_phishing"),
            indicators_count=result.get("indicators_count"),
            critical_issues=result.get("critical_issues"),
            recommendation=result.get("recommendation"),
        )
        analysis.set_indicators(result.get("indicators", []))
        db.session.add(analysis)
        db.session.commit()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/history", methods=["GET"])
def get_history():
    limit = request.args.get("limit", 50, type=int)
    rows = Analysis.query.order_by(Analysis.created_at.desc()).limit(limit).all()
    return jsonify([r.to_dict() for r in rows])


@api_bp.route("/stats", methods=["GET"])
def get_stats():
    total = Analysis.query.count()
    phishing = Analysis.query.filter_by(is_phishing=True).count()
    return jsonify({
        "total_analyses": total,
        "phishing_count": phishing,
        "legitimate_count": total - phishing,
        "phishing_percentage": (phishing / total * 100) if total else 0,
    })