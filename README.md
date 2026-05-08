# NHS RTT Breach Prediction & Risk Analysis Project

## Project Overview

This project was developed to analyse and predict NHS Referral to Treatment (RTT) pathway breaches using historical NHS England waiting time data.

The aim of the project was to identify treatment pathways that are likely to breach RTT performance targets in the following month using machine learning and data analytics techniques.

The project was built as an end-to-end analytics pipeline using:

* Python
* SQL Server
* Orange Data Mining
* Power BI
* GitHub

---

# Business Problem

NHS RTT performance is one of the key operational healthcare metrics in England.

Healthcare providers are expected to ensure that patients receive treatment within 18 weeks of referral.

However, due to increasing waiting lists, staffing pressures, and operational challenges, many pathways fail to meet the required threshold.

This project was designed to answer the following business questions:

* Which treatment pathways are likely to breach next month?
* Which providers show the highest operational risk?
* What factors contribute most to future breaches?
* How can NHS operational teams identify risks earlier?

---

# Data Source

The dataset used in this project was collected from NHS England official RTT statistics.

Data Source:
[https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/](https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/)

The dataset contains historical RTT waiting time information for multiple NHS providers and treatment functions across several years.

---

# Data Collection Process

The raw data was downloaded manually from NHS England.

The data was organised year-wise inside separate folders.

## Raw Data Structure

```text
RTT_RAW_DATA/
│
├── 2019-2020
├── 2020-2021
├── 2021-2022
├── 2022-2023
├── 2023-2024
└── 2024-2025
```

Each folder contained monthly RTT files.

Examples:

* RTT_2019_JAN
* RTT_2019_FEB
* RTT_2020_MAR
* RTT_2024_APR

The raw data included:

* Provider codes
* Treatment functions
* Waiting list counts
* RTT performance percentages
* 92nd percentile waiting time
* Monthly operational performance metrics

---

# Python Data Preparation

Python was used to combine multiple monthly files into a single master dataset.

Libraries used:

* pandas
* os

## Objective

The main objective of the Python stage was:

* Read all yearly datasets
* Combine monthly files
* Standardise column names
* Create a single consolidated dataset

---

# Python Workflow

## Step 1 - Read All Year Folders

The script looped through each yearly folder using Python.

## Step 2 - Load Monthly Files

Each monthly RTT CSV file was loaded into pandas.

## Step 3 - Combine Datasets

All yearly datasets were merged into a single dataframe.

## Step 4 - Clean Column Names

Column names were standardised using:

* whitespace removal
* underscore formatting

## Step 5 - Export Master Dataset

The final dataset was exported as:

```text
RTT_MASTER_DATA.csv
```

---

# Python Data Preparation Outcome

The Python pipeline successfully transformed multiple years of NHS RTT files into one consolidated dataset.

Benefits:

* Easier SQL processing
* Centralised dataset
* Improved data consistency
* Reduced manual processing

---

# SQL Data Cleaning & Transformation

After Python preprocessing, the master dataset was imported into SQL Server.

Database used:

```text
rtt_nhs
```

Main tables created:

* rtt_clean
* rtt_clean_final
* rtt_ml_dataset

---

# SQL Cleaning Process

The SQL stage focused on preparing machine learning-ready data.

## Step 1 - Remove Incomplete Records

Rows with missing values in critical columns were removed.

Removed records included:

* Missing waiting list values
* Missing RTT percentage values
* Incomplete operational records

Filtering logic:

```sql
WHERE total_waiting IS NOT NULL
AND within_18_weeks IS NOT NULL
```

---

# Feature Engineering in SQL

Feature engineering was one of the most important stages of the project.

The purpose was to create predictive variables that help machine learning models identify future breach risk.

---

## Features Created

### 1. current_pct

Represents the current RTT performance percentage.

Business meaning:

* Lower percentages indicate operational pressure
* Helps identify underperforming pathways

---

### 2. total_waiting

Represents the total waiting list size.

Business meaning:

* Higher waiting lists may increase breach probability

---

### 3. p92_wait_time

Represents the 92nd percentile waiting time.

Business meaning:

* Measures long patient waiting durations
* Indicates pathway backlog severity

---

### 4. pct_change_last_month

Calculated using SQL window functions.

Purpose:

* Measures month-on-month performance change
* Detects performance deterioration trends

SQL logic used:

```sql
LAG(pct_within_18_weeks)
```

---

### 5. waiting_list_change

Measures monthly waiting list growth.

Business meaning:

* Increasing waiting lists may signal future operational risk

---

# Target Variable Creation

The machine learning target variable was created using future month performance.

Target variable:

```text
will_breach_next_month
```

Logic:

* 1 = Future breach predicted
* 0 = Future safe pathway

Rule used:

```sql
CASE
WHEN next_month_pct < 92 THEN 1
ELSE 0
END
```

This allowed the model to learn patterns associated with future RTT breaches.

---

# Machine Learning Preparation

The final machine learning dataset was stored as:

```text
rtt_ml_dataset
```

This dataset contained:

* Operational metrics
* Trend variables
* Historical performance
* Future breach labels

---

# Orange Machine Learning Workflow

Orange Data Mining was used to build and evaluate machine learning models.

---

# Orange Workflow Process

## Step 1 - Import Dataset

The SQL output dataset was imported into Orange.

Input file:

```text
rtt_ml_dataset.csv
```

---

## Step 2 - Select Columns

Relevant predictive features were selected.

Features used:

* current_pct
* total_waiting
* p92_wait_time
* pct_change_last_month
* waiting_list_change

Ignored fields:

