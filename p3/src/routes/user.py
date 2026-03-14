from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from src.model.model import Users


def db_dependency():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




class UserRouter:
    router = APIRouter(
        prefix="/user",
        tags=["user"]
    )