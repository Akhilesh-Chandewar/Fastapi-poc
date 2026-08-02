from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorResponse:
    def __init__(self, status: str, error_code: str, message: str, details=None):
        self.status = status
        self.error_code = error_code
        self.message = message
        self.details = details

    def to_dict(self) -> dict:
        body = {
            "status": self.status,
            "error_code": self.error_code,
            "message": self.message,
        }
        if self.details is not None:
            body["details"] = self.details
        return body


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                status="error",
                error_code="http_error",
                message=str(exc.detail),
            ).to_dict(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        details = [
            {"loc": list(err.get("loc", [])), "msg": err.get("msg", ""), "type": err.get("type", "")}
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                status="error",
                error_code="validation_error",
                message="Request validation failed",
                details=details,
            ).to_dict(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status="error",
                error_code="internal_error",
                message="Internal server error",
            ).to_dict(),
        )