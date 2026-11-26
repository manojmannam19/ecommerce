import numpy as np
import pandas as pd

RAW_PATH = "/content/drive/MyDrive/customer_master.csv"
CLEANED_PATH = "/content/drive/MyDrive/customer_master_cleaned.csv"

# Extract
df = pd.read_csv(RAW_PATH)

# Standardize column names
df.columns = (
    df.columns.str.strip().str.lower().str.replace(" ", "_")
)

# Handle common null values
null_values = ["None", "none", "NULL", "null", "N/A", "n/a",
               "nan", "NaN", "Nan", "-", ""]
df.replace(null_values, np.nan, inplace=True)

# Remove duplicate customers
df = df.drop_duplicates(subset=["customer_id"], keep="first").copy()

# Clean IDs and text
df["customer_id"] = df["customer_id"].astype("string").str.strip().str.upper()
df["customer_name"] = df["customer_name"].astype("string").str.strip().str.title()

text_columns = [
    "customer_city", "customer_state", "customer_country",
    "region", "customer_segment"
]
for col in text_columns:
    df[col] = df[col].astype("string").str.strip().str.title()

# Standardize gender
gender_map = {
    "m": "Male", "male": "Male",
    "f": "Female", "female": "Female",
    "o": "Other", "other": "Other"
}
df["gender"] = df["gender"].astype("string").str.strip().str.lower().map(gender_map)

# Numeric conversion
df["customer_age"] = pd.to_numeric(df["customer_age"], errors="coerce")
df["customer_postal_code"] = pd.to_numeric(
    df["customer_postal_code"], errors="coerce"
)
df["customer_acquisition_cost"] = pd.to_numeric(
    df["customer_acquisition_cost"], errors="coerce"
)

# Validate numeric values
df.loc[~df["customer_age"].between(1, 100), "customer_age"] = np.nan
df.loc[df["customer_acquisition_cost"] < 0, "customer_acquisition_cost"] = np.nan

# Fill missing values
df["customer_age"] = df["customer_age"].fillna(df["customer_age"].median()).round().astype("Int32")
df["customer_postal_code"] = df["customer_postal_code"].fillna(
    df["customer_postal_code"].median()
).round().astype("Int64")
df["customer_acquisition_cost"] = df["customer_acquisition_cost"].fillna(
    df["customer_acquisition_cost"].median()
)

for col in ["gender", "customer_segment", "region"]:
    if not df[col].dropna().empty:
        df[col] = df[col].fillna(df[col].mode()[0])

# Feature engineering
df["age_group"] = pd.cut(
    df["customer_age"],
    bins=[0, 18, 25, 35, 45, 55, 65, 100],
    labels=["Under 18", "18-25", "26-35", "36-45",
            "46-55", "56-65", "65+"],
    include_lowest=True
).astype("string")

df["acquisition_cost_group"] = pd.qcut(
    df["customer_acquisition_cost"],
    q=4,
    labels=["Low", "Medium", "High", "Very High"],
    duplicates="drop"
).astype("string")

df["is_high_acquisition_cost"] = np.where(
    df["customer_acquisition_cost"] > df["customer_acquisition_cost"].median(),
    1, 0
)

df["customer_location"] = (
    df["customer_city"].fillna("Unknown") + ", " +
    df["customer_state"].fillna("Unknown")
)

df["customer_profile"] = (
    df["customer_segment"].fillna("Unknown") + " - " +
    df["age_group"].fillna("Unknown")
)

# Validation
assert df["customer_id"].notna().all()
assert not df["customer_id"].duplicated().any()
assert df["customer_age"].between(1, 100).all()
assert (df["customer_acquisition_cost"] >= 0).all()

# Round and save
df["customer_acquisition_cost"] = df["customer_acquisition_cost"].round(2)
df.to_csv(CLEANED_PATH, index=False)

print("Customer ETL completed")
print("Final shape:", df.shape)
print("Saved to:", CLEANED_PATH)
