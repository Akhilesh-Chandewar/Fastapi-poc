from sqlmodel import SQLModel, Session, create_engine

from config import settings

# Import models so that their tables are registered on SQLModel.metadata
from models.book import Book  # noqa: F401
from models.user import User  # noqa: F401

_connect_args = {}
if settings.database_url.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args=_connect_args,
)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session