from pydantic import BaseModel, Field


class Pincode(BaseModel):
    pincode: str = Field(pattern=r"^\d{6}$")
    office_name: str = Field(min_length=1, max_length=200)
    district: str = Field(min_length=1, max_length=100)
    state: str = Field(min_length=1, max_length=100)
    country: str = "India"


class PincodeResponse(BaseModel):
    status: str = "success"
    data: Pincode


class ErrorDetail(BaseModel):
    loc: list[str] = Field(default_factory=list)
    msg: str
    type: str


class ErrorResponse(BaseModel):
    status: str = "error"
    error_code: str
    message: str
    details: list[ErrorDetail] | None = None
