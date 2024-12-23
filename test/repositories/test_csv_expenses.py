from datetime import datetime
from io import StringIO

import pytest

from src.models.expense import Expense
from src.repositories.csv_expenses import CsvExpenses


@pytest.fixture
def io():
    return StringIO()


def test_adds_header_line_when_file_is_empty(io):
    CsvExpenses(io)

    assert io.getvalue() == "id,date,category,amount,description\n"


def test_adds_expense(io):
    expenses = CsvExpenses(io)
    expenses.add(
        date=datetime.fromisoformat("2021-01-01T00:00:00"),
        category="Food",
        amount=10.0,
        description="Lunch",
    )

    assert (
        io.getvalue()
        == "id,date,category,amount,description\n1,2021-01-01T00:00:00,Food,10.0,Lunch\n"
    )


def test_returns_expenses(io):
    io.write("id,date,category,amount,description\n")
    io.write("1,2021-01-01T00:00:00,Food,10.0,Lunch\n")
    io.seek(0)

    expenses = CsvExpenses(io)
    assert expenses.all() == [
        Expense(
            id=1,
            date=datetime.fromisoformat("2021-01-01T00:00:00"),
            category="Food",
            amount=10,
            description="Lunch",
        )
    ]


def test_before_filters_expenses(io):
    io.write("id,date,category,amount,description\n")
    io.write("1,2021-01-01T00:00:00,Food,10.0,Lunch\n")
    io.write("1,2021-01-02T00:00:00,Food,20.0,Dinner\n")
    io.seek(0)

    expenses = CsvExpenses(io)
    assert expenses.before(
        date=datetime.fromisoformat("2021-01-02T00:00:00")
    ).all() == [
        Expense(
            id=1,
            date=datetime.fromisoformat("2021-01-01T00:00:00"),
            category="Food",
            amount=10,
            description="Lunch",
        )
    ]


def test_after_filters_expenses(io):
    io.write("id,date,category,amount,description\n")
    io.write("1,2021-01-01T00:00:00,Food,10.0,Lunch\n")
    io.write("1,2021-01-02T00:00:00,Food,20.0,Dinner\n")
    io.seek(0)

    expenses = CsvExpenses(io)
    assert expenses.after(date=datetime.fromisoformat("2021-01-01T00:00:00")).all() == [
        Expense(
            id=1,
            date=datetime.fromisoformat("2021-01-02T00:00:00"),
            category="Food",
            amount=20,
            description="Dinner",
        )
    ]
