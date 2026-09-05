import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import HistGradientBoostingRegressor

MODEL_PATH = "resilix_flood_model.joblib"
DATA_PATH = "train_cleaned.parquet"
OUTPUT_IMG = "model_performance.png"
OUTPUT_METRICS = "metrics_summary.json"

print(f"Loading data from {DATA_PATH}...")
if os.path.exists(DATA_PATH):
    df = pd.read_parquet(DATA_PATH)
elif os.path.exists("train.csv"):
    df = pd.read_csv("train.csv")
else:
    raise FileNotFoundError("Neither 'train_cleaned.parquet' nor 'train.csv' found.")

# Sample 60,000 rows for rapid training & validation
sample_df = df.sample(n=min(60000, len(df)), random_state=42).reset_index(drop=True)
feature_cols = [c for c in sample_df.columns if c not in ["id", "FloodProbability"]]

X = sample_df[feature_cols]
y = sample_df["FloodProbability"]
if y.max() <= 1.0:
    y = y * 100.0  # Scale to 0-100%

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=42)

# Train or load model
if os.path.exists(MODEL_PATH):
    print(f"Loading existing model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)
else:
    print(f"Training fast baseline model and saving to {MODEL_PATH}...")
    model = HistGradientBoostingRegressor(max_iter=120, max_depth=6, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved: '{MODEL_PATH}'")

# Evaluate
print("Generating predictions on validation split...")
y_pred = model.predict(X_val)
rmse = float(np.sqrt(mean_squared_error(y_val, y_pred)))
r2 = float(r2_score(y_val, y_pred))

metrics = {
    "RMSE": round(rmse, 3),
    "R2_Score": round(r2, 4),
    "Validation_Samples": len(X_val)
}

with open(OUTPUT_METRICS, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"Validation Metrics: RMSE = {rmse:.3f} pts, R^2 = {r2:.4f}")

# Plotting dark-mode scatter plot for pitch deck
print(f"Exporting pitch plot to {OUTPUT_IMG}...")
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

ax.scatter(
    y_val, 
    y_pred, 
    alpha=0.3, 
    color="#38bdf8", 
    edgecolors="none", 
    s=12, 
    label="Sensor Telemetry Nodes"
)

# Reference diagonal (y = x)
min_val = min(float(y_val.min()), float(y_pred.min()))
max_val = max(float(y_val.max()), float(y_pred.max()))
ax.plot([min_val, max_val], [min_val, max_val], color="#f43f5e", linestyle="--", linewidth=2, label="Ideal Fit (y = x)")

ax.set_title("Resilix AI: Flood Risk Actual vs. Predicted", fontsize=13, fontweight="bold", pad=12, color="#ffffff")
ax.set_xlabel("Actual Risk Score (%)", fontsize=11, color="#cbd5e1")
ax.set_ylabel("Predicted Risk Score (%)", fontsize=11, color="#cbd5e1")
ax.grid(True, linestyle=":", alpha=0.3, color="#64748b")

annotation_text = f"$R^2$: {r2:.4f}\nRMSE: {rmse:.2f} pts"
ax.text(
    0.05, 0.88, 
    annotation_text, 
    transform=ax.transAxes, 
    fontsize=11, 
    fontfamily="monospace",
    verticalalignment="top", 
    bbox=dict(boxstyle="round,pad=0.6", facecolor="#0f172a", edgecolor="#e11d48", alpha=0.9)
)

ax.legend(loc="lower right", facecolor="#0f172a", edgecolor="#334155")
plt.tight_layout()
plt.savefig(OUTPUT_IMG)
plt.close()

print(f"Done! Created '{MODEL_PATH}', '{OUTPUT_IMG}', and '{OUTPUT_METRICS}'.")