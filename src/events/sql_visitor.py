from typing import TYPE_CHECKING, override

from sqlalchemy import insert
from sqlalchemy.orm import Session

from src.events.event import Event
from src.orm.mapper_registry import metadata

from .visitor import Visitor

if TYPE_CHECKING:
    from .event import ExpenseCreatedEvent


class SqlVisitor(Visitor):
    def __init__(self, session: Session):
        self._session = session

    @override
    def visit_expense_created(
        self, expense_created_event: "ExpenseCreatedEvent"
    ) -> None:
        self._session.execute(
            insert(metadata.tables["event"]).values(
                type=expense_created_event.type(), json=expense_created_event.json()
            )
        )
