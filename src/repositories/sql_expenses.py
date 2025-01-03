from datetime import datetime
from typing import Self

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src.interfaces.expenses_repository import ExpensesRepository
from src.models.expense import Expense


class SqlExpenses(ExpensesRepository):
    def __init__(self, session: Session):
        self._session = session
        self._select = select(Expense)

    def add(
        self, *, date: datetime, category: str, amount: float, description: str
    ) -> Expense:
        result = self._session.scalars(
            insert(Expense)
            .values(
                date=date, category=category, amount=amount, description=description
            )
            .returning(Expense)
        )
        return result.one()

    def before(self, *, date: datetime) -> Self:
        self._select = self._select.where(Expense.date < date)  # type: ignore[arg-type]
        return self

    def after(self, *, date: datetime) -> Self:
        self._select = self._select.where(Expense.date > date)  # type: ignore[arg-type]
        return self

    def with_category(self, *, category: str) -> Self:
        self._select = self._select.where(Expense.category == category)  # type: ignore[arg-type]
        return self

    def all(self) -> list[Expense]:
        expenses = self._session.scalars(self._select).all()
        self._select = select(Expense)
        return list(expenses)
