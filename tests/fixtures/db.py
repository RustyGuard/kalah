import pytest

from src.database import BaseModel, engine


@pytest.fixture(scope="function", autouse=True)
def drop_create_db():
    with engine.begin():
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        yield
        BaseModel.metadata.drop_all(engine)
