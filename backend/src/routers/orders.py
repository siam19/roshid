from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Literal
from datetime import datetime
from utils.uuid import simple_uuid
from utils.exceptions import RoshidError
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from routers.stores import get_stores_dal, StoresDAL
from routers.products import ProductDAL, get_products_dal, OrderForm


router = APIRouter()




class Order(BaseModel):
    form: OrderForm
    user_id: str
    store_id: str
    status: Literal["PENDING", "CONFIRMED", "ON ROUTE", "DELIVERED"]
    created_at: datetime
    updated_at: datetime



class OrdersDAL:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_order(self, order: Order, store_id: str) -> str:
        order_id = simple_uuid(12)
        order_data = order.model_dump()
        order_data["_id"] = order_id
        order_data["store_id"] = store_id
        order_data["created_at"] = datetime.now()
        
        try:
            await self.collection.insert_one(order_data)
            return order_id
        except Exception as e:
            raise RoshidError(f"Failed to create order: {str(e)}")

    async def get_order(self, order_id: str):
        order = await self.collection.find_one({"_id": order_id})
        if not order:
            raise RoshidError("Order not found")
        return order

    async def get_orders(self, store_id: str):
        orders = await self.collection.find({"store_id": store_id}).to_list(100)
        return orders

    async def update_order(self, order_id: str, order: Order):
        order_data = order.model_dump()
        await self.collection.update_one({"_id": order_id}, {"$set": order_data})

    async def delete_order(self, order_id: str):
        await self.collection.delete_one({"_id": order_id})

def get_orders_dal(request: Request):
    return request.app.orders_dal

@router.post("/order/create")
async def create_order(
        order: Order,
        store_id: str,
        orders_dal: OrdersDAL = Depends(get_orders_dal)
    ):
    order_id = await orders_dal.create_order(order, store_id)
    return {"order_id": order_id}