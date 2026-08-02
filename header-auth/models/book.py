from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field as SQLField, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: Optional[int] = SQLField(default=None, primary_key=True)
    title: str = SQLField(index=True, min_length=1, max_length=200)
    author: str = SQLField(index=True, min_length=1, max_length=100)
    description: Optional[str] = SQLField(default=None, max_length=1000)
    price: float = SQLField(ge=0)
    is_sold: bool = SQLField(default=False)
    created_at: datetime = SQLField(default_factory=utcnow)
    updated_at: datetime = SQLField(default_factory=utcnow)

    # Relationships
    user_id: Optional[int] = SQLField(default=None, foreign_key="users.id", index=True)
    owner: Optional["User"] = Relationship(back_populates="books")


class BookCreate(SQLModel):
    title: str = SQLField(min_length=1, max_length=200)
    author: str = SQLField(min_length=1, max_length=100)
    description: Optional[str] = SQLField(default=None, max_length=1000)
    price: float = SQLField(ge=0)
    is_sold: bool = False
    owner_id: int


class BookUpdate(SQLModel):
    title: Optional[str] = SQLField(default=None, min_length=1, max_length=200)
    author: Optional[str] = SQLField(default=None, min_length=1, max_length=100)
    description: Optional[str] = SQLField(default=None, max_length=1000)
    price: Optional[float] = SQLField(default=None, ge=0)
    is_sold: Optional[bool] = None
    owner_id: Optional[int] = None


class BookRead(SQLModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    price: float
    is_sold: bool
    created_at: datetime
    updated_at: datetime


Book.model_rebuild()