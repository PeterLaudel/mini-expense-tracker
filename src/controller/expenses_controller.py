from datetime import datetime

from sqlalchemy.orm import Session, sessionmaker

from src.orm.mapper_registry import DEFAULT_SESSION_FACTORY
from src.services.expenses_adder import ExpensesAdder
from src.unit_of_works.sql_expenses_unit_of_work import SqlExpensesUnitOfWork


class ExpensesController:
    def __init__(self) -> None:
        pass

    def add_expenses(
        self, session_maker: sessionmaker[Session] = DEFAULT_SESSION_FACTORY
    ) -> None:
        uow = SqlExpensesUnitOfWork(session_maker)
        ExpensesAdder(uow).add_expense(
            date=datetime.now(),
            category="food",
            amount=100.0,
            description="lunch",
        )
