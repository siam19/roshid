from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict

router = APIRouter()

@router.get("/products/{page_id}")
async def get_page_products(page_id: str):
    products = await app.product_dal.get_products_by_page(page_id)
    return products

@router.get("/products/{page_id}/{product_id}")
async def get_product_details(page_id: str, product_id: str):
    product = await app.product_dal.get_product_details(page_id, product_id)
    return product

@router.post("/products/{page_id}/{product_id}/stock")
async def update_product_stock(page_id: str, product_id: str, stock_data: dict):
    await app.product_dal.update_product_stock(page_id, product_id, stock_data)
    return {"status": "success"}