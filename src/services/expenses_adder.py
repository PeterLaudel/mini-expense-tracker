from abc import abstractmethod
from datetime import datetime

from src.events.event import ExpenseCreatedEvent
from src.events.event_handler import EventHandler
from src.interfaces.expenses_repository import ExpensesRepository
from src.interfaces.unit_of_work import UnitOfWork


class ExpensesUnitOfWork(UnitOfWork):
    @property
    @abstractmethod
    def expenses(self) -> ExpensesRepository:
        pass

    @property
    @abstractmethod
    def event_handler(self) -> EventHandler:
        pass


class ExpensesAdder:
    def __init__(self, expenses_unit_of_work: ExpensesUnitOfWork):
        self._expenses_unit_of_work = expenses_unit_of_work

    def add_expense(
        self,
        *,
        date: datetime,
        category: str,
        amount: float,
        description: str,
    ) -> None:
        with self._expenses_unit_of_work as uow:
            expense = uow.expenses.add(
                date=date,
                category=category,
                amount=amount,
                description=description,
            )
            uow.event_handler.add_event(ExpenseCreatedEvent(expense))
            uow.commit()
