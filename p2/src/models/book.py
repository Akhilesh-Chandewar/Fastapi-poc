from enum import Enum
from datetime import date
from pydantic import BaseModel


class RatingEnum(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: RatingEnum
    release_date: date    


