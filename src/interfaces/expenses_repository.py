from abc import abstractmethod
from datetime import datetime
from typing import Self

from src.models.expense import Expense

from .repository import Repository


class ExpensesRepository(Repository[Expense]):
    @abstractmethod
    def add(
        self, *, date: datetime, category: str, amount: float, description: str
    ) -> Expense:
        pass

    @abstractmethod
    def before(self, *, date: datetime) -> Self:
        pass

    @abstractmethod
    def after(self, *, date: datetime) -> Self:
        pass

    @abstractmethod
    def with_category(self, *, category: str) -> Self:
        pass
