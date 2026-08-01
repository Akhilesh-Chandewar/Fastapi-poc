from http import HTTPStatus
from fastapi.responses import JSONResponse
from fastapi import Request 

class PincodeNotFoundException(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode

class InvalidPincodeException(Exception):
    def __init__(self, pincode: str , reason: str = "Invalid pincode format"):
        self.pincode = pincode
        self.reason = reason

async def pincode_not_found_exception_handler(request: Request, exc: PincodeNotFoundException):
    return JSONResponse(
        status_code = HTTPStatus.NOT_FOUND,
        content={
            "error": "Pincode Not Found",
            "message": f"Pincode '{exc.pincode}' not found.",
            },
    )

async def invalid_pincode_exception_handler(request: Request, exc: InvalidPincodeException):
    return JSONResponse(
        status_code= HTTPStatus.BAD_REQUEST,
        content={
            "error": "Invalid Pincode",
            "message": f"Invalid pincode '{exc.pincode}': {exc.reason}"
        },
    )