from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from pydantic import BaseModel, ConfigDict
from typing import List, AsyncGenerator,Optional, Any, Union

from utils.uuid import simple_uuid
from utils.exceptions import RoshidError, RoshidAttributeError

from classes import Product, ProductVariant, ProductItem, OrderTemplate, DeliveryConfig, CustomerConfig, CustomerDataModel
from datetime import datetime

from delivery import SteadfastAPI
import os

from fastapi import HTTPException
#DAL stands for Data Access Layer. The DAL is responsible for handling all interactions with the database.


class ProductResponse(Product):
    product_id: Optional[str] 
    



### DEV ###
KOLATOLI_PAGE = {
    "userId": "kolatoli-restaurant-bd23-45xc",
    "title": "Kolatoli Restaurant",
    "blocks": [
        {
            "index": 0,
            "type": "img",
            "content": {
                "url": "https://storage.example.com/kolatoli/logo.png",
                "title": "Kolatoli Restaurant Logo",
                "style": {
                    "type": "4x3",
                    "alignment": "horizontal"
                }
            }
        },
        {
            "index": 1,
            "type": "text",
            "content": {
                "text": "Authentic Bengali Cuisine",
                "style": {
                    "type": "header",
                    "alignment": "center"
                }
            }
        },
        {
            "index": 2,
            "type": "productCollection",
            "content": {
                "products": [
                    "kol_biryani_001",
                    "kol_kebab_002",
                    "kol_curry_003",
                    "kol_dessert_004"
                ],
                "style": {
                    "columns": "double",
                    "type": "card"
                }
            }
        }
    ],
    "pageType": "restaurant",
    "created": "2024-10-26T10:00:00Z",
    "updated": "2024-10-26T10:00:00Z"
}

TECHSTART_PAGE = {
    "userId": "techstart-solutions-45ty-78op",
    "title": "TechStart Solutions",
    "blocks": [
        {
            "index": 0,
            "type": "img",
            "content": {
                "url": "https://storage.example.com/techstart/logo.png",
                "title": "TechStart Solutions Logo",
                "style": {
                    "type": "1x1",
                    "alignment": "horizontal"
                }
            }
        },
        {
            "index": 1,
            "type": "text",
            "content": {
                "text": "Transforming Ideas into Digital Reality",
                "style": {
                    "type": "header",
                    "alignment": "center"
                }
            }
        },
        {
            "index": 2,
            "type": "link",
            "content": {
                "title": "Book a Consultation",
                "linkTo": "https://calendly.com/techstart",
                "style": {
                    "type": "button"
                }
            }
        }
    ],
    "pageType": "technology",
    "created": "2024-10-26T10:00:00Z",
    "updated": "2024-10-26T10:00:00Z"
}

# In-memory storage
pages_db = {
    "kolatoli-restaurant-bd23-45xc": KOLATOLI_PAGE,
    "techstart-solutions-45ty-78op": TECHSTART_PAGE
}


class PagesDAL:
    '''Data Access Layer for the Pages collection'''
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_pages(self, user_id: str) -> dict:
        if user_id not in pages_db:
            raise HTTPException(status_code=404, detail="Page not found")
        return pages_db[user_id]


