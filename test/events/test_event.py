import json
from typing import override

from src.events.event import ExpenseCreatedEvent
from src.events.visitor import Visitor
from test.factories.expense_factory import ExpenseFactory


class FakeVisitor(Visitor):
    def __init__(self):
        self.visit_expense_created_called = False

    @override
    def visit_expense_created(self, event: ExpenseCreatedEvent) -> None:
        self.visit_expense_created_called = True


def test_expense_created_event_calls_visitor():
    visitor = FakeVisitor()
    event = ExpenseCreatedEvent(ExpenseFactory())
    event.accept(visitor)
    assert visitor.visit_expense_created_called is True


def test_expense_created_event_type():
    event = ExpenseCreatedEvent(ExpenseFactory())
    assert event.type() == f"expense.{event.expense.id}.created"


def test_expenst_created_event_json():
    event = ExpenseCreatedEvent(ExpenseFactory())
    assert json.loads(event.json()) == {
        "data": {
            "id": event.expense.id,
            "date": event.expense.date.isoformat(),
            "category": event.expense.category,
            "amount": event.expense.amount,
            "description": event.expense.description,
        },
        "type": f"expense.{event.expense.id}.created",
    }
