from types import TracebackType
from typing import Self, override

from sqlalchemy.orm import Session, sessionmaker

from src.interfaces.expenses_unit_of_work import ExpensesUnitOfWork
from src.repositories.sql_expenses import SqlExpenses


class SqlExpensesUnitOfWork(ExpensesUnitOfWork):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ):
        self._session_factory = session_factory

    @override
    def __enter__(self) -> Self:
        self._session = self._session_factory()
        self._expenses_repository = SqlExpenses(self._session)
        return super().__enter__()

    @override
    def __exit__(
        self,
        _type: type[BaseException] | None,
        _value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        super().__exit__(_type, _value, _traceback)
        self._session.close()

    @override
    def commit(self) -> None:
        self._session.commit()

    @override
    def rollback(self) -> None:
        self._session.rollback()
