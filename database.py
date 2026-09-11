import sqlite3
import os
import random
from datetime import datetime, timedelta


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

COMPANY_DB = os.path.join(
    DATA_DIR,
    "company_database.db"
)


def get_connection():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    return sqlite3.connect(
        COMPANY_DB
    )


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            transaction_date TEXT NOT NULL,
            department TEXT NOT NULL,
            category TEXT NOT NULL,
            vendor TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_settings (
            id INTEGER PRIMARY KEY,
            company_name TEXT NOT NULL,
            monthly_budget REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def generate_transactions(
    count=5000
):

    departments = [
        "IT",
        "Marketing",
        "Sales",
        "Human Resources",
        "Operations",
        "Finance",
        "Administration"
    ]

    categories = [
        "Software",
        "Payroll",
        "Marketing",
        "Travel",
        "Utilities",
        "Logistics",
        "Equipment",
        "Office Expenses",
        "Professional Services"
    ]

    vendors = [
        "Microsoft",
        "AWS",
        "Google Cloud",
        "Adobe",
        "Google Ads",
        "Meta Ads",
        "Air India",
        "IndiGo",
        "Ola Business",
        "DHL",
        "FedEx",
        "Dell",
        "HP",
        "Amazon Business",
        "Consulting Firm"
    ]

    payment_methods = [
        "Bank Transfer",
        "Corporate Card",
        "UPI",
        "NEFT"
    ]

    rows = []

    today = datetime.now()

    for i in range(1, count + 1):

        category = random.choice(
            categories
        )

        department = random.choice(
            departments
        )

        vendor = random.choice(
            vendors
        )

        amount = random.randint(
            2000,
            100000
        )

        transaction_date = (
            today -
            timedelta(
                days=random.randint(
                    0,
                    180
                )
            )
        ).strftime(
            "%Y-%m-%d"
        )

        payment_method = random.choice(
            payment_methods
        )

        description = (
            f"{category} business expense"
        )

        rows.append(
            (
                f"TXN{i:06d}",
                transaction_date,
                department,
                category,
                vendor,
                float(amount),
                payment_method,
                description
            )
        )

    return rows


def initialize_all():

    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    transaction_count = cursor.fetchone()[0]

    if transaction_count == 0:

        rows = generate_transactions(
            5000
        )

        cursor.executemany(
            """
            INSERT INTO transactions (
                transaction_id,
                transaction_date,
                department,
                category,
                vendor,
                amount,
                payment_method,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows
        )

    cursor.execute(
        "SELECT COUNT(*) FROM company_settings"
    )

    settings_count = cursor.fetchone()[0]

    if settings_count == 0:

        cursor.execute(
            """
            INSERT INTO company_settings (
                id,
                company_name,
                monthly_budget
            )
            VALUES (?, ?, ?)
            """,
            (
                1,
                "NovaTech Solutions Pvt. Ltd.",
                950000
            )
        )

    conn.commit()
    conn.close()


def get_company_info():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            company_name,
            monthly_budget
        FROM company_settings
        WHERE id = 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return (
            row[0],
            float(row[1])
        )

    return (
        "NovaTech Solutions Pvt. Ltd.",
        950000
    )


def get_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            transaction_id,
            transaction_date,
            department,
            category,
            vendor,
            amount,
            payment_method,
            description
        FROM transactions
        ORDER BY transaction_date DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows