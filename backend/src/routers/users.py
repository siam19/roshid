from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

router = APIRouter()

@router.get("/users/{user_id}/config")
async def get_user_config(user_id: str):
    config = await app.config_dal.get_user_config(user_id)
    return config

@router.put("/users/{user_id}/config")
async def update_user_config(user_id: str, config_data: dict):
    await app.config_dal.update_user_config(user_id, config_data)
    return {"status": "success"}