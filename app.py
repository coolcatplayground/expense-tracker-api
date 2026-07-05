"""
analyze.py
----------
A standalone script that shows off basic "data" skills separate from the API:
reads the expenses straight out of the SQLite database with pandas, then
prints a summary and saves a bar chart of spending by category.

Run it with:
    python analyze.py

Requires that expenses.db already has some data in it (use the API to add
a few expenses first, or run seed_data.py).
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "expenses.db"


def load_expenses():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df


def main():
    df = load_expenses()

    if df.empty:
        print("No expenses found yet. Add some via the API first!")
        return

    print("=== Expense Summary ===")
    print(f"Total spent: ${df['amount'].sum():.2f}")
    print(f"Number of transactions: {len(df)}")
    print()

    by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    print("Spending by category:")
    print(by_category)

    # Save a simple bar chart as an image
    by_category.plot(kind="bar", title="Spending by Category")
    plt.ylabel("Amount ($)")
    plt.tight_layout()
    plt.savefig("spending_by_category.png")
    print("\nSaved chart to spending_by_category.png")


if __name__ == "__main__":
    main()
