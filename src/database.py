from sqlalchemy import MetaData, create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, as_declarative, sessionmaker

from src.core.config import settings

engine = create_engine(str(settings.DATABASE_URI), echo=False, pool_pre_ping=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, autocommit=False, autoflush=False
)


def get_session() -> Session:
    with async_session() as session:
        return session


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


@as_declarative(metadata=metadata)
class BaseModel:
    def __repr__(self) -> str:
        pk = inspect(self.__class__).primary_key[0].name  # type: ignore[union-attr]
        return f"<{self.__class__.__name__} {getattr(self, pk, id(self))}>"
