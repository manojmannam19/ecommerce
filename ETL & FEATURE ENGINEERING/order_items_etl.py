import numpy as np
import pandas as pd

RAW_PATH = "/content/drive/MyDrive/order_items.csv"
CLEANED_PATH = "/content/drive/MyDrive/order_items_cleaned.csv"

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

# Remove exact duplicate order-item rows
df = df.drop_duplicates().copy()

# Clean IDs
for col in ["order_id", "product_id"]:
    df[col] = df[col].astype("string").str.strip().str.upper()

# Convert numeric columns
numeric_columns = [
    "quantity", "unit_price", "discount_percentage",
    "discount_amount", "gross_sales", "tax_amount",
    "shipping_cost", "net_sales", "product_cost", "profit"
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Validate quantity and financial values
df.loc[df["quantity"] <= 0, "quantity"] = np.nan

financial_columns = [
    "unit_price", "discount_percentage", "discount_amount",
    "gross_sales", "tax_amount", "shipping_cost",
    "net_sales", "product_cost"
]
for col in financial_columns:
    df.loc[df[col] < 0, col] = np.nan

# Fill missing numeric values
for col in numeric_columns:
    if df[col].notna().any():
        df[col] = df[col].fillna(df[col].median())

# Feature engineering
df["profit_margin_percentage"] = np.where(
    df["net_sales"] > 0,
    (df["profit"] / df["net_sales"]) * 100,
    0
)

df["effective_discount_rate"] = np.where(
    df["gross_sales"] > 0,
    (df["discount_amount"] / df["gross_sales"]) * 100,
    0
)

df["profit_status"] = np.where(
    df["profit"] > 0, "Profitable",
    np.where(df["profit"] < 0, "Loss", "Break-even")
)

# Validation
assert df["order_id"].notna().all()
assert df["product_id"].notna().all()
assert (df["quantity"] > 0).all()
assert (df["net_sales"] >= 0).all()

# Round values
for col in numeric_columns + [
    "profit_margin_percentage", "effective_discount_rate"
]:
    df[col] = df[col].round(2)

df.to_csv(CLEANED_PATH, index=False)

print("Order Items ETL completed")
print("Final shape:", df.shape)
print("Saved to:", CLEANED_PATH)
