from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import registry, sessionmaker

from src.environment import postgres_url
from src.models.expense import Expense

engine = create_engine(postgres_url())
metadata = MetaData()
metadata.reflect(bind=engine)
mapper_registry = registry(metadata=metadata)
DEFAULT_SESSION_FACTORY = sessionmaker(bind=engine)


def start_mapper() -> None:
    mapper_registry.map_imperatively(
        Expense,
        metadata.tables["expense"],
    )
