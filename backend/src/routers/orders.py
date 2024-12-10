from fastapi import APIRouter, Depends, HTTPException, Request
from classes import DeliveryInfo
from typing import List
from classes import CreateOrderRequest, DeliveryInfo
router = APIRouter()

@router.get("/orders")
async def get_all_orders():
    orders = await app.order_dal.get_all_orders()
    return orders

@router.post("/orders/create")
async def create_order(request: Request, delivery_info: DeliveryInfo | None, delivery_service_name: str|None):
    delivery_interface = request.app.delivery_interface

    delivery_interface.authenticate()

    # Partial order creation

    # Send Pickup Request
    consignment_info = delivery_interface.create_pickup_request(delivery_info, delivery_service_name)

    return consignment_info

    # if delivery_service:
    #     result = delivery_service.create_order(delivery_info)
    #     return result
    # else:
    #     return {"error": f"Delivery service '{delivery_service_name}' not found"}
    


    
@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = await app.order_dal.get_order(order_id)
    return order

@router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    await app.order_dal.delete_order(order_id)
    return {"status": "success"}

@router.post("/orders/{order_id}/deliver")
async def deliver_order(order_id: str):
    result = await app.delivery_dal.process_delivery(order_id)
    return result

@router.get("/orders/{order_id}/status")
async def get_order_status(order_id: str):
    status = await app.order_dal.get_order_status(order_id)
    return {"status": status}
