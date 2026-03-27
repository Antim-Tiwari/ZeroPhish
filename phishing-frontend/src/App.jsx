import React, { useState } from "react";
import ResultCard from "./components/ResultCard";
import "./App.css";

export default function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function scanUrl() {
    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("https://zerophish-6vma.onrender.com", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch {
      setError("Backend not reachable");
    }

    setLoading(false);
  }

  return (
    <div className="app-container">
      <h1 className="title">Phishing Fast Scan</h1>

      <div className="input-block">
        <input
          type="text"
          placeholder="Enter website URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={scanUrl} disabled={loading}>
          {loading ? "Scanning..." : "Scan"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {result && (
        <ResultCard
          result={result.result}
          probability={result.probability}
        />
      )}
    </div>
  );
}
