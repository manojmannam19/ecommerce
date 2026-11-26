import pandas as pd

RAW_PATH = "/content/drive/MyDrive/dataset_statistics.csv"
CLEANED_PATH = "/content/drive/MyDrive/dataset_statistics_cleaned.csv"

# Extract
df = pd.read_csv(RAW_PATH)

# Standardize column names
df.columns = (
    df.columns.str.strip().str.lower().str.replace(" ", "_")
)

# Save
df.to_csv(CLEANED_PATH, index=False)

print("Dataset Statistics ETL completed")
print("Final shape:", df.shape)
print("Saved to:", CLEANED_PATH)
