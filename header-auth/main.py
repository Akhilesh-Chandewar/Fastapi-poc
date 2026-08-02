import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import create_db_and_tables
from exceptions import ErrorResponse, register_exception_handlers
from routes.book import router as books_router
from routes.user import router as users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(settings.app_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    logger.info("Database tables created/verified")
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="Header-based API key authentication service with Users and Books resources.",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=not any("*" in origin for origin in settings.cors_origins),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s (%.2fms)", request.method, request.url.path, response.status_code, elapsed_ms)
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response


register_exception_handlers(app)


@app.get("/", tags=["root"])
async def read_root():
    return {
        "Message": f"Welcome to {settings.app_name}!",
        "Status": "Success",
        "Docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "environment": settings.environment}


api_prefix = settings.api_prefix or ""

app.include_router(users_router, prefix=api_prefix + "/api/v1")
app.include_router(books_router, prefix=api_prefix + "/api/v1")