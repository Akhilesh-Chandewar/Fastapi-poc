import logging
import time

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.data import menu_items
from app.exceptions import (
    AppException,
    InvalidCategoryError,
    InvalidRequestError,
    ItemNotFoundException,
)
from app.models import ErrorDetail, ErrorResponse, MenuResponse

logger = logging.getLogger("food-menu")

app = FastAPI(
    title=settings.app_name,
    description="An API for managing a food menu, allowing users to view, add, update, and delete menu items.",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.debug,
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
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time_ms = (time.perf_counter() - start_time) * 1000
    logger.info(
        "%s %s -> %s (%.2fms)",
        request.method,
        request.url.path,
        response.status_code,
        process_time_ms,
    )
    response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"
    return response


def _build_error_response(exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            error_code=exc.error_code,
            message=exc.message,
        ).model_dump(),
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning("%s -> %s (%s)", request.url.path, exc.error_code, exc.message)
    return _build_error_response(exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("%s -> HTTP %s: %s", request.url.path, exc.status_code, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            error_code="http_error",
            message=str(exc.detail),
        ).model_dump(),
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        ErrorDetail(
            loc=[str(part) for part in err.get("loc", [])],
            msg=err.get("msg", "Invalid value"),
            type=err.get("type", "value_error"),
        )
        for err in exc.errors()
    ]
    logger.warning("%s -> validation error: %s", request.url.path, details)
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status="error",
            error_code="validation_error",
            message="Request validation failed",
            details=details,
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status="error",
            error_code="internal_error",
            message="Internal server error",
        ).model_dump(),
    )


@app.get("/", tags=["health"])
async def read_root():
    return {
        "Message": f"Welcome to {settings.app_name}!",
        "Status": "Success",
        "Docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "environment": settings.environment}


@app.get("/menu", response_model=MenuResponse, tags=["menu"])
async def get_menu(
    category: str | None = Query(
        None,
        min_length=1,
        max_length=50,
        description="Filter menu items by category",
    ),
    available: bool | None = Query(None, description="Filter menu items by availability"),
):
    filtered_items = menu_items
    if category:
        filtered_items = [
            item for item in filtered_items if item["category"].lower() == category.lower()
        ]
        if not filtered_items:
            raise InvalidCategoryError(f"No menu items found for category '{category}'")
    if available is not None:
        filtered_items = [
            item for item in filtered_items if item["is_available"] == available
        ]
    return MenuResponse(
        status="success",
        count=len(filtered_items),
        menu_items=filtered_items,
    )


@app.get("/menu/{item_id}", response_model=MenuResponse, tags=["menu"])
async def get_menu_item(item_id: int):
    if item_id < 1:
        raise InvalidRequestError("item_id must be a positive integer")
    item = next((item for item in menu_items if item["id"] == item_id), None)
    if item is None:
        raise ItemNotFoundException(f"Menu item with id {item_id} not found")
    return MenuResponse(status="success", count=1, menu_items=[item])
