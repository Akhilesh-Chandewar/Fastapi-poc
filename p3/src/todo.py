from fastapi import FastAPI
from src.database.database import engine, Base

Base.metadata.create_all(bind=engine)


class TodoApp:
    def __init__(self):
        self.app = FastAPI()
