import streamlit as st
import pandas as pd

from database import (
    initialize_all,
    COMPANY_DB,
    get_company_info,
    get_transactions
)

from agents.auditor_agent import run_auditor_agent
from agents.forecast_agent import run_forecast_agent


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💼",
    layout="wide"
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

initialize_all()


# =========================================================
# HEADER
# =========================================================

st.title("💼 FinSight AI")

st.subheader(
    "Autonomous Business Finance Intelligence Platform"
)

st.write(
    "FinSight AI uses autonomous AI agents to analyze "
    "business financial data, detect financial risks, "
    "forecast spending and generate business insights "
    "without requiring manual financial analysis."
)


# =========================================================
# COMPANY INFORMATION
# =========================================================

company_name, monthly_budget = get_company_info()


st.success(
    f"🏢 Active Company Database: {company_name}"
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💼 FinSight AI")

st.sidebar.write(
    "Autonomous Multi-Agent Finance System"
)

st.sidebar.divider()

st.sidebar.info(
    "The system automatically reads the company "
    "database and runs both autonomous agents."
)


# =========================================================
# RUN AGENT 1
# =========================================================

audit = run_auditor_agent()


# =========================================================
# RUN AGENT 2
# =========================================================

forecast = run_forecast_agent(audit)


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.header("📊 Executive Financial Summary")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Transactions",
        f"{audit['transaction_count']:,}"
    )


with col2:

    st.metric(
        "Total Expense",
        f"₹{audit['total_expense']:,.0f}"
    )


with col3:

    st.metric(
        "Monthly Budget",
        f"₹{monthly_budget:,.0f}"
    )


with col4:

    st.metric(
        "Projected Expense",
        f"₹{forecast['projected_expense']:,.0f}"
    )


# =========================================================
# AGENT 1
# =========================================================

st.header(
    "🤖 Agent 1 — Autonomous Financial Auditor"
)

st.write(
    "The Financial Auditor Agent automatically reads "
    "all transactions and identifies important financial "
    "patterns, spending areas and unusual transactions."
)


# =========================================================
# AUDIT METRICS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Transaction",
        f"₹{audit['average_expense']:,.0f}"
    )


with col2:

    st.metric(
        "Highest Transaction",
        f"₹{audit['highest_expense']:,.0f}"
    )


with col3:

    if audit["unusual_transactions"]:

        st.metric(
            "Unusual Transactions",
            len(audit["unusual_transactions"])
        )

    else:

        st.metric(
            "Unusual Transactions",
            0
        )


# =========================================================
# AUDITOR FINDINGS
# =========================================================

st.subheader("🔎 Autonomous Audit Findings")


for finding in audit["findings"]:

    st.info(
        "🤖 " + finding
    )


# =========================================================
# CATEGORY ANALYSIS
# =========================================================

st.subheader(
    "💸 Expense Analysis by Category"
)


category_df = pd.DataFrame(
    audit["categories"]
)


if not category_df.empty:

    chart_df = category_df[
        ["category", "amount"]
    ].copy()

    chart_df.columns = [
        "Category",
        "Amount"
    ]

    st.bar_chart(
        chart_df.set_index("Category")
    )

    display_df = category_df.copy()

    display_df.columns = [
        "Category",
        "Amount",
        "Share (%)"
    ]

    display_df["Amount"] = display_df[
        "Amount"
    ].round(2)

    display_df["Share (%)"] = display_df[
        "Share (%)"
    ].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DEPARTMENT ANALYSIS
# =========================================================

st.subheader(
    "🏢 Department Spending Analysis"
)


department_df = pd.DataFrame(
    audit["departments"]
)


if not department_df.empty:

    department_chart = department_df[
        ["department", "amount"]
    ].copy()

    department_chart.columns = [
        "Department",
        "Amount"
    ]

    st.bar_chart(
        department_chart.set_index(
            "Department"
        )
    )


# =========================================================
# VENDOR ANALYSIS
# =========================================================

st.subheader(
    "🏪 Top Business Vendors"
)


vendor_df = pd.DataFrame(
    audit["vendors"],
    columns=[
        "Vendor",
        "Total Spending",
        "Transactions"
    ]
)


