from datetime import datetime
from typing import override
from unittest.mock import Mock

import pytest

from src.events.event import ExpenseCreatedEvent
from src.events.event_handler import EventHandler
from src.events.visitor import Visitor
from src.interfaces.repository import Repository
from src.models.expense import Expense
from src.services.expenses_adder import ExpensesAdder, ExpensesUnitOfWork
from test.factories.expense_factory import ExpenseFactory


class FakeVisitor(Visitor):
    def __init__(self):
        self.visit_expense_created_called = False

    @override
    def visit_expense_created(self, event: ExpenseCreatedEvent) -> None:
        self.visit_expense_created_called = True


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
    def __init__(self, expenses: Repository[Expense], event_handler: EventHandler):
        self._event_handler = event_handler
        self._expenses = expenses
        self.commited = False

    @override
    @property
    def event_handler(self):
        return self._event_handler

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


@pytest.fixture
def repository():
    return FakeExpensesRepository()


@pytest.fixture
def visitor():
    return FakeVisitor()


def test_expense_adder_adds_expense(visitor, repository):
    uow = FakeExpensesUnitOfWork(repository, EventHandler(visitor))
    date = datetime.now()
    ExpensesAdder(uow).add_expense(
        date=date,
        category="food",
        amount=100.0,
        description="lunch",
    )

    expenses = repository.all()
    assert len(expenses) == 1
    assert expenses[0].date == date
    assert expenses[0].category == "food"
    assert expenses[0].amount == 100.0
    assert expenses[0].description == "lunch"
    assert uow.commited


def test_expense_adder_rolls_back_on_exception(visitor):
    exception_list = Mock(spec=list)
    exception_list.append.side_effect = Exception("Boom!")
    expenses = FakeExpensesRepository(exception_list)
    uow = FakeExpensesUnitOfWork(expenses, visitor)
    with pytest.raises(Exception):
        ExpensesAdder(uow).add_expense(
            date="2021-01-01",
            category="food",
            amount=100.0,
            description="lunch",
        )
    assert not uow.commited


def test_expense_adder_adds_expense_created_event(visitor):
    expenses = FakeExpensesRepository()
    uow = FakeExpensesUnitOfWork(expenses, EventHandler(visitor))
    ExpensesAdder(uow).add_expense(
        date="2021-01-01",
        category="food",
        amount=100.0,
        description="lunch",
    )
    assert visitor.visit_expense_created_called
