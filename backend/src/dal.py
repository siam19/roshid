from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from pydantic import BaseModel, ConfigDict
from typing import List, AsyncGenerator,Optional, Any, Union

from utils.uuid import simple_uuid
from utils.exceptions import RoshidError, RoshidAttributeError

from datetime import datetime
import re

from classes import CreateOrderRequest
import os

from fastapi import HTTPException, Request
#DAL stands for Data Access Layer. The DAL is responsible for handling all interactions with the database.



class OrderDAL:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_all_orders(self) -> List[dict]:
        try:
            cursor = self.collection.find()
            return await cursor.to_list(length=None)
        except Exception as e:
            raise RoshidError(f"Failed to get orders: {str(e)}")

    async def create_order(self, order_data: CreateOrderRequest) -> str:
        order_id = simple_uuid(12)
        order_doc = {
            "_id": order_id,
            **order_data.dict(),
            "status": "pending",
            "created_at": datetime.now(datetime.utc)
        }
        
        try:
            await self.collection.insert_one(order_doc)
            return order_id
        except Exception as e:
            raise RoshidError(f"Failed to create order: {str(e)}")

    async def get_order(self, order_id: str) -> dict:
        try:
            order = await self.collection.find_one({"_id": order_id})
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            return order
        except Exception as e:
            raise RoshidError(f"Failed to get order: {str(e)}")

    async def delete_order(self, order_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": order_id})
            return result.deleted_count > 0
        except Exception as e:
            raise RoshidError(f"Failed to delete order: {str(e)}")

    async def get_order_status(self, order_id: str) -> str:
        try:
            order = await self.collection.find_one(
                {"_id": order_id},
                {"status": 1}
            )
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            return order["status"]
        except Exception as e:
            raise RoshidError(f"Failed to get order status: {str(e)}")


class UsersDAL:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_user_config(self, user_id: str) -> dict:
        try:
            config = await self.collection.find_one({"user_id": user_id})
            if not config:
                raise HTTPException(status_code=404, detail="User config not found")
            return config
        except Exception as e:
            raise RoshidError(f"Failed to get user config: {str(e)}")

    async def update_user_config(self, user_id: str, config_data: dict) -> bool:
        try:
            result = await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {
                    **config_data,
                    "updated_at": datetime.utcnow()
                }},
                upsert=True
            )
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            raise RoshidError(f"Failed to update user config: {str(e)}")
