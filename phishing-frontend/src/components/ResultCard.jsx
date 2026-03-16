import React from "react";
import "./ResultCard.css";

export default function ResultCard({ result, probability }) {
  const isPhishing = result === "Phishing";

  return (
    <div className={`result-card ${isPhishing ? "danger" : "safe"}`}>
      <h2>
        {isPhishing ? "Phishing Website" : "Safe Website"}
      </h2>

      <p className="confidence">
        Confidence Score:{" "}
        <strong>{(probability * 100).toFixed(2)}%</strong>
      </p>
    </div>
  );
}
