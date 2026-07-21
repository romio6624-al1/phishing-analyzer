import React, { useState } from "react";

function EmailUploader({ onUpload, loading }) {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
    else if (e.type === "dragleave") setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) onUpload(e.dataTransfer.files[0]);
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) onUpload(e.target.files[0]);
  };

  return (
    <div className="uploader">
      <div className={`upload-area ${dragActive ? "active" : ""}`}
           onDragEnter={handleDrag} onDragLeave={handleDrag}
           onDragOver={handleDrag} onDrop={handleDrop}>
        <div className="upload-content">
          <div className="upload-icon">📧</div>
          <h2>Upload Email for Analysis</h2>
          <p>Drag and drop an email file here, or click to select</p>
          <p className="supported">Supported: EML, MSG, TXT</p>
          <input type="file" onChange={handleChange} accept=".eml,.msg,.txt"
                 disabled={loading} id="file-input" style={{ display: "none" }} />
          <label htmlFor="file-input" className="upload-label">
            {loading ? "Analyzing..." : "Choose File"}
          </label>
        </div>
      </div>
    </div>
  );
}

export default EmailUploader;