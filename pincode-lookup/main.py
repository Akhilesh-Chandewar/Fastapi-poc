import re

from fastapi import FastAPI
import uvicorn

from data import pincodes
from exceptions import (
    InvalidPincodeException,
    PincodeNotFoundException,
    invalid_pincode_exception_handler,
    pincode_not_found_exception_handler,
)
from models import Pincode, PincodeResponse

app = FastAPI(
    title="Pincode Lookup API",
    description="An API for looking up pincode details.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_exception_handler(PincodeNotFoundException, pincode_not_found_exception_handler)
app.add_exception_handler(InvalidPincodeException, invalid_pincode_exception_handler)


@app.get("/")
def root():
    return {
        "Message": "Pincode lookup",
        "Status": "Success",
    }


@app.get("/pincode/{pincode}", response_model=PincodeResponse, tags=["pincode"])
def get_pincode_details(pincode: str):
    if not re.fullmatch(r"\d{6}", pincode):
        raise InvalidPincodeException(pincode)

    record = pincodes.get(pincode)
    if record is None:
        raise PincodeNotFoundException(pincode)

    return PincodeResponse(data=Pincode(**record))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
