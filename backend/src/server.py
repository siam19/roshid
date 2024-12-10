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
from routers import pages, orders, products, users

from dal import PagesDAL, UsersDAL
from classes import CreateOrderRequest
import logging

from plugins.delivery_api import DeliveryInterface
from plugin_manager import PluginManager

DEBUG = True

# Get MONGODB_URI from environment variable
MONGODB_URI = os.environ.get("MONGODB_URI")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:

    # client = AsyncIOMotorClient("mongodb://localhost:27017")
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client.get_database("roshid")

    # Ensure the database is available:
    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")
    

    product_list = database.get_collection("products")
    users_list = database.get_collection("users")
    app.pages_dal = PagesDAL(database.get_collection("pages"))

    app.users_dal = UsersDAL(users_list)
    
    app.delivery_interface = DeliveryInterface()


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


# Include routers
app.include_router(pages.router, tags=["pages"])
app.include_router(orders.router, tags=["orders"])
app.include_router(products.router, tags=["products"])
app.include_router(users.router, tags=["users"])






def main():
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=4000, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()