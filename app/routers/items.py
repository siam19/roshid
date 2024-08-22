from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/products")
def get_all_products():
    return [{"name": "all product"} ,{"name": "all product"} ]