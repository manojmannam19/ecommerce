import numpy as np
import pandas as pd

RAW_PATH = "/content/drive/MyDrive/ecommerce_sales_customer_analytics_150k.csv"
CLEANED_PATH = "/content/drive/MyDrive/ecommerce_sales_customer_analytics_cleaned.csv"

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

# Remove duplicate orders
df = df.drop_duplicates(subset=["order_id"], keep="first").copy()

# Clean IDs
df["order_id"] = df["order_id"].astype("string").str.strip().str.upper()
df["customer_id"] = df["customer_id"].astype("string").str.strip().str.upper()

# Date and time
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
if df["order_date"].isna().any() and not df["order_date"].dropna().empty:
    df["order_date"] = df["order_date"].fillna(df["order_date"].mode()[0])

df["order_time"] = df["order_time"].astype("string").str.strip()

# Clean text columns
text_columns = [
    "order_status", "sales_channel", "customer_name", "gender",
    "customer_segment", "customer_type", "customer_city",
    "customer_state", "customer_country", "region", "payment_method",
    "payment_status", "currency", "shipping_method", "warehouse",
    "delivery_status", "return_status", "return_reason",
    "review_sentiment", "customer_review", "marketing_channel",
    "campaign_name", "coupon_code"
]
for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# Standardize gender
gender_map = {
    "m": "Male", "male": "Male",
    "f": "Female", "female": "Female",
    "o": "Other", "other": "Other"
}
df["gender"] = (
    df["gender"].str.lower().map(gender_map)
)
if not df["gender"].dropna().empty:
    df["gender"] = df["gender"].fillna(df["gender"].mode()[0])

# Numeric conversion
numeric_columns = [
    "customer_age", "customer_postal_code", "delivery_days",
    "estimated_delivery_days", "customer_rating",
    "loyalty_points_earned", "loyalty_points_redeemed",
    "quantity", "gross_sales", "discount_amount", "tax_amount",
    "shipping_cost", "net_sales", "product_cost", "profit",
    "profit_margin_percentage", "customer_lifetime_value",
    "customer_order_count"
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Validate customer age and quantity
df.loc[~df["customer_age"].between(1, 100), "customer_age"] = np.nan
df["customer_age"] = (
    df["customer_age"].fillna(df["customer_age"].median())
    .round().astype("Int32")
)

df.loc[df["quantity"] <= 0, "quantity"] = np.nan
df["quantity"] = (
    df["quantity"].fillna(df["quantity"].median())
    .round().astype("Int32")
)

# Clean financial values
financial_columns = [
    "gross_sales", "discount_amount", "tax_amount", "shipping_cost",
    "net_sales", "product_cost", "profit",
    "profit_margin_percentage", "customer_lifetime_value"
]
for col in financial_columns:
    df.loc[df[col] < 0, col] = np.nan
    df[col] = df[col].fillna(df[col].median())

# Clean delivery days
for col in ["delivery_days", "estimated_delivery_days"]:
    df.loc[df[col] < 0, col] = np.nan
    df[col] = df[col].fillna(df[col].median())

# Feature engineering: date
df["order_year"] = df["order_date"].dt.year.astype("Int32")
df["order_month"] = df["order_date"].dt.month.astype("Int32")
df["order_year_month"] = df["order_date"].dt.strftime("%Y-%m")

# Feature engineering: customer
df["age_group"] = pd.cut(
    df["customer_age"],
    bins=[0, 18, 25, 35, 45, 55, 65, 100],
    labels=["Under 18", "18-25", "26-35", "36-45",
            "46-55", "56-65", "65+"],
    include_lowest=True
).astype("string")

# Feature engineering: business metrics
df["delivery_variance_days"] = (
    df["delivery_days"] - df["estimated_delivery_days"]
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

df["is_returned"] = (
    df["return_status"].str.lower()
    .isin(["returned", "yes", "true", "1"])
    .astype("Int8")
)

df["repeat_customer_flag"] = (
    df["is_repeat_customer"].astype("boolean")
)

# Validation
assert df["order_id"].notna().all()
assert not df["order_id"].duplicated().any()
assert df["customer_id"].notna().all()
assert (df["quantity"] > 0).all()
assert (df["net_sales"] >= 0).all()

# Round financial values
round_columns = [
    "gross_sales", "discount_amount", "tax_amount", "shipping_cost",
    "net_sales", "product_cost", "profit",
    "profit_margin_percentage", "customer_lifetime_value",
    "effective_discount_rate"
]
for col in round_columns:
    df[col] = df[col].round(2)

df.to_csv(CLEANED_PATH, index=False)

print("Sales & Customer Analytics ETL completed")
print("Final shape:", df.shape)
print("Saved to:", CLEANED_PATH)
