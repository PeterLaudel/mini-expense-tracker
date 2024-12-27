from src.events.event import ExpenseCreatedEvent
from src.events.sql_visitor import SqlVisitor
from test.factories.expense_factory import ExpenseFactory


def test_sql_visitor(session):
    visitor = SqlVisitor(session)
    event = ExpenseCreatedEvent(ExpenseFactory())
    event.accept(visitor)
    assert True
