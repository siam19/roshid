from fastapi import APIRouter, Depends, HTTPException, Request
from classes import DeliveryInfo
from typing import List
from classes import CreateOrderRequest, DeliveryInfo
from pydantic import BaseModel



router = APIRouter()

class Store(BaseModel):
    id: str
    store_name: str
    phone: str
    delivery_methods: List[str]
    products: List[str]
    pages: List[str]
    user_id: str

class CreateStoreRequest(BaseModel):
    store_name: str
    phone: str
    delivery_methods: List[str]
    user_id: str

def get_pages_dal(request: Request):
    return request.app.stores_dal


@router.post("/store/create")
async def create_store(
        store: CreateStoreRequest,
        request: Request
    ):
    store_id = request.app.store_dal.create_store(store)
    return {"store_id": store_id}
