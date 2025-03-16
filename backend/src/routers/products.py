from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List, Dict, Literal
from pydantic import BaseModel, Field
from utils.uuid import simple_uuid
from utils.exceptions import RoshidError
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime
from routers.stores import get_stores_dal, StoresDAL
import json


## Order Form

class FormElement(BaseModel):
    type: Literal["text", "phone", "long_text", "select", "checkbox"]
    label: str
    required: bool


class OrderForm(BaseModel):
    elements: List[FormElement] = [
        FormElement(type="text", label="Full Name", required=True),
        FormElement(type="phone", label="Phone Number", required=True),
        FormElement(type="long_text", label="Address", required=True),
        FormElement(type="text", label="Delivery Instructions", required=False),
    ]

    def add_element(self, element: FormElement):
        self.elements.append(element)
    
    def remove_element(self, element: FormElement):
        self.elements.remove(element)

# Products


class ProductContent(BaseModel):
    name: str
    description: str 
    images: List[str]

class Product(BaseModel):
    availability: bool
    price: float
    content: ProductContent
    delivery_method: str
    order_form: OrderForm = OrderForm()

class CreateProductRequest(BaseModel):
    availability: bool
    price: float
    content: ProductContent
    delivery_method: str


class Stock(BaseModel):
    product_id: str
    quantity: int
    minimum_quantity: int
    last_updated: float

class CreateStockRequest(BaseModel):
    quantity: int
    minimum_quantity: int



from typing import Literal

class InventoryTransaction(BaseModel):
    product_id: str
    type: Literal["IN", "OUT"]
    quantity: int
    created: float
    method: Literal["STOCK_UPDATE", "ORDER"]





class ProductDAL:
    def __init__(
            self,
            product_collection: AsyncIOMotorCollection,
            stock_collection: AsyncIOMotorCollection,
            inventory_collection: AsyncIOMotorCollection
        ):

            self.collection = product_collection
            self.stock_collection = stock_collection
            self.inventory_collection = inventory_collection

    
    async def create_product(
            self, product: CreateProductRequest,
            store_id:str,
            stores_dal: StoresDAL,

        ) -> str:
        product_id = simple_uuid(8)
      
        product_instance = Product(
        
            availability=product.availability,
            price=product.price,
            content=product.content,
            delivery_method=product.delivery_method
        )
        
        product_doc = product_instance.model_dump()
        product_doc["_id"] = product_id
        product_doc["store_id"] = store_id

        try:
            await self.collection.insert_one(product_doc)
            await stores_dal.add_product(store_id, product_id)
            
            return product_id
        except Exception as e:
            raise RoshidError(f"Failed to create product: {str(e)}")
        

    async def get_product(self, product_id: str) -> dict:
        try:
            product = await self.collection.find_one({"_id": product_id})
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            return product
        except Exception as e:
            raise RoshidError(f"Failed to get product: {str(e)}")
        
    async def add_stock(self, product_id: str, stock: CreateStockRequest) -> str:
        # Check if stock already exists
        existing_stock = await self.stock_collection.find_one({"product_id": product_id})
        if existing_stock:
            raise RoshidError("Stock already exists for this product.")

        stock_doc = {
            "product_id": product_id,
            **stock.model_dump(),
            "last_updated": datetime.now().timestamp()
        }
        
        # TODO: find a way to make these 3 operations atomic
        try:
            result = await self.stock_collection.insert_one(stock_doc)
            await self.collection.update_one(
                {"_id": product_id},
                {"$set": {"stock_id": str(result.inserted_id)}}
            )

            transaction = InventoryTransaction(
                product_id=product_id,
                type="IN",
                quantity=stock.quantity,
                created=datetime.now().timestamp(),
                method="STOCK_UPDATE"
            )
            await self.inventory_collection.insert_one(transaction.model_dump())

            return str(result.inserted_id)
        except Exception as e:
            raise RoshidError(f"Failed to add stock: {str(e)}")

    async def get_stock(self, product_id: str) -> dict:
        try:
            stock = await self.stock_collection.find_one({"product_id": product_id})
            if not stock:
                raise HTTPException(status_code=404, detail="Stock not found")
            return stock
        
        except Exception as e:
            raise RoshidError(f"Failed to get stock: {str(e)}")
        
    async def update_stock(self, product_id: str, quantity: int) -> bool:
        current_stock = await self.stock_collection.find_one({"product_id": product_id})
        old_quantity = int(current_stock["quantity"]) 
        try:
            if old_quantity == quantity:
                return False
            else:
                result = await self.stock_collection.update_one(
                    {"product_id": product_id},
                    {"$set": {"quantity": quantity, "last_updated": datetime.now().timestamp()}}
                )

            if old_quantity < quantity:
                transaction_type = "IN"
            else:
                transaction_type = "OUT"
            transaction = InventoryTransaction(
                product_id=product_id,
                type=transaction_type,
                quantity=abs(old_quantity - quantity),
                created=datetime.now().timestamp(),
                method="STOCK_UPDATE"
            )

            await self.inventory_collection.insert_one(transaction.model_dump())
            return result.modified_count > 0
        except Exception as e:
            raise RoshidError(f"Failed to update stock: {str(e)}")
        



router = APIRouter()

def get_products_dal(request: Request):
    return request.app.products_dal


@router.post("/products/create")
async def create_product(
        product: CreateProductRequest,
        store_id: str = Header(...),
        products_dal: ProductDAL = Depends(get_products_dal),
        stores_dal: StoresDAL = Depends(get_stores_dal)
    ):
    product_id = await products_dal.create_product(product, store_id, stores_dal)
    return {"product_id": product_id}



@router.get("/products/all")
async def get_all_products(
    products_dal: ProductDAL = Depends(get_products_dal)
):
    products = []
    async for product in products_dal.collection.find():
        product["_id"] = str(product["_id"])
        products.append(product)
    return products

class GetProductsRequest(BaseModel):
    product_ids: List[str]

@router.post("/products")
async def get_products(
    request: GetProductsRequest,
    products_dal: ProductDAL = Depends(get_products_dal)
):
    products = []
    for product_id in request.product_ids:
        product = await products_dal.get_product(product_id)
        product["_id"] = str(product["_id"])
        products.append(product)
    return products

@router.post("/products/{product_id}/stock/add")
async def add_stock(
        product_id: str,
        stock: CreateStockRequest,
        products_dal: ProductDAL = Depends(get_products_dal)
    ):

    stock_id = await products_dal.add_stock(product_id, stock)
    return {"stock_id": stock_id}

@router.get("/products/{product_id}/stock")
async def get_stock(
        product_id: str,
        products_dal: ProductDAL = Depends(get_products_dal)
    ):
    stock = await products_dal.get_stock(product_id)
    stock["_id"] = str(stock["_id"])
    return stock

@router.put("/products/{product_id}/stock/update")
async def update_stock(
        product_id: str,
        quantity: int,
        products_dal: ProductDAL = Depends(get_products_dal)
    ):
    success = await products_dal.update_stock(product_id, quantity)
    return {"success": success}



