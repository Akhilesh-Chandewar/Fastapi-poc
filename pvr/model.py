from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie_name : str = Field(index=True)
    reviewer_name : str 
    rating : int = Field(ge=1, le=5)
    comment : Optional[str] = Field(default=None)
    created_at : datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at : datetime.datetime = Field(default_factory=datetime.datetime.now)

class ReviewCreate(SQLModel):
    movie_name : str
    reviewer_name : str 
    rating : int = Field(ge=1, le=5)
    comment : Optional[str] = Field(default=None)

class ReviewUpdate(SQLModel):
    movie_name : Optional[str] = None
    reviewer_name : Optional[str] = None
    rating : Optional[int] = Field(default=None, ge=1, le=5)
    comment : Optional[str] = Field(default=None)

class ReviewRead(SQLModel):
    id: int
    movie_name : str
    reviewer_name : str 
    rating : int
    comment : Optional[str] = None
    created_at : datetime.datetime
    updated_at : datetime.datetime