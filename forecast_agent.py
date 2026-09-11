from database import get_connection, get_company_info


def run_forecast_agent(auditor_result):

    total_expense = auditor_result["total_expense"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            MIN(transaction_date),
            MAX(transaction_date)
        FROM transactions
    """)

    dates = cursor.fetchone()

    conn.close()

    company_name, monthly_budget = get_company_info()

    if dates[0] and dates[1]:

        from datetime import datetime

        start_date = datetime.strptime(
            dates[0],
            "%Y-%m-%d"
        )

        end_date = datetime.strptime(
            dates[1],
            "%Y-%m-%d"
        )

        days_analyzed = (
            end_date - start_date
        ).days + 1

        if days_analyzed < 1:
            days_analyzed = 1

    else:

        days_analyzed = 1

    daily_burn_rate = (
        total_expense / days_analyzed
    )

    projected_expense = (
        daily_burn_rate * 30
    )

    if monthly_budget > 0:

        projected_utilization = (
            projected_expense / monthly_budget
        ) * 100

    else:

        projected_utilization = 0

    projected_variance = (
        monthly_budget - projected_expense
    )

    if projected_utilization >= 100:

        risk = "HIGH"

        recommendation = (
            "Projected spending may exceed the monthly "
            "budget. Management should reduce unnecessary "
            "expenses and review high-cost categories."
        )

    elif projected_utilization >= 85:

        risk = "MEDIUM"

        recommendation = (
            "Projected spending is approaching the budget "
            "limit. Monitor discretionary expenses carefully."
        )

    else:

        risk = "LOW"

        recommendation = (
            "Projected spending is within the expected "
            "monthly budget range."
        )

    return {
        "company_name": company_name,
        "monthly_budget": float(monthly_budget),
        "days_analyzed": days_analyzed,
        "total_expense": float(total_expense),
        "daily_burn_rate": round(daily_burn_rate, 2),
        "projected_expense": round(projected_expense, 2),
        "projected_utilization": round(
            projected_utilization,
            2
        ),
        "projected_variance": round(
            projected_variance,
            2
        ),
        "risk": risk,
        "recommendation": recommendation
    }