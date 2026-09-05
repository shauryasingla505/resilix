import pandas as pd

# 1. Define file names (replace 'dataset.parquet' with your actual file name)
input_parquet = "test_cleaned.parquet"
output_csv = "test_dataset.csv"

try:
    print(f"Reading {input_parquet}...")
    # Read the parquet file
    df = pd.read_parquet(input_parquet)

    print("Converting to CSV...")
    # Export to CSV (index=False prevents writing row numbers)
    df.to_csv(output_csv, index=False)

    print(f"Done! Successfully saved to {output_csv}")

except FileNotFoundError:
    print(
        f"Error: Could not find '{input_parquet}'. Make sure it's in the same folder as this script!"
    )
except Exception as e:
    print(f"An error occurred: {e}")