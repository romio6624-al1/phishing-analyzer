import React from "react";

function Dashboard({ stats }) {
  return (
    <div className="dashboard">
      <h2>Analytics Dashboard</h2>
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{stats.total_analyses}</div>
            <div className="stat-label">Total Analyses</div>
          </div>
          <div className="stat-card danger">
            <div className="stat-value">{stats.phishing_count}</div>
            <div className="stat-label">Phishing Detected</div>
          </div>
          <div className="stat-card safe">
            <div className="stat-value">{stats.legitimate_count}</div>
            <div className="stat-label">Legitimate Emails</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">
              {stats.phishing_percentage ? stats.phishing_percentage.toFixed(1) : 0}%
            </div>
            <div className="stat-label">Phishing Rate</div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;