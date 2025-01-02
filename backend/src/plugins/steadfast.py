import logging
from .delivery_api import DeliveryAPI
from classes import DeliveryInfo

from abc import ABC, abstractmethod
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional

from utils.custom_uuid import CustomUUID


class SteadfastDeliveryInfo(BaseModel):
    invoice: str = Field(..., description="Unique alpha-numeric identifier including hyphens and underscores")
    recipient_name: str = Field(..., max_length=100, description="Name of the recipient")
    recipient_phone: str = Field(..., min_length=11, max_length=11, description="11-digit phone number of recipient") 
    recipient_address: str = Field(..., max_length=250, description="Address of the recipient")
    cod_amount: str = Field(..., description="Cash on delivery amount in BDT (must be >= 0)")
    note: Optional[str] = Field(None, description="Delivery instructions or other notes")

class InitParams(BaseModel):
    name: str = "steadfast"
    api_key: str = "STEADFAST_API_KEY" # value will be used to search user config
    secret_key: str = "STEADFAST_SECRET_KEY"


class SteadfastAPI(DeliveryAPI):
    BASE_URL = "https://portal.packzy.com/api/v1"

    def __init__(self, init_params: InitParams):
        self.init_params = init_params

        self.api_key = init_params.api_key
        self.secret_key = init_params.secret_key
        
        # print("Headers:", json.dumps(self.headers, indent=2))

    def create_order(self, delivery_info: DeliveryInfo) -> dict:
        """
        Place an order using the Steadfast API.

        Args:
            delivery_info (DeliveryInfo): Pydantic model containing delivery information

        Returns:
            dict: The API response as a dictionary
        """
        endpoint = f"{self.BASE_URL}/create_order"
        self.headers = {
            "Api-Key": self.api_key,
            "Secret-Key": self.secret_key,
            "Content-Type": "application/json"
        }

        # Transform DeliveryInfo into SteadfastDeliveryInfo
        steadfast_delivery_info = SteadfastDeliveryInfo(
            invoice=CustomUUID(4).uuid_str, # Generate a simple unique invoice ID
            recipient_name=delivery_info.name,
            recipient_phone=delivery_info.phone,
            recipient_address=delivery_info.address,
            cod_amount="0", # Default to 0 since DeliveryInfo doesn't have this field
            note=delivery_info.instructions
        )
        
        payload = steadfast_delivery_info.model_dump(exclude_none=True)
        logging.info(payload)
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return None

    def create_bulk_order(self):
        return super().create_bulk_order()

    def get_delivery_status(self):
        return super().get_delivery_status()


DeliveryServicePlugin = SteadfastAPI
DeliveryServiceInitParams = InitParams