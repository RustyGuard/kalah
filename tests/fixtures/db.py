from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.core.config import settings
from src.database import BaseModel


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator:
    engine = create_engine(str(settings.DATABASE_URI))

    with engine.begin():
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        yield engine
        BaseModel.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def db_session_factory(setup_test_db):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=setup_test_db))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()

