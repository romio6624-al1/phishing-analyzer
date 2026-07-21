import React from "react";

function ThreatIndicator({ score }) {
  let status, color, icon;
  if (score >= 80) { status = "LIKELY PHISHING"; color = "danger"; icon = "🚨"; }
  else if (score >= 60) { status = "SUSPICIOUS"; color = "warning"; icon = "⚠️"; }
  else if (score >= 40) { status = "POSSIBLY SUSPICIOUS"; color = "caution"; icon = "❓"; }
  else { status = "LIKELY LEGITIMATE"; color = "safe"; icon = "✅"; }

  return (
    <div className={`threat-indicator ${color}`}>
      <div className="indicator-icon">{icon}</div>
      <div className="indicator-content">
        <div className="threat-status">{status}</div>
        <div className="threat-score">
          <div className="score-bar">
            <div className="score-fill" style={{ width: `${score}%` }}></div>
          </div>
          <div className="score-value">{score}% Phishing Probability</div>
        </div>
      </div>
    </div>
  );
}

export default ThreatIndicator;