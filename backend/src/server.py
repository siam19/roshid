from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import os
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Depends
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from bson import ObjectId

from dal import PagesDAL, ProductsDAL
from classes import Product, ProductVariant, ProductItem, OrderTemplate, DeliveryConfig, CustomerDataModel, CustomerConfig, CreateOrderRequest
import asyncio

DEBUG = True

# Get MONGODB_URI from environment variable
MONGODB_URI = os.environ.get("MONGODB_URI")

# Global variable to hold the CustomerData model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client.get_database("roshid")

    # Ensure the database is available:
    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")

    product_list = database.get_collection("products")
    order_list = database.get_collection("orders")
    delivery_list = database.get_collection("delivery")
    config_list = database.get_collection("roshid_configs")

    app.pages_dal = PagesDAL(database.get_collection("pages"))

    app.product_dal = ProductsDAL(product_list)
    # app.order_dal = OrderDAL(order_list)
    # app.delivery_dal = DeliveryDAL(delivery_list)

    # app.config_dal = ConfigDAL(config_list)
    # app.customer_config = await app.config_dal.get_customer_config()

    # Yield back to FastAPI Application:
    yield

    # Shutdown:
    client.close()

app = FastAPI(lifespan=lifespan, debug=DEBUG, root_path="/api/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Generates CustomerData Pydantic model from the config

@app.get("/test")
async def test():
    # return [os.environ.get("STEADFAST_API_KEY"), os.environ.get("STEADFAST_SECRET_KEY")]
    return [{"name": "abir"},{"name": "tanvir"}]

async def initialize_customer_data_model():
    customer_config = await app.config_dal.get_customer_config()
    CustomerData = CustomerDataModel.generate_model(customer_config)
    return CustomerData



# # Order endpoints
# @app.get("/orders")
# async def list_orders(
#     start_date: Optional[datetime] = None,
#     end_date: Optional[datetime] = None,
#     status: Optional[str] = None,
#     limit: int = 10,
#     offset: int = 0
# ) -> List[OrderTemplate]:
#     return await app.order_dal.list_orders(start_date, end_date, status, limit, offset)

# # order statuses for steadfast: pending, delivered_approval_pending, partial_delivered_approval_pending, cancelled_approval_pending
# # unknown_approval_pending, delivered, partial_delivered, cancelled, hold, in_review, unknown

# @app.get("/orders/{order_id}")
# async def get_order(order_id: str):
#     order = await app.order_dal.get_order(order_id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order


# @app.post("/orders/create")
# async def create_order(order_request: CreateOrderRequest):
    
#     return await app.order_dal.create_order(
#         order_request.customer_data, 
#         order_request.cart_items, 
#         order_request.delivery_method
#     )


# @app.put("/orders/{order_id}")
# async def update_order(order_id: str, order: OrderTemplate):
#     updated_order = await app.order_dal.update_order(order_id, order)
#     if not updated_order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return updated_order

# @app.delete("/orders/{order_id}")
# async def delete_order(order_id: str):
#     deleted = await app.order_dal.delete_order(order_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return {"message": "Order deleted successfully"}

# @app.post("/order/delete/{order_id}")
# async def delete_order(order_id: str):
#     deleted = await app.order_dal.delete_order(order_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return {"message": "Order deleted successfully"}

# @app.get("/orders/{order_id}/invoice")
# async def get_invoice(order_id: str):
#     invoice = await app.order_dal.get_invoice(order_id)
#     if not invoice:
#         raise HTTPException(status_code=404, detail="Invoice not found")
#     return invoice

# @app.get("/orders/{order_id}/status")
# async def get_order_status(order_id: str):
#     status = await app.order_dal.get_order_status(order_id)
#     if not status:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return {"status": status}




# # Product endpoints
# @app.get("/products")
# async def get_all_products() -> List[Product]:
#     return [
#         {"name": "Black Tshirt",
#          "base_price": 650,
#          "weight_category": "parcel-1kg"
#         },
#         {"name": "Grey Pant (Jeans)",
#          "base_price": 1450,
#          "weight_category": "parcel-1kg"
#         },
#         {"name": "Cargo Pant",
#          "base_price": 1750,
#          "weight_category": "parcel-1kg"
#         },
        

#     ]
#     # return await app.product_dal.list_products()

# @app.get("/products/{product_id}")
# async def get_product(product_id: str) -> Product:
#     product = await app.product_dal.get_product(product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

# @app.get("/products/batch")
# async def get_products_batch(product_ids: List[str] = Query(...)) -> List[Product]:
#     products = await app.product_dal.get_products_batch(product_ids)
#     return products

# @app.delete("/products/{product_id}")
# async def delete_product(product_id: str):
#     deleted = await app.product_dal.delete_product(product_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"message": "Product deleted successfully"}

# @app.post("/products/create")
# async def create_product(product: Product) -> Product:
#     return await app.product_dal.create_product(product)

# @app.put("/products/{product_id}")
# async def update_product(product_id: str, product: Product) -> Product:
#     updated_product = await app.product_dal.update_product(product_id, product)
#     if not updated_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return updated_product

# @app.post("/products/{product_id}/image")
# async def add_product_image(product_id: str, image: UploadFile = File(...)):
#     success = await app.product_dal.add_product_image(product_id, image)
#     if not success:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"message": "Image added successfully"}

# @app.get("/products/{product_id}/image")
# async def get_product_image(product_id: str):
#     image_path = await app.product_dal.get_product_image_path(product_id)
#     if not image_path:
#         raise HTTPException(status_code=404, detail="Product image not found")
#     return FileResponse(image_path)




@app.get("/users")
async def get_users():
    return {
        "total": 2,
        "users": [

            {   "userId": "kolatoli-restaurant-bd23-45xc",
                "pageUrl": "/kolatoli",
                "businessName": "Kolatoli",
                "phone": "+8801788592045",
                "address": "123 Business Avenue, Suite 100, Farmgate, Dhaka 1215",
                "settings": {
                    "theme": {
                        "name": "modern-dark",
                        "font": "Roboto"
                    },
                    "customerConfig": {
                        "extractionKeys": [
                            {
                                "valueTitle": "Invoice Number",
                                "valueDescription": "Unique identifier for invoice tracking"
                            }
                        ]
                    },
                    "deliveryConfig": [
                        {
                            "name": "steadfast",
                            "credentials": {
                                "apiKey": "sf_prod_key_123"
                            }
                        }
                    ]
                }
            },
            {   "userId": "techstart-solutions-45ty-78op",
                "pageUrl": "/techstart",
                "businessName": "TechStart Solutions",
                "phone": "+1-555-0456",
                "address": "456 Innovation Drive, Gulshan-2, Dhaka",
                "settings": {
                    "theme": {
                        "name": "light-minimal",
                        "font": "Inter"
                    },
                    "customerConfig": {
                        "extractionKeys": [
                            {
                                "valueTitle": "Client ID",
                                "valueDescription": "Internal client reference number"
                            }
                        ]
                    },
                    "deliveryConfig": [
                        {
                            "name": "steadfast",
                            "credentials": {
                                "apiKey": "sf_prod_key_456",
                                "region": "us-west"
                            }
                        },
                        {
                            "name": "express-courier",
                            "credentials": {
                                "username": "techstart",
                                "apiToken": "ec_789xyz"
                            }
                        }
                    ]
                }
            }
        ]
    }





@app.get("/pages/{user_id}")
async def get_page(user_id: str):
    pages = await app.pages_dal.get_pages(user_id)
    return pages

@app.get("/products/{product_id}")
async def get_product(product_id:str):
    res = await app.product_dal.get_product(product_id)
    return res


@app.get("/products/user/{user_id}")
async def get_user_product(user_id:str):
    res = await app.product_dal.get_user_products(user_id)
    print(res)
    return res


# from llm import LLM, get_text
# import json
# from typing import Annotated

# # Screenshot processing endpoint
# @app.post("/llm/extract/customer_data")
# async def extract_customer_data(file: Annotated[bytes, File()]):
#     customer_config = app.customer_config
#     llm = LLM("groq")
#     ocr_text = get_text(file)
#     customer_data = llm.extract_customer_data(ocr_text, customer_config)
#     try:
#         return json.loads(customer_data)
#     except Exception as e:
#         return {"error": str(e)}








def main():
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=4000, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()