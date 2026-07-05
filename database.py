"""
app.py
------
A small REST API for tracking personal expenses.

Endpoints:
  GET    /expenses          -> list all expenses
  GET    /expenses/<id>     -> get one expense
  POST   /expenses          -> add a new expense
  PUT    /expenses/<id>     -> update an expense
  DELETE /expenses/<id>     -> delete an expense
  GET    /expenses/summary  -> total spend + breakdown by category

Run it with:
    python app.py

Then visit http://127.0.0.1:5000/expenses in your browser or Postman.
"""

from flask import Flask, request, jsonify
import database

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Expense Tracker API is running. Try GET /expenses"})


@app.route("/expenses", methods=["GET"])
def list_expenses():
    expenses = database.get_all_expenses()
    return jsonify(expenses)


@app.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = database.get_expense_by_id(expense_id)
    if expense is None:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify(expense)


@app.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()

    required_fields = ["description", "category", "amount", "date"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    new_id = database.add_expense(
        data["description"], data["category"], data["amount"], data["date"]
    )
    return jsonify({"message": "Expense added", "id": new_id}), 201


@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    if database.get_expense_by_id(expense_id) is None:
        return jsonify({"error": "Expense not found"}), 404

    data = request.get_json()
    database.update_expense(
        expense_id,
        data["description"],
        data["category"],
        data["amount"],
        data["date"],
    )
    return jsonify({"message": "Expense updated"})


@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    if database.get_expense_by_id(expense_id) is None:
        return jsonify({"error": "Expense not found"}), 404

    database.delete_expense(expense_id)
    return jsonify({"message": "Expense deleted"})


@app.route("/expenses/summary", methods=["GET"])
def summary():
    """A tiny bit of data analysis: total spend + spend per category."""
    expenses = database.get_all_expenses()
    total = sum(e["amount"] for e in expenses)

    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    return jsonify({"total_spent": round(total, 2), "by_category": by_category})


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)
