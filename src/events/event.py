import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from src.models.expense import Expense

from .visitor import Visitor

if TYPE_CHECKING:
    from mypy.types import JsonDict


class Event(ABC):
    @abstractmethod
    def type(self) -> str:
        pass

    def json(self) -> str:
        return json.dumps(
            {  # type: ignore[misc]
                "data": self.data(),
                "type": self.type(),
            }
        )

    @abstractmethod
    def data(self) -> "JsonDict":
        pass

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


class ExpenseCreatedEvent(Event):
    def __init__(self, expense: Expense):
        self._expense = expense

    @override
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_expense_created(self)

    @override
    def type(self) -> str:
        return f"expense.{self._expense.id}.created"

    @override
    def data(self) -> "JsonDict":
        return {  # type: ignore[misc]
            "id": self._expense.id,
            "date": self._expense.date.isoformat(),
            "category": self._expense.category,
            "amount": self._expense.amount,
            "description": self._expense.description,
        }

    @property
    def expense(self) -> Expense:
        return self._expense
