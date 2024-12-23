from datetime import datetime
from unittest.mock import ANY

from sqlalchemy import text

from src.models.expense import Expense
from src.repositories.sql_expenses import SqlExpenses


def test_adds_expense(session):
    expenses = SqlExpenses(session)
    expenses.add(
        date=datetime.fromisoformat("2021-01-01T00:00:00"),
        category="Food",
        amount=10.0,
        description="Lunch",
    )

    assert session.execute(text("SELECT * FROM expense")).fetchall() == [
        (
            ANY,
            datetime.fromisoformat("2021-01-01T00:00:00"),
            "Food",
            10.0,
            "Lunch",
        )
    ]


def test_returns_expenses(session):
    session.execute(
        text(
            "INSERT INTO expense (date, category, amount, description) VALUES "
            "('2021-01-01T00:00:00', 'Food', 10.0, 'Lunch')"
        )
    )

    expenses = SqlExpenses(session)
    assert expenses.all() == [
        Expense(
            ANY,
            datetime.fromisoformat("2021-01-01T00:00:00"),
            "Food",
            10.0,
            "Lunch",
        )
    ]
