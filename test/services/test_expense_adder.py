from datetime import datetime
from typing import override
from unittest.mock import Mock

import pytest

from src.interfaces.repository import Repository
from src.models.expense import Expense
from src.services.expenses_adder import ExpensesAdder, ExpensesUnitOfWork
from test.factories.expense_factory import ExpenseFactory


class FakeExpensesRepository(Repository[Expense]):
    def __init__(self, expenses: list[Expense] | None = None):
        self.expenses = expenses or []

    def add(self, *, date: str, category: str, amount: float, description: str) -> None:
        self.expenses.append(
            ExpenseFactory(
                date=date,
                category=category,
                amount=amount,
                description=description,
            )
        )

    def all(self):
        return self.expenses


class FakeExpensesUnitOfWork(ExpensesUnitOfWork):
    def __init__(self, expenses: Repository[Expense]):
        self._expenses = expenses
        self.commited = False

    @override
    @property
    def expenses(self):
        return self._expenses

    @override
    def commit(self):
        self.commited = True

    @override
    def rollback(self):
        pass


def test_expense_adder_adds_expense():
    expenses = FakeExpensesRepository()
    uow = FakeExpensesUnitOfWork(expenses)
    date = datetime.now()
    ExpensesAdder(uow).add_expense(
        date=date,
        category="food",
        amount=100.0,
        description="lunch",
    )
    assert len(expenses.all()) == 1
    assert expenses.all()[0].date == date
    assert expenses.all()[0].category == "food"
    assert expenses.all()[0].amount == 100.0
    assert expenses.all()[0].description == "lunch"
    assert uow.commited


def test_expense_adder_rolls_back_on_exception():
    exception_list = Mock(spec=list)
    exception_list.append.side_effect = Exception("Boom!")
    expenses = FakeExpensesRepository(exception_list)
    uow = FakeExpensesUnitOfWork(expenses)
    with pytest.raises(Exception):
        ExpensesAdder(uow).add_expense(
            date="2021-01-01",
            category="food",
            amount=100.0,
            description="lunch",
        )
    assert not uow.commited
