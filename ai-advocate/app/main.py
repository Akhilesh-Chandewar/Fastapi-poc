from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db

from app.routes.contract import router as contract_router
from app.routes.analysis import router as analysis_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Advocate",
    description="An AI-powered platform for legal advocacy and support.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(contract_router)
app.include_router(analysis_router)