* provider_code
* treatment_function
* record_date

Target variable:

```text
will_breach_next_month
```

---

## Step 3 - Missing Value Handling

The Impute widget was used to handle missing values.

Purpose:

* Improve model consistency
* Prevent model training issues

---

## Step 4 - Machine Learning Models

The following models were trained:

### Random Forest

Primary prediction model used.

### Logistic Regression

Used for comparison and classification evaluation.

### Decision Tree

Used for interpretable rule-based analysis.

---

# Model Evaluation

The models were evaluated using:

* ROC Analysis
* Confusion Matrix
* Test & Score

Random Forest showed the strongest predictive performance and was selected for final prediction.

---

# Prediction Process

The trained Random Forest model was used to predict future RTT breaches.

Prediction logic:

* Historical data used for training
* March 2025 data used as input
* Model predicted April 2025 breach outcomes

Prediction output:

* 1 = Likely breach
* 0 = Likely safe

The final prediction output was exported for dashboard analysis.

---

# Power BI Dashboard Development

The machine learning prediction output was imported into Power BI.

The dashboard was created to visualise:

* Future RTT breach risks
* High-risk providers
* High-risk treatment functions
* Operational performance drivers

---

# Dashboard Metrics

The dashboard included:

## KPI Cards

* Total Pathways
* Predicted Breaches
* Breach Rate

---

# Dashboard Visuals

## RTT Breach Risk Distribution

Pie chart showing:

* Safe pathways
* Predicted breaches

---

## Top Risky Treatment Functions

Bar chart identifying treatment functions with the highest predicted breach counts.

---

## Provider-Level Breach Analysis

Provider comparison based on breach predictions.

---

## Drivers of RTT Breach Risk

Scatter plot showing:

* Waiting list size
* Operational performance
* Breach probability relationship

---

## Detailed Operational Table

Table containing:

* Provider code
* Treatment function
* Current RTT performance
* Waiting list metrics
* Predicted breach risk

---

# Dataset Statistics & Project Metrics

## Total Dataset Size

The final consolidated NHS RTT dataset contained:

```text
260,356 total records
```

The dataset included:

* Multiple NHS providers
* Multiple treatment functions
* Historical monthly RTT operational data
* Multi-year waiting time trends

---

# Data Cleaning Outcome

During SQL preprocessing:

* Records with missing operational metrics were removed
* Null waiting list records were filtered
* Incomplete RTT percentage values were excluded

This improved:

* machine learning reliability
* data consistency
* prediction quality

---

# Machine Learning Output Statistics

After model prediction:

```text
Total Pathways Analysed: 742
Predicted Breaches: 101
Predicted Safe Pathways: 641
```

---

# Breach Prediction Rate

The final dashboard showed:

```text
Predicted Breach Rate = 0.14
```

Equivalent to:

```text
14% of analysed pathways predicted to breach RTT targets
```

---

# Prediction Distribution

## Safe Pathways

```text
641 pathways
86.39%
```

## Predicted Breaches

```text
101 pathways
13.61%
```

---

# Operational Insight Examples

The model identified several high-risk treatment functions.

Examples included:

* General Internal Medicine
* Elderly Medicine
* Cardiology Services
* Plastic Surgery
* General Surgery

These pathways showed:

* Higher waiting list growth
* Lower RTT performance percentages
* Increased breach probability

---

# Dashboard KPI Summary

| KPI                | Value        |
| ------------------ | ------------ |
| Total Pathways     | 742          |
| Predicted Breaches | 101          |
| Breach Rate        | 14%          |
| Dataset Size       | 260,356 rows |

---

# Key Findings

The project identified several important operational insights.

---

## 1. High Waiting Lists Increase Breach Risk

Providers with larger waiting lists showed significantly higher breach probability.

---

## 2. Declining Monthly Performance Signals Future Breaches

Negative month-on-month performance trends strongly correlated with future RTT failures.

---

## 3. Certain Treatment Functions Showed Consistent Risk

Several treatment functions repeatedly appeared as high-risk categories.

Examples included:

* General Internal Medicine
* Elderly Medicine
* Cardiology-related pathways

---

## 4. Operational Trends Matter More Than Single Metrics

The machine learning model performed better when trend-based features were included.

This demonstrates the importance of:

* performance trends
* waiting list growth
* historical operational patterns

---

# Business Value

This project demonstrates how predictive analytics can support proactive healthcare management.

Potential benefits:

* Early breach identification
* Improved resource allocation
* Better operational planning
* Reduced RTT performance failures
* Data-driven healthcare decision making

---

# Technologies Used

| Technology | Purpose                                 |
| ---------- | --------------------------------------- |
| Python     | Data preparation                        |
| pandas     | File processing                         |
| SQL Server | Data cleaning & feature engineering     |
| Orange     | Machine learning modelling              |
| Power BI   | Dashboard development                   |
| GitHub     | Project documentation & version control |

---

# Project Workflow Summary

```text
NHS England Data
        ↓
Python Data Preparation
        ↓
SQL Cleaning & Feature Engineering
        ↓
Orange Machine Learning
        ↓
Prediction Output
        ↓
Power BI Dashboard
        ↓
Operational Insights
```

---

# Conclusion

This project successfully developed an end-to-end predictive analytics pipeline for NHS RTT breach prediction.

The solution combines:

* data engineering
* SQL analytics
* machine learning
* dashboard storytelling

The project demonstrates how historical NHS operational data can be transformed into predictive insights that support proactive healthcare decision making.

---

# Author

Saketh Veerabathini

MSc Business Analytics
Coventry University
