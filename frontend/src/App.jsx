import React, { useState, useEffect } from "react";
import axios from "axios";
import EmailUploader from "./components/EmailUploader";
import AnalysisReport from "./components/AnalysisReport";
import Dashboard from "./components/Dashboard";
import ThreatIndicator from "./components/ThreatIndicator";
import "./App.css";

function App() {
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

  const [currentView, setCurrentView] = useState("upload");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_URL}/api/stats`);
      setStats(res.data);
    } catch (err) {
      console.error("Error fetching stats:", err);
    }
  };

  const handleEmailUpload = async (file) => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post(`${API_URL}/api/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setAnalysis(res.data);
      setCurrentView("analysis");
      fetchStats();
    } catch (err) {
      setError(err.response?.data?.error || "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setAnalysis(null);
    setCurrentView("upload");
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔒 Phishing Email Scanner</h1>
        <p>Protect yourself from phishing threats</p>
      </header>

      <nav className="app-nav">
        <button className={currentView === "upload" ? "active" : ""}
                onClick={() => setCurrentView("upload")}>Analyze</button>
        <button className={currentView === "dashboard" ? "active" : ""}
                onClick={() => setCurrentView("dashboard")}>Dashboard</button>
      </nav>

      <main className="app-main">
        {currentView === "upload" && (
          <div className="upload-section">
            {error && <div className="error-message">{error}</div>}
            <EmailUploader onUpload={handleEmailUpload} loading={loading} />
          </div>
        )}

        {currentView === "analysis" && analysis && (
          <div className="analysis-section">
            <button className="btn-back" onClick={handleNewAnalysis}>
              ← Analyze Another Email
            </button>
            <ThreatIndicator score={analysis.phishing_score} />
            <AnalysisReport analysis={analysis} />
          </div>
        )}

        {currentView === "dashboard" && <Dashboard stats={stats} />}
      </main>

      <footer className="app-footer">
        <p>🔐 Emails are analyzed for security education.</p>
      </footer>
    </div>
  );
}

export default App;