import sys
import os
import joblib
import numpy as np
import json

import warnings
warnings.filterwarnings("ignore")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from app.url_features import extract_features

MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "model_simple.pkl")
SCALER_PATH = os.path.join(PROJECT_ROOT, "model", "scaler_simple.pkl")
FEATURE_LIST_PATH = os.path.join(PROJECT_ROOT, "model", "feature_list_simple.pkl")

# Load once
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_list = joblib.load(FEATURE_LIST_PATH)
except Exception as e:
    print(json.dumps({"error": f"Model load failed: {str(e)}"}))
    sys.exit(1)


def predict_simple(url):
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
        "probability": float(prob)
        # remove features in production (too heavy)
    }


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError("No URL provided")

        url = sys.argv[1]
        result = predict_simple(url)

        # ALWAYS JSON output
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)