from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from .base import BaseRouter

router = BaseRouter()

@router.post("/page/create")
@router.dal_handler
async def create_page(page_data: dict, dal):
    page_id = await dal.pages_dal.create_page(page_data)
    return {"page_id": page_id}

@router.put("/page/{page_id}")
@router.dal_handler
async def update_page(page_id: str, page_data: dict, dal):
    await dal.pages_dal.update_page(page_id, page_data)
    return {"status": "success"}

@router.get("/page/{page_id}")
@router.dal_handler
async def get_page(page_id: str, dal):
    page = await dal.pages_dal.get_page_content(page_id)
    return page