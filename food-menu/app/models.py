from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    category: str = Field(min_length=1, max_length=50)
    price: float = Field(ge=0)
    is_available: bool = True


class MenuResponse(BaseModel):
    status: str = "success"
    count: int
    menu_items: list[MenuItem]


class ErrorDetail(BaseModel):
    loc: list[str] = Field(default_factory=list)
    msg: str
    type: str


class ErrorResponse(BaseModel):
    status: str = "error"
    error_code: str
    message: str
    details: list[ErrorDetail] | None = None
