from database import get_connection


def run_auditor_agent():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(amount), 0),
            COALESCE(AVG(amount), 0),
            COALESCE(MAX(amount), 0)
        FROM transactions
    """)

    summary = cursor.fetchone()

    transaction_count = summary[0]
    total_expense = summary[1]
    average_expense = summary[2]
    highest_expense = summary[3]

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM transactions
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    category_rows = cursor.fetchall()

    cursor.execute("""
        SELECT
            department,
            SUM(amount)
        FROM transactions
        GROUP BY department
        ORDER BY SUM(amount) DESC
    """)

    department_rows = cursor.fetchall()

    cursor.execute("""
        SELECT
            transaction_id,
            transaction_date,
            department,
            category,
            vendor,
            amount
        FROM transactions
        WHERE amount >= (
            SELECT AVG(amount) * 3
            FROM transactions
        )
        ORDER BY amount DESC
        LIMIT 20
    """)

    unusual_transactions = cursor.fetchall()

    cursor.execute("""
        SELECT
            vendor,
            SUM(amount),
            COUNT(*)
        FROM transactions
        GROUP BY vendor
        ORDER BY SUM(amount) DESC
        LIMIT 10
    """)

    vendor_rows = cursor.fetchall()

    conn.close()

    categories = []

    for category, amount in category_rows:

        percentage = 0

        if total_expense > 0:
            percentage = (amount / total_expense) * 100

        categories.append({
            "category": category,
            "amount": float(amount),
            "percentage": round(percentage, 2)
        })

    departments = []

    for department, amount in department_rows:

        percentage = 0

        if total_expense > 0:
            percentage = (amount / total_expense) * 100

        departments.append({
            "department": department,
            "amount": float(amount),
            "percentage": round(percentage, 2)
        })

    findings = []

    if categories:

        highest_category = categories[0]

        findings.append(
            f"{highest_category['category']} is the highest "
            f"spending category with "
            f"₹{highest_category['amount']:,.2f}."
        )

    if departments:

        highest_department = departments[0]

        findings.append(
            f"{highest_department['department']} has the "
            f"highest departmental spending."
        )

    if unusual_transactions:

        findings.append(
            f"{len(unusual_transactions)} potentially unusual "
            f"high-value transactions were detected."
        )

    else:

        findings.append(
            "No unusually high transactions were detected."
        )

    if vendor_rows:

        findings.append(
            f"{vendor_rows[0][0]} is the highest-spend vendor."
        )

    return {
        "transaction_count": transaction_count,
        "total_expense": float(total_expense),
        "average_expense": float(average_expense),
        "highest_expense": float(highest_expense),
        "categories": categories,
        "departments": departments,
        "unusual_transactions": unusual_transactions,
        "vendors": vendor_rows,
        "findings": findings
    }