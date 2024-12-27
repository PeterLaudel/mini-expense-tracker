from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .event import ExpenseCreatedEvent


class Visitor(ABC):
    @abstractmethod
    def visit_expense_created(self, expense_created: "ExpenseCreatedEvent") -> None:
        pass
