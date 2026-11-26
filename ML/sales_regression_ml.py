import pandas as pd
import numpy as np
import gc

from xgboost import XGBRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error
)


# 1. Load cleaned dataset


file_path = "/content/drive/MyDrive/ecommerce_sales_customer_analytics_cleaned.csv"

df = pd.read_csv(file_path)

# Date only for chronological split / final output
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Remove invalid target/date rows
df = df.dropna(subset=["order_date", "net_sales"])
df = df[df["net_sales"] >= 0].copy()

# Sort chronologically
df = df.sort_values("order_date").reset_index(drop=True)


# 2. Target


target = "net_sales"

# Columns that should NOT be used for prediction
exclude_cols = [
    "order_id",
    "customer_id",
    "product_id",
    "order_date",
    "net_sales",

    # Leakage / post-sale information
    "tax_amount",
    "shipping_fee",
    "shipping_cost",
    "profit",
    "profit_margin_percentage",
    "return_flag",
    "return_status",
    "delivery_status",
    "actual_delivery_days",
    "delivery_variance_days",
    "customer_rating",
    "review_text",
    "review_sentiment_score",
    "customer_lifetime_value"
]

# Keep only columns that actually exist
exclude_cols = [c for c in exclude_cols if c in df.columns]


# 3. Use existing numeric engineered features
#    No new feature engineering


feature_cols = [
    c for c in df.select_dtypes(include=np.number).columns
    if c not in exclude_cols
]

X = df[feature_cols].astype("float32")
y = df[target].astype("float32")


# 4. Chronological 80/20 split


split_index = int(len(X) * 0.80)

X_train = X.iloc[:split_index]
X_test  = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test  = y.iloc[split_index:]

test_dates = df["order_date"].iloc[split_index:].reset_index(drop=True)


# 5. Validation split inside training data


validation_index = int(len(X_train) * 0.85)

X_subtrain = X_train.iloc[:validation_index]
X_valid    = X_train.iloc[validation_index:]

y_subtrain = y_train.iloc[:validation_index]
y_valid    = y_train.iloc[validation_index:]


# 6. Try a few memory-safe XGBoost configurations


configs = [

    {
        "objective": "reg:squarederror",
        "n_estimators": 400,
        "max_depth": 4,
        "learning_rate": 0.04,
        "min_child_weight": 3
    },

    {
        "objective": "reg:squaredlogerror",
        "n_estimators": 500,
        "max_depth": 4,
        "learning_rate": 0.03,
        "min_child_weight": 3
    },

    {
        "objective": "reg:squaredlogerror",
        "n_estimators": 650,
        "max_depth": 3,
        "learning_rate": 0.025,
        "min_child_weight": 3
    }
]

best_config = None
best_mape = float("inf")

for config in configs:

    model = XGBRegressor(
        **config,
        subsample=0.90,
        colsample_bytree=0.90,
        reg_alpha=0.05,
        reg_lambda=1.5,
        tree_method="hist",
        max_bin=64,
        random_state=42,
        n_jobs=2
    )

    model.fit(X_subtrain, y_subtrain)

    valid_pred = model.predict(X_valid)
    valid_pred = np.maximum(valid_pred, 0)

    valid_mape = mean_absolute_percentage_error(
        y_valid,
        valid_pred
    ) * 100

    if valid_mape < best_mape:
        best_mape = valid_mape
        best_config = config.copy()

    del model
    gc.collect()


# 7. Train final model using best configuration


final_model = XGBRegressor(
    **best_config,
    subsample=0.90,
    colsample_bytree=0.90,
    reg_alpha=0.05,
    reg_lambda=1.5,
    tree_method="hist",
    max_bin=64,
    random_state=42,
    n_jobs=2
)

final_model.fit(X_train, y_train)


# 8. Final Sales Prediction


y_pred = final_model.predict(X_test)
y_pred = np.maximum(y_pred, 0)


# 9. Evaluation


mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

r2 = r2_score(y_test, y_pred)

mape = mean_absolute_percentage_error(
    y_test,
    y_pred
) * 100

print("Sales ML Results")
print("----------------------------")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")
print(f"MAPE : {mape:.2f}%")


# 10. Actual vs Predicted Sales


prediction_result = pd.DataFrame({
    "date": test_dates,
    "actual_sales": y_test.reset_index(drop=True),
    "predicted_sales": y_pred
})

prediction_result["error"] = (
    prediction_result["actual_sales"]
    - prediction_result["predicted_sales"]
)

display(prediction_result.head(10))