from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from pydantic import BaseModel, ConfigDict
from typing import List, AsyncGenerator,Optional, Any

from utils.uuid import simple_uuid
from utils.exceptions import RoshidError, RoshidAttributeError

from classes import Product, ProductVariant, Order, CustomerData, OrderTemplate, DeliveryConfig
from datetime import datetime


#DAL stands for Data Access Layer. The DAL is responsible for handling all interactions with the database.


class ProductResponse(Product):
    product_id: Optional[str] 
    


class ProductDAL:
    '''
    Acts as a Data Access Layer for the Product collection.
    Attach the ProductDAL to the app instance as app.product_dal.
    '''
    def __init__(self, product_collection: AsyncIOMotorCollection):
       self._product_collection = product_collection
    

    async def list_products(self, session=None)-> AsyncGenerator:
        #yields a generator that returns Product instances.
        # `use [i async for i in app.product_dal.list_products()]

        async for doc in self._product_collection.find({}, session=session):
            yield Product.from_doc(doc)

    async def get_product(self, id: str | ObjectId, session=None) -> Product:
        doc = await self._product_collection.find_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return Product.from_doc(doc)
    
    async def create_product(self, product: Product, session=None) -> str:
        #product.product_id = simple_uuid(4)
        response = await self._product_collection.insert_one(
            product.model_dump(),
            session=session,
        )
        return {"inserted_id": str(response.inserted_id)}
    
    async def delete_product(self, id: str | ObjectId, session=None) -> bool:
        response = await self._product_collection.delete_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return response.deleted_count == 1
    
    
class ConfigDAL:
    def __init__(self, collection):
        self.collection = collection

    async def get_customer_data_format(self):
        # Retrieve the customer data format from the database
        pass

    async def create_customer_data_format(self, format: dict[str, Any]):
        # Create a new customer data format in the database
        pass

    async def update_customer_data_format(self, format: dict[str, Any]):
        # Update the existing customer data format in the database
        pass

    async def get_vendor_config(self, vendor_name: str):
        # Retrieve the vendor config from the database
        pass


class OrderDAL:
    def __init__(self, collection):
        self.collection = collection

    async def list_orders(self, start_date: Optional[datetime], end_date: Optional[datetime], 
                          status: Optional[str], limit: int, offset: int) -> List[Order]:
        # Retrieve a list of orders with optional filtering and pagination
        pass

    async def get_order(self, order_id: str) -> Optional[Order]:
        # Retrieve a single order by its ID
        pass

    async def create_order(self, customer_data: CustomerData, products: List[str]) -> Order:
        # Create a new order with the given customer data and products
        pass

    async def update_order(self, order_id: str, order: Order) -> Optional[Order]:
        # Update an existing order
        pass

    async def delete_order(self, order_id: str) -> bool:
        # Delete an order by its ID
        pass

    async def get_invoice(self, order_id: str) -> Optional[dict]:
        # Retrieve the invoice for a specific order
        pass

    async def get_order_status(self, order_id: str) -> Optional[str]:
        # Retrieve the status of a specific order
        pass

class DeliveryDAL:
    def __init__(self, collection):
        self.collection = collection

    async def list_delivery_apis(self) -> List[str]:
        # Retrieve a list of all configured delivery APIs
        pass

    async def create_delivery_config(self, vendor: str, config: DeliveryConfig) -> DeliveryConfig:
        # Create a new delivery configuration for a specific vendor
        pass

    async def create_pickup_request(self, vendor: str, order_template: OrderTemplate) -> dict:
        # Create a pickup request with a specific vendor using the given order template
        pass

    async def cancel_pickup_request(self, vendor: str, order_id: str) -> bool:
        # Cancel a pickup request for a specific vendor and order
        pass

    async def get_delivery_balance(self, vendor: str) -> float:
        # Retrieve the current balance for a specific delivery vendor
        pass