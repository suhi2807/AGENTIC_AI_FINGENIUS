# AGENTIC AI FINGENIUS

## FinSight AI – Autonomous Business Finance Intelligence

FinSight AI is a multi-agent financial intelligence system that automatically analyzes company transaction data, identifies unusual expenses, forecasts future spending, evaluates budget risk, and provides financial recommendations.

## Features

* Upload CSV or Excel transaction datasets
* Automatic data validation and cleaning
* Financial auditing using SQL and Pandas
* Expense category and department analysis
* High-value transaction anomaly detection
* Daily burn-rate calculation
* 30-day expense forecasting
* Budget utilization and risk classification
* Automated financial recommendations
* Interactive Streamlit dashboard
* SQLite-based data storage

## Agents

### Agent 1 – Financial Auditor

Analyzes transactions, total expenses, categories, departments, vendors, and unusual high-value transactions.

### Agent 2 – Financial Forecast

Uses the audit results to calculate burn rate, projected expenses, budget utilization, variance, and financial risk.

## Workflow

Company Dataset → Data Validation → SQLite Database → Financial Auditor Agent → Forecast Agent → Risk Analysis → Recommendation → Dashboard

## Technologies Used

* Python
* Pandas
* SQLite
* SQL
* Streamlit

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Note

The project uses synthetic financial transaction data for demonstration and testing purposes.