## DEV ###
# Sample Products Data
products_db = {
    "kol_biryani_001": {
        "productId": "kol_biryani_001",
        "userId": "kolatoli-restaurant-bd23-45xc",
        "name": "Special Kacchi Biryani",
        "price": 350.00,
        "description": "Traditional Dhaka-style kacchi biryani made with premium basmati rice, tender mutton, and our secret blend of spices. Served with raita and salad.",
        "images": [
            "https://storage.example.com/kolatoli/products/biryani_main.jpg",
            "https://storage.example.com/kolatoli/products/biryani_plated.jpg"
        ],
        "created": "2024-10-26T10:00:00Z",
        "updated": "2024-10-26T10:00:00Z"
    },
    "kol_kebab_002": {
        "productId": "kol_kebab_002",
        "userId": "kolatoli-restaurant-bd23-45xc",
        "name": "Galouti Kebab",
        "price": 280.00,
        "description": "Melt-in-your-mouth kebabs made with minced lamb and aromatic spices. Served with mint chutney and roomali roti.",
        "images": [
            "https://storage.example.com/kolatoli/products/kebab_main.jpg",
            "https://storage.example.com/kolatoli/products/kebab_plated.jpg"
        ],
        "created": "2024-10-26T10:00:00Z",
        "updated": "2024-10-26T10:00:00Z"
    },
    "kol_curry_003": {
        "productId": "kol_curry_003",
        "userId": "kolatoli-restaurant-bd23-45xc",
        "name": "Bengali Fish Curry",
        "price": 320.00,
        "description": "Fresh Hilsa fish cooked in a traditional mustard-based curry sauce. Served with steamed rice.",
        "images": [
            "https://storage.example.com/kolatoli/products/curry_main.jpg",
            "https://storage.example.com/kolatoli/products/curry_served.jpg"
        ],
        "created": "2024-10-26T10:00:00Z",
        "updated": "2024-10-26T10:00:00Z"
    },
    "kol_dessert_004": {
        "productId": "kol_dessert_004",
        "userId": "kolatoli-restaurant-bd23-45xc",
        "name": "Roshogolla Platter",
        "price": 150.00,
        "description": "Traditional Bengali sweet made from cottage cheese and sugar syrup. Served chilled with rabri.",
        "images": [
            "https://storage.example.com/kolatoli/products/roshogolla_main.jpg",
            "https://storage.example.com/kolatoli/products/roshogolla_plated.jpg"
        ],
        "created": "2024-10-26T10:00:00Z",
        "updated": "2024-10-26T10:00:00Z"
    }
}


class ProductsDAL:
    '''
    Acts as a Data Access Layer for the Product collection.
    Attach the ProductDAL to the app instance as app.product_dal.
    '''
    def __init__(self, product_collection: AsyncIOMotorCollection):
       self._product_collection = product_collection
    
    async def get_product(self, product_id: str):
        if product_id not in products_db:
            raise HTTPException(status_code=404, detail="Product not found")
        return products_db[product_id]
    
    async def get_user_products(self, user_id: str):
        user_products = [product for product in products_db.values() if product["userId"] == user_id]
        return user_products
    

#     async def list_products(self, session=None)-> AsyncGenerator:
#         #yields a generator that returns Product instances.
#         # `use [i async for i in app.product_dal.list_products()]

#         async for doc in self._product_collection.find({}, session=session):
#             yield Product.from_doc(doc)

#     async def get_product(self, id: str | ObjectId, session=None) -> Product:
#         doc = await self._product_collection.find_one(
#             {"_id": ObjectId(id)},
#             session=session,
#         )
#         return Product.from_doc(doc)
    
#     async def create_product(self, product: Product, session=None) -> str:
#         #product.product_id = simple_uuid(4)
#         response = await self._product_collection.insert_one(
#             product.model_dump(),
#             session=session,
#         )
#         return {"inserted_id": str(response.inserted_id)}
    
#     async def delete_product(self, id: str | ObjectId, session=None) -> bool:
#         response = await self._product_collection.delete_one(
#             {"_id": ObjectId(id)},
#             session=session,
#         )
#         return response.deleted_count == 1
    
    
# class ConfigDAL:
#     def __init__(self, config_collection: AsyncIOMotorCollection):
#         self.collection = config_collection

    
#     async def get_customer_config(self) -> CustomerConfig:
#         config_doc = await self.collection.find_one({"__config__": "CustomerConfig"})
#         return CustomerConfig.from_doc(config_doc)
        
#     async def get_customer_data_model(self, customer_config: CustomerConfig):
#         # Generates a CustomerData model with attributes from customer config
#         return CustomerDataModel.generate_model(customer_config)

    
#     async def update_customer_data_format(self, format: dict[str, Any]):
#         # Update the existing customer data format in the database
#         pass

