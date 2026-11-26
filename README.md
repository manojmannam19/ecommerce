🛒 E-Commerce Analytics Platform

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![XGBoost](https://img.shields.io/badge/XGBoost-Machine_Learning-green?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)


An end-to-end E-Commerce Data Analytics and Machine Learning Project built using Python, XGBoost, and Microsoft Power BI.

This project focuses on analyzing e-commerce sales, customer behavior, product performance, marketing effectiveness, and business operations. It also uses Machine Learning models to predict customer churn, sales performance, and product returns.

📌 Project Overview

The E-Commerce Analytics Platform transforms raw e-commerce data into meaningful business insights through data cleaning, feature engineering, machine learning, and interactive Power BI dashboards.

The project is designed to help businesses understand their sales performance, identify customer trends, monitor product returns, and make data-driven decisions.

🎯 Project Objectives
Analyze overall sales and profitability.
Understand customer purchasing behavior.
Identify customers at risk of churning.
Evaluate product performance.
Analyze marketing and discount effectiveness.
Monitor order delivery and return patterns.
Predict sales performance using Machine Learning.
Predict customer churn and product returns.
Present business insights through interactive dashboards.

🛠️ Technologies Used
Technology	Purpose
Python	Data processing and ETL
Pandas & NumPy	Data cleaning and manipulation
XGBoost	Machine Learning models
Scikit-learn	Model evaluation and preprocessing
Microsoft Power BI	Interactive dashboards
CSV / Excel	Data storage and documentation
Jupyter / Google Colab	Model development and analysis

🏗️ Project Architecture


## 🏗️ Project Architecture

The project follows an end-to-end data analytics and machine learning workflow.

```mermaid
flowchart TD
    A["Raw E-Commerce Datasets"] --> B["ETL & Data Cleaning"]
    B --> C["Cleaned Datasets"]
    C --> D["Feature Engineering"]
    D --> E["XGBoost Machine Learning"]
    C --> F["Power BI Data Model"]
    E --> G["ML Predictions & Metrics"]
    G --> F
    F --> H["Interactive Power BI Dashboard"]
    H --> I["Business Insights & Decision Making"]
```

### Project Components

| Component | Description |
|---|---|
| DATA | Raw and cleaned datasets |
| ETL | Five Python scripts for dataset cleaning |
| Feature Engineering | Preparation of analytical and ML features |
| ML | XGBoost classification and regression models |
| POWERBI | Interactive business intelligence dashboard |
| DOCS | Data dictionary, architecture and ML documentation |

### Repository Structure

```text
ecommerce/
├── DATA/
│   ├── SOURCE/
│   └── cleaned/
├── ETL & FEATURE ENGINEERING/
├── ML/
├── POWERBI/
├── PROJECT DOCS/
└── README.md
```


📂 Project Folder Structure
text
ecommerce/
│
├── DATA/
│
├── ETL & FEATURE ENGINEERING/
│
├── ML/
│
├── POWERBI/
│
└── PROJECT DOCS/

Folder Description
DATA: Raw and cleaned e-commerce datasets.
ETL & FEATURE ENGINEERING: Python scripts for data cleaning, transformation, and feature creation.
ML: XGBoost machine learning implementation and prediction outputs.
POWERBI: Power BI dashboard and related files.
PROJECT DOCS: Project documentation, architecture, data dictionary, and supporting reports.


## 🔄 ETL & Feature Engineering

The ETL pipeline was developed using Python and Pandas to clean and transform five raw e-commerce datasets.

### ETL Workflow

```text
Extract
   ↓
Clean
   ↓
Transform
   ↓
Feature Engineering
   ↓
Validate
   ↓
Save Cleaned Dataset
```

### Dataset-wise ETL Implementation

| Dataset | Cleaning & Transformation | Feature Engineering |
|---|---|---|
| Customer Master | Standardized columns, handled missing values, removed duplicate customers, cleaned text and customer IDs, standardized gender and age | Age Group, Acquisition Cost Group, High Acquisition Cost Flag, Customer Location and Customer Profile |
| Product Catalog | Cleaned product IDs and text, handled missing values, removed duplicates, converted price and rating fields to numeric | Profit per Unit, Profit Margin %, Rating Category and Price Category |
| Order Items | Cleaned order and product IDs, handled missing values, removed duplicates, converted numerical fields and validated quantities and prices | Effective Discount Rate, Profit Margin %, Order Value Group, Profit Status and Discount Category |
| E-Commerce Sales | Cleaned transaction records, standardized dates and columns, handled missing values and duplicates, validated numerical and financial fields | Order Year, Order Month, Year-Month, Age Group, Delivery Variance, Effective Discount Rate, Profit Status and Return Flag |
| Dataset Statistics | Standardized columns, removed empty columns and duplicate rows | No additional feature engineering was required because it is a one-row reference dataset |

### Data Quality Validation

The ETL process included validation checks such as:

- Removing duplicate customer, product and order records.
- Checking missing and invalid values.
- Standardizing IDs, text fields and column names.
- Converting numerical and date columns into appropriate data types.
- Validating positive quantities and non-negative financial values.
- Checking unique IDs and important business rules.

### Output

The cleaned datasets were saved as separate CSV files.

The original raw datasets were preserved, allowing the cleaned data to be used for Machine Learning and Power BI reporting.


📊 Dataset Information

The main cleaned analytical dataset contains:

Total transactions: 138,116
Total customers: 24,911
Data period: January 2021 – December 2025

The project uses multiple datasets covering customer information, products, orders, and sales transactions.

🤖 Machine Learning — XGBoost Models

The project includes three machine learning models developed using XGBoost to support sales forecasting, customer retention analysis and return-risk prediction.

Models Developed
Model	Algorithm	Business Objective	Prediction
Sales Prediction	XGBRegressor	Predict sales amount	Numerical sales value
Customer Churn	XGBClassifier	Identify customers likely to stop purchasing	Active / Churned
Return Risk	XGBClassifier	Identify orders likely to be returned	Retained / Returned
1. Sales Prediction Model
Algorithm: XGBoost Regressor
Target variable: net_sales
Objective: Predict the sales amount for an order.
Evaluation metrics:
Metric	Result
MAE	49.39
RMSE	106.70
R² Score	0.9917
MAPE	4.95%

Observation: The model achieved an R² score of 99.17%, with an average percentage prediction error of approximately 4.95%.

2. Customer Churn Prediction Model
Algorithm: XGBoost Classifier
Target variable: churn_target
Class labels: 0 = Active, 1 = Churned
Objective: Identify customers who may stop purchasing.

Model evaluation:

Metric	Result
Accuracy	91.86%
Precision	94.51%
Recall	93.89%
F1 Score	94.20%
ROC-AUC	0.9245

Observation: The model correctly classified approximately 91.86% of the evaluated customer records, helping identify customers who may require retention attention.

3. Return Risk Prediction Model
Algorithm: XGBoost Classifier
Target variable: is_returned
Class labels: 0 = Retained, 1 = Returned
Objective: Predict the probability that an order will be returned.

Model evaluation:

Metric	Result
Accuracy	94.43%
Precision	53.14%
Recall	94.50%
F1 Score	68.86%
ROC-AUC	0.9585

Observation: The model detected approximately 94.50% of actual returned orders. Precision is lower, so some orders predicted as returns were not actually returned.

Machine Learning Workflow
Load cleaned datasets.
Select input features (X) and target variable (y).
Preprocess and encode categorical features.
Split data into training, validation and testing sets.
Handle class imbalance where required.
Train the XGBoost model.
Generate predictions and probabilities.
Evaluate model performance using suitable metrics.
Export prediction results and evaluation outputs for Power BI.
Technologies Used
Python
Pandas and NumPy
XGBoost
Scikit-learn
Google Colab
Model Outputs

The prediction results and evaluation metrics are exported as CSV files and used in the Power BI dashboard for model-performance analysis.
📈 Power BI Dashboard

The project includes interactive Power BI reports covering the following business areas:


## 📸 Power BI Dashboard Screenshots

### 1. Executive Overview
![Executive Overview](<POWERBI/Screenshot 2026-11-19 101646.png>)

### 2. Sales & Profitability
![Sales & Profitability](<POWERBI/Screenshot 2026-11-19 101719.png>)

### 3. Customer Analytics
![Customer Analytics](<POWERBI/Screenshot 2026-11-19 101741.png>)

### 4. Product Analytics
![Product Analytics](<POWERBI/Screenshot 2026-11-19 101818.png>)

### 5. Marketing Analytics
![Marketing Analytics](<POWERBI/Screenshot 2026-11-19 101846.png>)

### 6. Operations & Delivery
![Operations & Delivery](<POWERBI/Screenshot 2026-11-19 101914.png>)

### 7. Returns & Customer Experience
![Returns & Customer Experience](<POWERBI/Screenshot 2026-11-19 101931.png>)

### 8. Sales ML Predictions
![Sales ML Predictions](<POWERBI/Screenshot 2026-11-19 101955.png>)

### 9. Churn ML Predictions
![Churn ML Predictions](<POWERBI/Screenshot 2026-11-19 102011.png>)

### 10. Return ML Prediction
![Return ML Prediction](<POWERBI/Screenshot 2026-11-24 142422.png>)


The dashboards combine business KPIs, analytical visuals, filters, and machine learning prediction results.

💡 Key Business Insights
Customer purchase frequency plays an important role in churn prediction.
Customers with longer gaps between purchases show increased churn risk.
Discount-related features are important in return prediction.
Sales patterns and customer behavior provide useful information for business planning.
Machine Learning predictions can support customer retention and operational decisions.

🚀 Project Outcomes
Developed an end-to-end data analytics workflow.
Prepared multiple datasets for analytical reporting.
Implemented XGBoost classification and regression models.
Evaluated models using appropriate performance metrics.
Developed interactive Power BI dashboards.
Connected business analysis with machine learning predictions.

👨‍💻 Author

Mannam Manoj

Associate Software Engineer | Data Analytics | Python | Machine Learning | Power BI

GitHub:https://github.com/manojmannam19/ecommerce.git

This project was developed as an end-to-end analytical implementation for learning and demonstrating data analytics, machine learning, and business intelligence skills.
