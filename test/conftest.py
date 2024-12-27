import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.orm.mapper_registry import engine, start_mapper


@pytest.fixture(scope="session", autouse=True)
def mapper():
    start_mapper()


@pytest.fixture(scope="function")
def session_maker():
    """Creates a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)

    yield Session

    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def session(session_maker):
    session = session_maker()

    yield session

    session.close()
