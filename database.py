import sqlite3

DATABASE_NAME = "expenses.db"


def create_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_expense(amount, category, description, expense_date):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, expense_date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, expense_date))

    connection.commit()
    connection.close()


def get_monthly_total(year_month):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
    """, (year_month,))

    result = cursor.fetchone()[0]

    connection.close()

    return result


def get_expenses():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses
