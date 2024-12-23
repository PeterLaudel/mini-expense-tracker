import io
from datetime import datetime
from typing import Callable, Self, TextIO

from src.interfaces.expenses_repository import ExpensesRepository
from src.models.expense import Expense


class CsvExpenses(ExpensesRepository):
    def __init__(self, csv_file: TextIO):
        self._csv_file = csv_file
        # seek to end of file to avoid reading the header
        self._csv_file.seek(0, io.SEEK_END)
        if self._csv_file.tell() == 0:
            self._csv_file.write("id,date,category,amount,description\n")
        self._csv_file.seek(0)
        self._filters: list[Callable[[Expense], bool]] = []

    def add(
        self, *, date: datetime, category: str, amount: float, description: str
    ) -> None:
        self._csv_file.seek(0, io.SEEK_END)
        self._csv_file.write(
            f"1,{date.isoformat()},{category},{amount},{description}\n"
        )
        self._csv_file.seek(0)

    def all(self) -> list[Expense]:
        self._csv_file.seek(0)
        lines = self._csv_file.readlines()
        expenses = [
            Expense(
                id=int(id),
                date=datetime.fromisoformat(date),
                category=category,
                amount=float(amount),
                description=description,
            )
            for id, date, category, amount, description in (
                line.strip().split(",") for line in lines[1:]
            )
        ]
        for _filter in self._filters:
            expenses = list(filter(_filter, expenses))
            self._filters.clear()
        self._csv_file.seek(0)
        return expenses

    def before(self, *, date: datetime) -> Self:
        self._filters.append(lambda expense: expense.date < date)
        return self

    def after(self, *, date: datetime) -> Self:
        self._filters.append(lambda expense: expense.date > date)
        return self

    def with_category(self, *, category: str) -> Self:
        self._filters.append(lambda expense: expense.category == category)
        return self
