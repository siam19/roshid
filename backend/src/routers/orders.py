from fastapi import APIRouter
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime


from classes import Order, CustomerData



router = APIRouter()



# Order endpoints
@router.get("/orders")
async def list_orders(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[Order]:
    return await router.order_dal.list_orders(start_date, end_date, status, limit, offset)
