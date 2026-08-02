from fastapi import APIRouter, Depends, HTTPException, Query , status
from sqlmodel import Session, select
from ..database import get_session
from ..models import Order , OrderCreate , OrderRead , OrderUpdate, Status
from ..database import get_session

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/", response_model=list[OrderRead])
def read_orders(
    status: Status | None = Query(None, description="Filter orders by status"),
    created_at: str | None = Query(None, description="Filter orders by creation date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=10, description="Maximum number of records to return"),
):
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    if created_at:
        query = query.where(Order.created_at == created_at)
    orders = Session.exec(query.offset(skip).limit(limit)).all()
    return orders