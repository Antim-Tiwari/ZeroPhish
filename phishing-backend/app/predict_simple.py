"""
predict_simple.py
-----------------
Loads the SIMPLE (URL-only) ML model and predicts phishing vs legit.
"""

import sys
import os
import joblib
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

# Loading the simple URL-only feature extractor
from app.url_features import extract_features


# Load Model and Scaler and Feature List (combination)
MODEL_PATH = "model/model_simple.pkl"
SCALER_PATH = "model/scaler_simple.pkl"
FEATURE_LIST_PATH = "model/feature_list_simple.pkl"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_list = joblib.load(FEATURE_LIST_PATH)
except Exception as e:
    print({"error": f"Failed to load simple model: {e}"})
    sys.exit(1)

def predict_simple(url):
    """Predict using the SIMPLE (URL-only) model."""
    vector = extract_features(url)

    if len(vector) != len(feature_list):
        raise ValueError(
            f"Feature mismatch: expected {len(feature_list)}, got {len(vector)}"
        )

    X = np.array(vector).reshape(1, -1)
    X_scaled = scaler.transform(X)

    pred = model.predict(X_scaled)[0]
    prob = model.predict_proba(X_scaled)[0][pred]

    label = "Phishing" if pred == 1 else "Legit"

    return {
        "mode": "simple",
        "url": url,
        "result": label,
        "probability": float(prob),
        "features": dict(zip(feature_list, vector))
    }

import json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python predict_simple.py <url>"}))
        sys.exit(1)

    url = sys.argv[1]
    result = predict_simple(url)
    print(json.dumps(result))