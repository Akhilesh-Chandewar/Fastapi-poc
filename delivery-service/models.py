from enum import Enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Status(str, Enum):
    PROCESSING = "processing"
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    delivery_address: str
    items: str
    status: Status = Field(default=Status.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class OrderCreate(SQLModel):
    customer_name: str
    delivery_address: str
    items: str

class OrderUpdate(SQLModel):
    status: Optional[Status] = None
    customer_name: Optional[str] = None
    delivery_address: Optional[str] = None
    items: Optional[str] = None

class OrderRead(SQLModel):
    id: int
    customer_name: str
    delivery_address: str
    items: str
    status: Status
    created_at: datetime
    updated_at: datetime

