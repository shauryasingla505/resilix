import json
import numpy as np
import pandas as pd

def generate_risk_geojson(
    input_file="train_cleaned.parquet",
    output_file="risk_heatmap.geojson",
    sample_size=600,
    center_lat=12.9165,
    center_lng=79.1325
):
    print(f"Loading data from {input_file}...")
    if input_file.endswith(".parquet"):
        df = pd.read_parquet(input_file)
    else:
        df = pd.read_csv(input_file)

    sample_df = df.sample(n=min(sample_size, len(df)), random_state=42).reset_index(drop=True)

    features = []
    np.random.seed(42)

    # Distribute nodes across a realistic urban dispatch radius (~5-7 km)
    lat_offsets = np.random.normal(0, 0.025, size=len(sample_df))
    lng_offsets = np.random.normal(0, 0.025, size=len(sample_df))

    for idx, row in sample_df.iterrows():
        # Scale 0.0 - 1.0 to 0 - 100 if needed
        risk = float(row.get("FloodProbability", 0.5))
        if risk <= 1.0:
            risk = round(risk * 100.0, 1)

        # Approximate simulated pipe water level
        water_level = round(float(risk / 30.0 + np.random.uniform(0.1, 0.4)), 2)
        status = "CRITICAL" if risk >= 65 else ("WARNING" if risk >= 45 else "NOMINAL")

        lat = round(center_lat + lat_offsets[idx], 5)
        lng = round(center_lng + lng_offsets[idx], 5)

        # Standard GeoJSON coordinates convention: [longitude, latitude]
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]
            },
            "properties": {
                "id": f"node_{100 + idx}",
                "risk_score": risk,
                "water_level_m": water_level,
                "status": status
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, "w") as f:
        json.dump(geojson_data, f, indent=2)

    print(f"Exported {len(features)} points to '{output_file}'.")

if __name__ == "__main__":
    generate_risk_geojson()