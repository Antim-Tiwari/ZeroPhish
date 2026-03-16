"""
train_model_simple.py
----------------------
Trains a SIMPLE phishing detection ML model based ONLY on
23 classical URL features from the Kaggle dataset.

Input CSV must contain the Kaggle columns:
 - All 23 URL-based features
 - CLASS_LABEL
 - id (ignored)

This produces:
 - model/model_simple.pkl
 - model/scaler_simple.pkl
 - model/feature_list_simple.pkl
"""

import pandas as pd
import numpy as np
import argparse
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ------------------------------------------------------------
# DEFINE THE 23 URL-ONLY FEATURES (MUST MATCH url_features.py)
# ------------------------------------------------------------
FEATURE_COLUMNS = [
    "NumDots",
    "SubdomainLevel",
    "PathLevel",
    "UrlLength",
    "NumDash",
    "NumDashInHostname",
    "AtSymbol",
    "TildeSymbol",
    "NumUnderscore",
    "NumPercent",
    "NumQueryComponents",
    "NumAmpersand",
    "NumHash",
    "NumNumericChars",
    "NoHttps",
    "IpAddress",
    "DomainInSubdomains",
    "DomainInPaths",
    "HttpsInHostname",
    "HostnameLength",
    "PathLength",
    "QueryLength",
    "DoubleSlashInPath",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to Kaggle CSV")
    parser.add_argument("--out-dir", default="model", help="Where to save model files")
    args = parser.parse_args()

    # ------------------------------
    # Load dataset
    # ------------------------------
    print("[INFO] Loading dataset...")
    df = pd.read_csv(args.input)

    if "CLASS_LABEL" not in df.columns:
        raise ValueError("CSV does not contain CLASS_LABEL column")

    # Drop ID field if present
    if "id" in df.columns:
        df = df.drop(columns=["id"])

    # Validate feature columns
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required feature column: {col}")

    X = df[FEATURE_COLUMNS].values
    y = df["CLASS_LABEL"].values

    # ------------------------------
    # Train-test split
    # ------------------------------
    print("[INFO] Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ------------------------------
    # Scaling
    # ------------------------------
    print("[INFO] Scaling data...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ------------------------------
    # Train model
    # ------------------------------
    print("[INFO] Training Random Forest model (simple)...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)

    # ------------------------------
    # Evaluate
    # ------------------------------
    print("[INFO] Evaluating...")
    preds = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, preds)

    print("\n=== SIMPLE MODEL ACCURACY ===")
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds))

    # ------------------------------
    # Save model
    # ------------------------------
    os.makedirs(args.out_dir, exist_ok=True)

    joblib.dump(model, f"{args.out_dir}/model_simple.pkl")
    joblib.dump(scaler, f"{args.out_dir}/scaler_simple.pkl")
    joblib.dump(FEATURE_COLUMNS, f"{args.out_dir}/feature_list_simple.pkl")

    print("\n[INFO] SIMPLE MODEL SAVED:")
    print("  model/model_simple.pkl")
    print("  model/scaler_simple.pkl")
    print("  model/feature_list_simple.pkl")


if __name__ == "__main__":
    main()
