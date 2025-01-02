from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from plugins.delivery_api import DeliveryInterface, DeliveryInfo
router = APIRouter()

@router.post("/delivery/{service_name}/create")
async def create_pickup_request(service_name: str, delivery_info: DeliveryInfo):
    delivery = DeliveryInterface()
    delivery.authenticate()
    
    #TODO implement error handilgn
    delivery.create_pickup_request(delivery_info, service_name)

    return delivery_info

