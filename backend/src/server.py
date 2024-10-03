from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
from fastapi import FastAPI, HTTPException, Query, File, UploadFile
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

from dal import ProductDAL, OrderDAL, DeliveryDAL, ConfigDAL
from classes import Product, ProductVariant, Order, OrderTemplate, DeliveryConfig, CustomerDataModel, CustomerConfig
import asyncio

DEBUG = True

MONGODB_URI = "mongodb://root:rootpassword@mongodb_container:27017/"

# Global variable to hold the CustomerData model

CustomerData = None

async def initialize_customer_data():
    global CustomerData
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client.get_database("roshid")

    config_list = database.get_collection("roshid_configs")
    config_dal = ConfigDAL(config_list)

    customer_config = await config_dal.get_customer_config()
    CustomerData = CustomerDataModel.generate_model(customer_config)

    client.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    await initialize_customer_data()

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

    app.product_dal = ProductDAL(product_list)
    app.order_dal = OrderDAL(order_list)
    app.delivery_dal = DeliveryDAL(delivery_list)

    app.config_dal = ConfigDAL(config_list)
    app.customer_config = await app.config_dal.get_customer_config()

    # Yield back to FastAPI Application:
    yield

    # Shutdown:
    client.close()

app = FastAPI(lifespan=lifespan, debug=DEBUG)
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
    return app.customer_config.to_doc()



# Order endpoints
@app.get("/orders")
async def list_orders(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[Order]:
    return await app.order_dal.list_orders(start_date, end_date, status, limit, offset)

# order statuses for steadfast: pending, delivered_approval_pending, partial_delivered_approval_pending, cancelled_approval_pending
# unknown_approval_pending, delivered, partial_delivered, cancelled, hold, in_review, unknown

@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> Order:
    order = await app.order_dal.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders/create")
async def create_order(customer_data: List[dict[str, Any]], products: List[str]):
    #return await app.order_dal.create_order(customer_data, products)
    pass

@app.put("/orders/{order_id}")
async def update_order(order_id: str, order: Order):
    updated_order = await app.order_dal.update_order(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    deleted = await app.order_dal.delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@app.get("/orders/{order_id}/invoice")
async def get_invoice(order_id: str):
    invoice = await app.order_dal.get_invoice(order_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@app.get("/orders/{order_id}/status")
async def get_order_status(order_id: str):
    status = await app.order_dal.get_order_status(order_id)
    if not status:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": status}




# Product endpoints
@app.get("/products")
async def get_all_products() -> List[Product]:
    return await app.product_dal.get_all_products()

@app.get("/products/{product_id}")
async def get_product(product_id: str) -> Product:
    product = await app.product_dal.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/batch")
async def get_products_batch(product_ids: List[str] = Query(...)) -> List[Product]:
    products = await app.product_dal.get_products_batch(product_ids)
    return products

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    deleted = await app.product_dal.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.post("/products/create")
async def create_product(product: Product) -> Product:
    return await app.product_dal.create_product(product)

@app.put("/products/{product_id}")
async def update_product(product_id: str, product: Product) -> Product:
    updated_product = await app.product_dal.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.post("/products/{product_id}/image")
async def add_product_image(product_id: str, image: UploadFile = File(...)):
    success = await app.product_dal.add_product_image(product_id, image)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Image added successfully"}

@app.get("/products/{product_id}/image")
async def get_product_image(product_id: str):
    image_path = await app.product_dal.get_product_image_path(product_id)
    if not image_path:
        raise HTTPException(status_code=404, detail="Product image not found")
    return FileResponse(image_path)



# Delivery API endpoints
@app.get("/delivery")
async def list_delivery_apis():
    return await app.delivery_dal.list_delivery_apis()

@app.post("/delivery/add/{vendor}")
async def create_delivery_config(vendor: str, config: DeliveryConfig):
    return await app.delivery_dal.create_delivery_config(vendor, config)

@app.post("/delivery/{vendor}/create")
async def create_pickup_request(vendor: str, order_template: OrderTemplate):
    return await app.delivery_dal.create_pickup_request(vendor, order_template)


@app.delete("/delivery/{vendor}/{order_id}")
async def cancel_pickup_request(vendor: str, order_id: str):
    cancelled = await app.delivery_dal.cancel_pickup_request(vendor, order_id)
    if not cancelled:
        raise HTTPException(status_code=404, detail="Pickup request not found")
    return {"message": "Pickup request cancelled successfully"}

@app.get("/delivery/{vendor}/get_balance")
async def get_delivery_balance(vendor: str):
    balance = await app.delivery_dal.get_delivery_balance(vendor)
    if balance is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"balance": balance}







# Screenshot processing endpoint
@app.post("/llm/extract/customer_data")
async def extract_customer_data(file: UploadFile = File(...)):
    # For now,return a placeholder response
    return {"message": "Customer data extraction not implemented yet"}







# Data Visualization endpoints (placeholders)
@app.get("/stats/orders")
async def get_orders_for_visualization():
    # Placeholder for visualization logic
    return {"message": "Orders visualization data endpoint"}

@app.get("/stats/earnings/")
async def get_earnings_data():
    # Placeholder for earnings data logic
    return {"message": "Earnings data endpoint"}

@app.get("/stats/sheet/orders")
async def get_orders_sheet():
    # Placeholder for generating CSV
    return {"message": "Orders sheet data endpoint"}








# Config endpoints
class CustomerDataFormat(BaseModel):
    format: Dict[str, Any]

@app.get("/configs/customer_data_format")
async def get_customer_data_format():
    format = app.customer_config.to_doc()
    if not format:
        raise HTTPException(status_code=404, detail="Customer data format not found")
    return format

@app.post("/configs/customer_data_format")
async def create_customer_data_format(format: CustomerDataFormat):
    created_format = await app.config.create_customer_data_format(format.format)
    return created_format

@app.put("/configs/customer_data_format")
async def update_customer_data_format(format: CustomerDataFormat):
    updated_format = await app.config.update_customer_data_format(format.format)
    if not updated_format:
        raise HTTPException(status_code=404, detail="Customer data format not found")
    return updated_format

@app.get("/configs/vendor/{vendor_name}")
async def get_vendor_config(vendor_name: str):
    config = await app.config.get_vendor_config(vendor_name)
    if not config:
        raise HTTPException(status_code=404, detail="Vendor config not found")
    return config

def main():
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()