if not vendor_df.empty:

    vendor_df["Total Spending"] = (
        vendor_df["Total Spending"].round(2)
    )

    st.dataframe(
        vendor_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# ANOMALY DETECTION
# =========================================================

st.subheader(
    "🚨 Autonomous Anomaly Detection"
)


if audit["unusual_transactions"]:

    anomaly_df = pd.DataFrame(
        audit["unusual_transactions"],
        columns=[
            "Transaction ID",
            "Date",
            "Department",
            "Category",
            "Vendor",
            "Amount"
        ]
    )

    st.dataframe(
        anomaly_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No unusual high-value transactions detected."
    )


# =========================================================
# AGENT 2
# =========================================================

st.header(
    "🔮 Agent 2 — Autonomous Financial Forecast Agent"
)

st.write(
    "The Forecast Agent automatically receives the "
    "Auditor Agent's results and predicts future spending, "
    "budget utilization and financial risk."
)


# =========================================================
# FORECAST METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Daily Burn Rate",
        f"₹{forecast['daily_burn_rate']:,.0f}"
    )


with col2:

    st.metric(
        "30-Day Projection",
        f"₹{forecast['projected_expense']:,.0f}"
    )


with col3:

    st.metric(
        "Projected Budget Usage",
        f"{forecast['projected_utilization']:.1f}%"
    )


with col4:

    st.metric(
        "Financial Risk",
        forecast["risk"]
    )


# =========================================================
# BUDGET VS FORECAST
# =========================================================

st.subheader(
    "📈 Monthly Budget vs Projected Expense"
)


comparison_df = pd.DataFrame(
    {
        "Amount": [
            forecast["monthly_budget"],
            forecast["projected_expense"]
        ]
    },
    index=[
        "Monthly Budget",
        "Projected Expense"
    ]
)


st.bar_chart(
    comparison_df
)


# =========================================================
# FORECAST RESULT
# =========================================================

if forecast["projected_variance"] >= 0:

    st.success(
        f"💰 Projected budget surplus: "
        f"₹{forecast['projected_variance']:,.0f}"
    )

else:

    st.error(
        f"🚨 Projected budget deficit: "
        f"₹{abs(forecast['projected_variance']):,.0f}"
    )


# =========================================================
# AUTONOMOUS DECISION
# =========================================================

st.subheader(
    "🧠 Autonomous Business Decision"
)


if forecast["risk"] == "HIGH":

    st.error(
        "🔴 HIGH RISK\n\n" +
        forecast["recommendation"]
    )

elif forecast["risk"] == "MEDIUM":

    st.warning(
        "🟡 MEDIUM RISK\n\n" +
        forecast["recommendation"]
    )

else:

    st.success(
        "🟢 LOW RISK\n\n" +
        forecast["recommendation"]
    )


# =========================================================
# AGENT WORKFLOW
# =========================================================

st.header(
    "🔄 Autonomous Agent Workflow"
)


workflow_df = pd.DataFrame(
    {
        "Stage": [
            "Company Database",
            "Financial Auditor Agent",
            "Expense Analysis",
            "Anomaly Detection",
            "Forecast Agent",
            "Risk Evaluation",
            "Business Decision"
        ],

        "Status": [
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed"
        ]
    }
)


st.dataframe(
    workflow_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# COMPANY DATABASE
# =========================================================

st.header(
    "🗄️ Company Transaction Database"
)


transactions = get_transactions()


transaction_df = pd.DataFrame(
    transactions,
    columns=[
        "Transaction ID",
        "Date",
        "Department",
        "Category",
        "Vendor",
        "Amount",
        "Payment Method",
        "Description"
    ]
)


if not transaction_df.empty:

    st.dataframe(
        transaction_df.head(100),
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No transactions are currently available."
    )


# =========================================================
# BUSINESS DEPLOYMENT MODEL
# =========================================================

st.header(
    "🏢 Real Business Deployment Model"
)


st.write(
    "The current project uses a synthetic company database "
    "for demonstration. In a real business, the same "
    "system can be connected to an authorized internal "
    "financial database."
)


st.code(
    """Company Financial Database
            ↓
    Autonomous Auditor Agent
            ↓
    Financial Analysis
            ↓
    Anomaly Detection
            ↓
    Forecast Agent
            ↓
    Risk Evaluation
            ↓
    Business Recommendation
            ↓
    Streamlit Dashboard""",
    language="text"
)


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.header(
    "ℹ️ Project Information"
)


st.write(
    "FinSight AI demonstrates autonomous multi-agent "
    "business finance intelligence using Python, "
    "SQLite and Streamlit."
)


st.write(
    "The agents operate automatically from the company "
    "database. No manual expense entry is required for "
    "the autonomous analysis workflow."
)


st.divider()


st.caption(
    "FinSight AI • Autonomous Business Finance Intelligence"
)