from abc import abstractmethod
from datetime import datetime

from src.interfaces.expenses_repository import ExpensesRepository
from src.interfaces.unit_of_work import UnitOfWork


class ExpensesUnitOfWork(UnitOfWork):
    @property
    @abstractmethod
    def expenses(self) -> ExpensesRepository:
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
            uow.expenses.add(
                date=date,
                category=category,
                amount=amount,
                description=description,
            )
            uow.commit()
