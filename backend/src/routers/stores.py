from fastapi import APIRouter, Depends, HTTPException, Request, Header
from classes import DeliveryInfo
from typing import List
from classes import CreateOrderRequest, DeliveryInfo
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from utils.custom_uuid import CustomUUID
from utils.exceptions import RoshidError
from datetime import datetime

router = APIRouter()

class Store(BaseModel):
    id: str
    store_name: str
    phone: str
    delivery_methods: List[str]
    products: List[str]
    pages: List[str]
    user_id: str
    created_at: float

class CreateStoreRequest(BaseModel):
    store_name: str
    phone: str
    delivery_methods: List[str]

def get_stores_dal(request: Request):
    return request.app.stores_dal

class StoresDAL:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_store(self, user_id: str, store: CreateStoreRequest) -> str:
        store_id = str(CustomUUID(5, store.store_name))
        store_data = store.model_dump()
        store_data["_id"] = store_id
        store_data["created_at"] = datetime.now().timestamp()
        store_data["user_id"] = user_id
        store_data["products"] = []
        store_data["pages"] = []

        try:
            await self.collection.insert_one(store_data)
            return store_id
        except Exception as e:
            raise RoshidError(f"Failed to create store: {str(e)}")

    async def get_store(self, store_id: str) -> dict:
        store = await self.collection.find_one({"_id": store_id})
        return store

    async def add_page(self, store_id: str, page_id: str):
        '''Add page to store document'''
        await self.collection.update_one({"_id": store_id}, {"$push": {"pages": page_id}})
        return {"status": "success"}

    async def add_product(self, store_id: str, product_id: str):
        '''Add product to store document'''
        await self.collection.update_one({"_id": store_id}, {"$push": {"products": product_id}})
        return {"status": "success"}
    

@router.post("/store/create")
async def create_store(
        store: CreateStoreRequest,
        user_id: str = Header(...),
        stores_dal: StoresDAL = Depends(get_stores_dal)
    ):
    store_id = await stores_dal.create_store(user_id, store)
    return {"store_id": store_id}

@router.get("/store/{store_id}")
async def get_store(
        store_id: str,
        stores_dal: StoresDAL = Depends(get_stores_dal)
    ):
    store = await stores_dal.get_store(store_id)
    return store