import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.environment import postgres_url
from src.orm.mapper_registry import start_mapper


@pytest.fixture(scope="session")
def engine():
    start_mapper()
    return create_engine(postgres_url())


@pytest.fixture(scope="function")
def session(engine):
    """Creates a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
