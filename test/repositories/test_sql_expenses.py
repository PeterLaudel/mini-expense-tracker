from datetime import datetime
from unittest.mock import ANY

from sqlalchemy import text

from src.models.expense import Expense
from src.repositories.sql_expenses import SqlExpenses


def test_adds_expense(session):
    expenses = SqlExpenses(session)
    expense = expenses.add(
        date=datetime.fromisoformat("2021-01-01T00:00:00"),
        category="Food",
        amount=10.0,
        description="Lunch",
    )

    assert expense == Expense(
        id=ANY,
        date=datetime.fromisoformat("2021-01-01T00:00:00"),
        category="Food",
        amount=10.0,
        description="Lunch",
    )


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


def test_before_filters_expenses(session):
    session.execute(
        text(
            "INSERT INTO expense (date, category, amount, description) VALUES "
            "('2021-01-01T00:00:00', 'Food', 10.0, 'Lunch'), "
            "('2021-01-02T00:00:00', 'Food', 20.0, 'Dinner')"
        )
    )

    expenses = SqlExpenses(session)
    assert expenses.before(
        date=datetime.fromisoformat("2021-01-02T00:00:00")
    ).all() == [
        Expense(
            ANY,
            datetime.fromisoformat("2021-01-01T00:00:00"),
            "Food",
            10.0,
            "Lunch",
        )
    ]


def test_after_filters_expenses(session):
    session.execute(
        text(
            "INSERT INTO expense (date, category, amount, description) VALUES "
            "('2021-01-01T00:00:00', 'Food', 10.0, 'Lunch'), "
            "('2021-01-02T00:00:00', 'Food', 20.0, 'Dinner')"
        )
    )

    expenses = SqlExpenses(session)
    assert expenses.after(date=datetime.fromisoformat("2021-01-01T00:00:00")).all() == [
        Expense(
            ANY,
            datetime.fromisoformat("2021-01-02T00:00:00"),
            "Food",
            20.0,
            "Dinner",
        )
    ]


def test_filter_expenses_by_category(session):
    session.execute(
        text(
            "INSERT INTO expense (date, category, amount, description) VALUES "
            "('2021-01-01T00:00:00', 'Food', 10.0, 'Lunch'), "
            "('2021-01-02T00:00:00', 'Transport', 20.0, 'Bus')"
        )
    )

    expenses = SqlExpenses(session)
    assert expenses.with_category(category="Food").all() == [
        Expense(
            ANY,
            datetime.fromisoformat("2021-01-01T00:00:00"),
            "Food",
            10.0,
            "Lunch",
        )
    ]
    assert expenses.with_category(category="Transport").all() == [
        Expense(
            ANY,
            datetime.fromisoformat("2021-01-02T00:00:00"),
            "Transport",
            20.0,
            "Bus",
        )
    ]
    assert expenses.with_category(category="Other").all() == []
