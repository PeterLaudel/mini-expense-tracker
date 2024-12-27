import pytest
from sqlalchemy import text

from src.controller.expenses_controller import ExpensesController


@pytest.fixture
def expense_controller():
    return ExpensesController()


# @pytest.mark.skip(reason="This test is not implemented yet.")
def test_expenses_controller_adds_expense(expense_controller, session_maker):
    expense_controller.add_expenses(session_maker)

    session = session_maker()
    assert len(session.execute(text("SELECT * FROM expense")).fetchall()) == 1


def test_expenes_controller_adds_expense_adds_expense_create_event(
    expense_controller, session_maker
):
    expense_controller.add_expenses(session_maker)

    session = session_maker()
    all = session.execute(text("SELECT * FROM event")).fetchall()
    assert len(all) == 1
