import os
import glob
import pandas as pd

def find_file(filename: str) -> str:
    """Finds a file in the current directory or immediate subdirectories."""
    if os.path.exists(filename):
        return filename
    matches = glob.glob(f"**/{filename}", recursive=True)
    if matches:
        return matches[0]
    raise FileNotFoundError(
        f"Could not locate '{filename}'. Ensure it is unzipped in this folder."
    )

def clean_and_optimize(file_path: str, is_train: bool = True) -> pd.DataFrame:
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)
    
    feature_cols = [c for c in df.columns if c not in ['id', 'FloodProbability']]
    
    # 1. Downcast feature columns to uint8
    for col in feature_cols:
        df[col] = df[col].astype('uint8')
        
    # 2. Add statistical aggregation features
    df['f_sum'] = df[feature_cols].sum(axis=1).astype('uint16')
    df['f_std'] = df[feature_cols].std(axis=1).astype('float32')
    df['f_mean'] = df[feature_cols].mean(axis=1).astype('float32')
    df['f_median'] = df[feature_cols].median(axis=1).astype('float32')
    df['f_ptp'] = (df[feature_cols].max(axis=1) - df[feature_cols].min(axis=1)).astype('uint8')

    # 3. Downcast ID and Target
    df['id'] = df['id'].astype('uint32')
    if is_train and 'FloodProbability' in df.columns:
        df['FloodProbability'] = df['FloodProbability'].astype('float32')
        
    return df

# Locate files dynamically
train_path = find_file("train.csv")
test_path = find_file("test.csv")

# Clean and output Parquet files
train_clean = clean_and_optimize(train_path, is_train=True)
test_clean = clean_and_optimize(test_path, is_train=False)

train_clean.to_parquet("train_cleaned.parquet", index=False)
test_clean.to_parquet("test_cleaned.parquet", index=False)

print("Finished: 'train_cleaned.parquet' and 'test_cleaned.parquet' generated successfully.")