#     async def get_vendor_config(self, vendor_name: str):
#         # Retrieve the vendor config from the database
#         pass


class OrderDAL:
    def __init__(self, order_collection: AsyncIOMotorCollection):
        self._order_collection = order_collection

    async def list_orders(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, 
                          status: Optional[str] = None, limit: int = 10, offset: int = 0):
        # Retrieve a list of orders with optional filtering and pagination from _order_collection (mongodb)
        query = {}
        if start_date:
            query["created_at"] = {"$gte": start_date}
        if end_date:
            if "created_at" in query:
                query["created_at"]["$lte"] = end_date
            else:
                query["created_at"] = {"$lte": end_date}
        if status:
            query["status"] = status

        cursor = self._order_collection.find(query).skip(offset).limit(limit)
        orders = []
        async for doc in cursor:
            orders.append(OrderTemplate(**doc))
        return orders

    async def get_order(self, order_id: str):
        order = await self._order_collection.find_one({"roshid_id": order_id})
        if not order:
            return {"error": "Order not found"}
        else:
            return OrderTemplate(**order)

    async def create_order(self, customer_data: dict[str, Any], cart_items: List[ProductItem], delivery_method: Optional[Union[dict, str]]):
        roshid_id = simple_uuid(8)
        order = OrderTemplate(
            roshid_id=roshid_id,
            status="pending",
            customer_data=customer_data,
            cart_items=cart_items,
            delivery_method = delivery_method,
            base_price= sum([p.total() for p in cart_items])
            )
        
        print(order)
        response = await self._order_collection.insert_one(order.model_dump())
        
        return {"inserted_id": str(response.inserted_id), **order.model_dump()}

    
    # async def update_order(self, order_id: str, order: Order) -> Optional[Order]:
    #     # Update an existing order
    #     pass

    async def delete_order(self, order_id: str) -> bool:
        response = await self._order_collection.delete_one({"roshid_id": order_id})
        return response.deleted_count == 1

    # async def get_invoice(self, order_id: str) -> Optional[dict]:
    #     # Retrieve the invoice for a specific order
    #     pass

    # async def get_order_status(self, order_id: str) -> Optional[str]:
    #     # Retrieve the status of a specific order
    #     pass

class DeliveryDAL:
    """
    Acts as a Data Access Layer for the Delivery collection.
    Attach the DeliveryDAL to the app instance as app.delivery_dal.

    """
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    # async def list_delivery_apis(self) -> List[str]:
    #     # Retrieve a list of all configured delivery APIs
    #     pass

    # async def create_delivery_config(self, vendor: str, config: DeliveryConfig) -> DeliveryConfig:
    #     # Create a new delivery configuration for a specific vendor
    #     pass

    async def create_pickup_request(self, vendor: str, order_template: OrderTemplate) -> dict:
        # Create a pickup request with a specific vendor using the given order template
        """

        Args:
            vendor (str): _description_
            order_template (OrderTemplate): _description_

        Returns:
            dict: _description_
        """
        customer_data = order_template.customer_data
        base_price = order_template.base_price

        if vendor.lower() =='steadfast':
            api_key = os.getenv("STEADFAST_API_KEY")
            api_secret = os.getenv("STEADFAST_SECRET_KEY")
            client = SteadfastAPI(api_key, api_secret)
        
        response = client.create_order(
            invoice=order_template.roshid_id,
            recipient_name=customer_data["name"],
            recipient_phone=customer_data["phone"],
            recipient_address=customer_data["address"], 
            cod_amount=order_template.base_price + 60,
            note=' '
        )
        
        return response

    # async def cancel_pickup_request(self, vendor: str, order_id: str) -> bool:
    #     # Cancel a pickup request for a specific vendor and order
    #     pass

    async def get_delivery_balance(self, vendor: str) -> float:
        # Retrieve the current balance for a specific delivery vendor
        pass