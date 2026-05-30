# 🔮 Customer Churn Prediction — End-to-End Data Project

> Predicting customer churn using SQL, Python, XGBoost, SHAP, Streamlit & Power BI

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?logo=powerbi)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)

---

## 📌 Business Problem

A telecom company loses **26.6% of its customers** every year.
Each churned customer represents ~12 months of lost recurring revenue.

**Goal:** Build an end-to-end system that identifies at-risk customers **before** they leave, so the retention team can act proactively.

---

## 🏗️ Project Architecture

```
Raw Data (CSV)
      ↓
PostgreSQL Database     ← SQL modeling + business queries
      ↓
Python / Jupyter        ← EDA, feature engineering, ML
(pandas, sklearn, SHAP)
      ↓
XGBoost Model           ← Best AUC among 3 algorithms
      ↓
Streamlit App           ← Live scoring demo
      ↓
Power BI Dashboard      ← Executive business view
```

---

## 📊 Key Results

| Metric | Value |
|---|---|
| Dataset | 7,032 Telco customers |
| Churn rate | 26.6% |
| Best model | XGBoost |
| AUC-ROC | **0.845** |
| Key insight | Month-to-month + Fiber optic → **54.6% churn rate** |
| Key insight | Two year contract → **2.8% churn rate** |

---

## 🔍 Top Insights (EDA + SQL)

- 📌 **Contract type** is the strongest churn predictor — month-to-month customers churn 20x more than 2-year contracts
- 📌 **New customers** (tenure < 12 months) + high monthly charges → **66.5% churn rate**
- 📌 **Loyal customers** (tenure > 60 months) churn at only **6.6%** regardless of spend
- 📌 Customers without **online security or tech support** are 2x more likely to churn
- 📌 **Electronic check** payment method correlates with highest churn (~45%)

---

## 🤖 ML Pipeline

### Models compared
| Model | AUC (Test) | AUC (CV 5-fold) |
|---|---|---|
| Logistic Regression | 0.851 | 0.843 |
| Random Forest | 0.827 | 0.819 |
| **XGBoost** | **0.845** | **0.838** |

### Feature Engineering
- `avg_monthly_spend` — Total charges / tenure (historical monthly average)
- `spend_drift` — Gap between current and historical monthly spend
- `nb_services` — Number of active services
- `no_protection` — Flag: no security + no tech support + no device protection
- `tenure_segment` — Bucketed customer lifetime (New / Intermediate / Loyal / Very loyal)
- `value_segment` — Revenue tier (Small / Medium / Large account)

### Why XGBoost?
- Best interpretability via SHAP values
- Robust to class imbalance (26/74 split)
- No feature scaling required

---

## 🧠 SHAP Explainability

SHAP (SHapley Additive exPlanations) reveals **why** each prediction is made:

- `tenure` — Low tenure strongly pushes toward churn
- `Contract` — Month-to-month increases churn risk significantly
- `MonthlyCharges` — High charges without loyalty = high risk
- `InternetService` — Fiber optic customers churn more than DSL

> This goes beyond "the model says 73%" — it gives actionable business levers.

---

## 🖥️ Streamlit App

The interactive app allows anyone to:
1. Fill in a customer profile (contract, tenure, services...)
2. Get an instant churn risk score (0–100%)
3. See a **SHAP waterfall chart** explaining the exact drivers of that score

```bash
cd app
streamlit run streamlit_app.py
```

---

## 📈 Power BI Dashboard

The executive dashboard shows:
- **KPIs** — Total customers, churners, monthly revenue, revenue at risk
- **Donut chart** — Churn vs loyal split
- **Bar chart** — Churn rate by contract type
- **Matrix heatmap** — Churn rate by tenure segment × value segment
- **Scatter plot** — Customer profiling (tenure vs monthly charges)

---

## 🗄️ SQL Business Queries

Key queries in `sql/03_business_queries.sql`:
```sql
-- Churn rate by contract & internet service
SELECT contract, internet_service,
       ROUND(AVG(CASE WHEN churn THEN 1 ELSE 0 END) * 100, 1) AS churn_rate
FROM customers
GROUP BY contract, internet_service
ORDER BY churn_rate DESC;
```

---

## 🚀 How to Run

### Prerequisites
```
Python 3.11+
PostgreSQL 15+
Anaconda (recommended)
Power BI Desktop
```

### Setup
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/churn-prediction-project.git
cd churn-prediction-project

# Install dependencies
pip install -r requirements.txt

# Configure database credentials
cp .env.example .env
# Edit .env with your PostgreSQL password

# Load data into PostgreSQL
python sql/02_load_data.py

# Run notebooks in order
# notebooks/01_eda.ipynb
# notebooks/02_features.ipynb
# notebooks/03_modeling.ipynb

# Launch the Streamlit app
cd app && streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
churn-prediction-project/
├── data/
│   ├── raw/                  # Original Kaggle dataset
│   └── processed/            # Cleaned & feature-engineered data
├── sql/
│   ├── 01_create_tables.sql  # PostgreSQL schema
│   ├── 02_load_data.py       # Data ingestion script
│   └── 03_business_queries.sql
├── notebooks/
│   ├── 01_eda.ipynb          # Exploratory Data Analysis
│   ├── 02_features.ipynb     # Feature Engineering
│   └── 03_modeling.ipynb     # ML modeling + SHAP
├── src/
│   └── export_for_powerbi.py
├── app/
│   └── streamlit_app.py      # Interactive scoring app
├── models/
│   └── best_model.pkl        # Saved XGBoost model
├── reports/
│   └── figures/              # All exported charts
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Database | PostgreSQL, SQLAlchemy |
| Analysis | Python, pandas, numpy, matplotlib, seaborn |
| ML | scikit-learn, XGBoost, SHAP |
| App | Streamlit, Plotly |
| Dashboard | Power BI Desktop |
| Versioning | Git, GitHub |

---

## 👤 Author

**Salwane ALAO**
Data Analyst

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/salwane-alao)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/salwanealao63-cell
)

---

*Dataset source: [Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)*
