from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from auth import check_api_key
from database import get_session
from models.book import Book, BookCreate, BookRead, BookUpdate
from models.user import User

router = APIRouter(prefix="/books", tags=["Books"])


def get_book_or_404(session: Session, book_id: int) -> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post(
    "/",
    response_model=BookRead,
    status_code=201,
    dependencies=[Depends(check_api_key)],
)
async def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
):
    if not session.get(User, book.owner_id):
        raise HTTPException(status_code=400, detail="Owner user does not exist")
    db_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        price=book.price,
        is_sold=book.is_sold,
        user_id=book.owner_id,
    )
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.get("/", response_model=List[BookRead], dependencies=[Depends(check_api_key)])
async def read_books(
    title: str | None = Query(None, description="Filter by title (partial match)"),
    author: str | None = Query(None, description="Filter by author (partial match)"),
    is_sold: bool | None = Query(None, description="Filter by sold state"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    session: Session = Depends(get_session),
):
    query = select(Book)
    if title:
        query = query.where(Book.title.contains(title))
    if author:
        query = query.where(Book.author.contains(author))
    if is_sold is not None:
        query = query.where(Book.is_sold == is_sold)
    query = query.order_by(Book.created_at.desc()).offset(skip).limit(limit)
    return session.exec(query).all()


@router.get("/{book_id}", response_model=BookRead, dependencies=[Depends(check_api_key)])
async def read_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    return get_book_or_404(session, book_id)


@router.put("/{book_id}", response_model=BookRead, dependencies=[Depends(check_api_key)])
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    session: Session = Depends(get_session),
):
    db_book = get_book_or_404(session, book_id)
    data = book_update.model_dump(exclude_unset=True)
    if "owner_id" in data:
        if not session.get(User, data["owner_id"]):
            raise HTTPException(status_code=400, detail="Owner user does not exist")
        data["user_id"] = data.pop("owner_id")
    for key, value in data.items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=204, dependencies=[Depends(check_api_key)])
async def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    db_book = get_book_or_404(session, book_id)
    session.delete(db_book)
    session.commit()