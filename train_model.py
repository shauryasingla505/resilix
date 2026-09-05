import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb

# 1. Load the cleaned training dataset
df = pd.read_csv("train_dataset.csv")

# 2. Select features matching dataset parameters
feature_cols = [
    "MonsoonIntensity",
    "TopographyDrainage",
    "RiverManagement",
    "Deforestation",
    "Urbanization",
    "ClimateChange",
    "DamsQuality",
    "Siltation",
    "AgriculturalPractices",
    "Encroachments",
    "IneffectiveDisasterPreparedness",
    "DrainageSystems",
    "CoastalVulnerability",
    "Landslides",
    "Watersheds",
    "DeterioratingInfrastructure",
    "PopulationScore",
    "WetlandLoss",
    "InadequatePlanning",
    "PoliticalFactors",
    "f_sum",
    "f_std",
    "f_mean",
    "f_median",
    "f_ptp",
]

X = df[feature_cols]
y = df["FloodProbability"]

# 3. Train XGBoost Model (FR-2.1)
model = xgb.XGBRegressor(
    n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42
)
model.fit(X, y)

# 4. Save trained artifact for FastAPI backend
joblib.dump(model, "resilix_flood_model.joblib")
print(
    "Successfully trained XGBoost on dataset and saved 'resilix_flood_model.joblib'!"
)