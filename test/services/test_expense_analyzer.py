from io import StringIO

import pytest

from src.services.expense_analyzer import ExpenseAnalyzer
from test.factories import ExpenseFactory


@pytest.fixture
def expenses():
    return [
        ExpenseFactory.build(amount=10.0, category="category1"),
        ExpenseFactory.build(amount=20.0, category="category2"),
    ]


def test_computes_total_expenses(expenses):
    assert ExpenseAnalyzer(expenses).total() == 30.0


def test_computes_total_by_category(expenses):
    assert ExpenseAnalyzer(expenses).total_by_category() == {
        "category1": 10.0,
        "category2": 20.0,
    }
