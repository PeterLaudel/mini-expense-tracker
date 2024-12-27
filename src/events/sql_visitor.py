from typing import TYPE_CHECKING, override

from sqlalchemy.orm import Session

from .visitor import Visitor

if TYPE_CHECKING:
    from .event import ExpenseCreatedEvent


class SqlVisitor(Visitor):
    def __init__(self, session: Session):
        self._session = session

    @override
    def visit_expense_created(self, expense_created: "ExpenseCreatedEvent") -> None:
        print(
            f"INSERT INTO expenses (date, category, amount, description) VALUES ('{expense_created.expense.date}', '{expense_created.expense.category}', {expense_created.expense.amount}, '{expense_created.expense.description}');"
        )
