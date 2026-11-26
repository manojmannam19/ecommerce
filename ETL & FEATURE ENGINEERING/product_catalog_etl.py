import numpy as np
import pandas as pd

RAW_PATH = "/content/drive/MyDrive/product_catalog.csv"
CLEANED_PATH = "/content/drive/MyDrive/product_catalog_cleaned.csv"

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

# Remove duplicate products
df = df.drop_duplicates(subset=["product_id"], keep="first").copy()

# Clean IDs and text
df["product_id"] = df["product_id"].astype("string").str.strip().str.upper()

text_columns = [
    "product_name", "product_category", "product_subcategory",
    "brand", "supplier"
]
for col in text_columns:
    df[col] = df[col].astype("string").str.strip().str.title()

# Numeric conversion
for col in ["unit_price", "product_cost", "product_rating"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Validate numeric values
df.loc[df["unit_price"] < 0, "unit_price"] = np.nan
df.loc[df["product_cost"] < 0, "product_cost"] = np.nan
df.loc[~df["product_rating"].between(0, 5), "product_rating"] = np.nan

# Fill missing numeric values
df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())
df["product_cost"] = df["product_cost"].fillna(df["product_cost"].median())
df["product_rating"] = df["product_rating"].fillna(df["product_rating"].median())

# Fill missing categorical values
for col in ["product_category", "product_subcategory", "brand", "supplier"]:
    if not df[col].dropna().empty:
        df[col] = df[col].fillna(df[col].mode()[0])

# Feature engineering
df["profit_per_unit"] = df["unit_price"] - df["product_cost"]

df["profit_margin_percentage"] = np.where(
    df["unit_price"] > 0,
    (df["profit_per_unit"] / df["unit_price"]) * 100,
    0
)

df["rating_category"] = pd.cut(
    df["product_rating"],
    bins=[0, 2, 3, 4, 5],
    labels=["Low", "Average", "Good", "Excellent"],
    include_lowest=True
).astype("string")

df["price_category"] = pd.qcut(
    df["unit_price"],
    q=4,
    labels=["Low", "Medium", "High", "Very High"],
    duplicates="drop"
).astype("string")

# Validation
assert df["product_id"].notna().all()
assert not df["product_id"].duplicated().any()
assert (df["unit_price"] >= 0).all()
assert (df["product_cost"] >= 0).all()
assert df["product_rating"].between(0, 5).all()

# Round and save
for col in [
    "unit_price", "product_cost", "product_rating",
    "profit_per_unit", "profit_margin_percentage"
]:
    df[col] = df[col].round(2)

df.to_csv(CLEANED_PATH, index=False)

print("Product ETL completed")
print("Final shape:", df.shape)
print("Saved to:", CLEANED_PATH)
