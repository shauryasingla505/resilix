import os
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

def generate_synthetic_data(num_samples=5000):
    """
    Fallback data generator so you can train and export models immediately.
    """
    np.random.seed(42)
    rainfall_mm_hr = np.random.uniform(0, 150, num_samples)       # Rainfall (mm/hr)
    elevation_m = np.random.uniform(5, 100, num_samples)          # Elevation (meters)
    elevation_gradient = np.random.uniform(0.1, 5.0, num_samples) # Slope gradient
    drain_capacity_lps = np.random.uniform(10, 50, num_samples)   # Drain capacity (L/s)
    
    # Calculate water level (0m to 5m)
    water_level_m = (
        0.035 * rainfall_mm_hr 
        - 0.15 * elevation_gradient 
        - 0.02 * (elevation_m / 10) 
        - 0.04 * drain_capacity_lps 
        + np.random.normal(0, 0.2, num_samples)
    )
    water_level_m = np.clip(water_level_m, 0.0, 5.0)
    
    # Calculate risk score (0 to 100)
    risk_score = np.clip((water_level_m / 5.0) * 100 + np.random.normal(0, 2, num_samples), 0, 100)
    
    return pd.DataFrame({
        'rainfall_mm_hr': rainfall_mm_hr,
        'elevation_m': elevation_m,
        'elevation_gradient': elevation_gradient,
        'drain_capacity_lps': drain_capacity_lps,
        'water_level_m': water_level_m,
        'risk_score': risk_score
    })

def load_data():
    """
    Loads Person B's cleaned CSV if available, otherwise defaults to synthetic data.
    """
    csv_filename = "cleaned_flood_data.csv"
    if os.path.exists(csv_filename):
        print(f"[*] Found '{csv_filename}'. Loading dataset processed by Person B...")
        df = pd.read_csv(csv_filename)
    else:
        print(f"[!] '{csv_filename}' not found yet. Generating synthetic data for instant testing...")
        df = generate_synthetic_data()
    return df

def train_models():
    df = load_data()
    
    # Select feature columns and targets
    feature_cols = ['rainfall_mm_hr', 'elevation_m', 'elevation_gradient', 'drain_capacity_lps']
    X = df[feature_cols]
    y_water = df['water_level_m']
    y_risk = df['risk_score']
    
    # Split dataset
    X_train, X_test, y_w_train, y_w_test = train_test_split(X, y_water, test_size=0.2, random_state=42)
    _, _, y_r_train, y_r_test = train_test_split(X, y_risk, test_size=0.2, random_state=42)
    
    # 1. Train Water Level Model
    print("[*] Training XGBoost Regressor for Water Level Prediction...")
    water_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    water_model.fit(X_train, y_w_train)
    
    # 2. Train Risk Score Model
    print("[*] Training XGBoost Regressor for Hazard Risk Score...")
    risk_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    risk_model.fit(X_train, y_r_train)
    
    # Evaluate
    w_preds = water_model.predict(X_test)
    r_preds = risk_model.predict(X_test)
    
    print("\n--- MODEL EVALUATION ---")
    print(f" -> Water Level Model R2 Score: {r2_score(y_w_test, w_preds):.4f}")
    print(f" -> Risk Score Model R2 Score:  {r2_score(y_r_test, r_preds):.4f}\n")
    
    # Export trained models as pickle files
    with open("flood_water_model.pkl", "wb") as f:
        pickle.dump(water_model, f)
    with open("flood_risk_model.pkl", "wb") as f:
        pickle.dump(risk_model, f)
        
    print("[+] Models exported successfully:")
    print("    - flood_water_model.pkl")
    print("    - flood_risk_model.pkl")

if __name__ == "__main__":
    train_models()