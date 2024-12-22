from collections import defaultdict

from src.models.expense import Expense


class ExpenseAnalyzer:
    def __init__(self, expenses: list[Expense]):
        self._expenses = expenses

    def total(self) -> float:
        return sum(expense.amount for expense in self._expenses)

    def total_by_category(self) -> dict[str, float]:
        total_by_category = defaultdict(float)
        for expense in self._expenses:
            total_by_category[expense.category] += expense.amount
        return total_by_category
