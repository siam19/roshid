from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel

from dal import ProductDAL
from classes import Product, ProductVariant

DEBUG = True


MONGODB_URI = "mongodb://root:rootpassword@mongodb_container:27017/"
COLLECTION_NAME = "products"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client.get_database("roshid")

    # Ensure the database is available:
    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")

    product_list = database.get_collection(COLLECTION_NAME)
    app.product_dal = ProductDAL(product_list)

    # Yield back to FastAPI Application:
    yield

    # Shutdown:
    client.close()

app = FastAPI(lifespan=lifespan, debug=DEBUG)
    

@app.get("/products")
async def list_products() -> list[Product]:
    return [i async for i in app.product_dal.list_products()]

@app.post("/products/create")
async def create_product(product: Product):
    return await app.product_dal.create_product(product)

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    return await app.product_dal.delete_product(product_id)

def main():
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()