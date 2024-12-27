from types import TracebackType
from typing import Self, override

from sqlalchemy.orm import Session, sessionmaker

from src.events.event_handler import EventHandler
from src.events.sql_visitor import SqlVisitor
from src.interfaces.expenses_repository import ExpensesRepository
from src.repositories.sql_expenses import SqlExpenses
from src.services.expenses_adder import ExpensesUnitOfWork


class SqlExpensesUnitOfWork(ExpensesUnitOfWork):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ):
        self._session_factory = session_factory
        self._expenses_repository: SqlExpenses | None = None
        self._event_handler: EventHandler | None = None

    @override
    def __enter__(self) -> Self:
        self._session = self._session_factory()
        self._expenses_repository = SqlExpenses(self._session)
        visitor = SqlVisitor(self._session)
        self._event_handler = EventHandler(visitor)
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

    @property
    @override
    def expenses(self) -> ExpensesRepository:
        if self._expenses_repository is None:
            raise ValueError("Session not available")
        return self._expenses_repository

    @property
    @override
    def event_handler(self) -> EventHandler:
        if self._event_handler is None:
            raise ValueError("Session not available")

        return self._event_handler

    @override
    def commit(self) -> None:
        self._session.commit()

    @override
    def rollback(self) -> None:
        self._session.rollback()
