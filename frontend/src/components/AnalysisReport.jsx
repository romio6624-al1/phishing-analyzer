import React from "react";

function AnalysisReport({ analysis }) {
  return (
    <div className="analysis-report">
      <div className="report-header">
        <h2>Email Analysis Report</h2>
        <div className="report-meta">
          <p><strong>From:</strong> {analysis.sender}</p>
          <p><strong>Subject:</strong> {analysis.subject}</p>
        </div>
      </div>

      <div className="report-recommendation">
        <h3>Recommendation</h3>
        <p>{analysis.recommendation}</p>
      </div>

      <div className="report-summary">
        <div className="summary-item">
          <span>Total Indicators</span><strong>{analysis.indicators_count}</strong>
        </div>
        <div className="summary-item critical">
          <span>Critical Issues</span><strong>{analysis.critical_issues}</strong>
        </div>
      </div>

      {analysis.indicators && analysis.indicators.length > 0 && (
        <div className="report-indicators">
          <h3>Security Findings</h3>
          {["critical", "high", "medium", "low"].map((sev) => {
            const items = analysis.indicators.filter((i) => i.severity === sev);
            if (items.length === 0) return null;
            return (
              <div key={sev} className={`indicator-group ${sev}`}>
                <h4>{sev.toUpperCase()} Severity</h4>
                {items.map((ind, idx) => (
                  <div key={idx} className="indicator-item">
                    <div className="indicator-title">{ind.title}</div>
                    <div className="indicator-desc">{ind.description}</div>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default AnalysisReport;