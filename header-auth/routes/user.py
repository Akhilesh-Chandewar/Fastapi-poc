from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, func, select

from auth import check_api_key
from database import get_session
from models.book import Book, BookRead
from models.user import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_or_404(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_api_key)],
)
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
):
    existing = session.exec(
        select(User).where((User.username == user.username) | (User.email == str(user.email)))
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead], dependencies=[Depends(check_api_key)])
async def read_users(
    search: str | None = Query(None, description="Filter by username or email"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    session: Session = Depends(get_session),
):
    query = select(User)
    if search:
        query = query.where(
            User.username.contains(search) | User.email.contains(search)
        )
    query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
    return session.exec(query).all()


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(check_api_key)])
async def read_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    return get_user_or_404(session, user_id)


@router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(check_api_key)])
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
):
    db_user = get_user_or_404(session, user_id)
    data = user_update.model_dump(exclude_unset=True)
    if "email" in data:
        existing = session.exec(select(User).where(User.email == str(data["email"]))).first()
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email already in use")
    if "username" in data:
        existing = session.exec(select(User).where(User.username == data["username"])).first()
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Username already in use")
    for key, value in data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_api_key)],
)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = get_user_or_404(session, user_id)
    session.delete(db_user)
    session.commit()


@router.get(
    "/{user_id}/books",
    response_model=List[BookRead],
    tags=["Users", "Books"],
    dependencies=[Depends(check_api_key)],
)
async def read_user_books(
    user_id: int,
    session: Session = Depends(get_session),
):
    get_user_or_404(session, user_id)
    books = session.exec(select(Book).where(Book.user_id == user_id)).all()
    return books