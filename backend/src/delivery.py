from abc import ABC, abstractmethod
from dal import ConfigDAL
import json

class DeliveryAPI(ABC):
    @abstractmethod
    def create_order(self):
        pass
    
    @abstractmethod
    def create_bulk_order(self):
        pass
    
    @abstractmethod
    def get_delivery_status(self):
        pass



class SteadfastAPI(DeliveryAPI):
    BASE_URL = "https://portal.packzy.com/api/v1"

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.headers = {
            "Api-Key": self.api_key,
            "Secret-Key": self.secret_key,
            "Content-Type": "application/json"
        }
        print("Headers:", json.dumps(self.headers, indent=2))
    def create_order(self, invoice: str, recipient_name: str, recipient_phone: str, 
                     recipient_address: str, cod_amount: str, note: str) -> dict:
        """
        
        Place an order using the Steadfast API.

        
        Args:
            invoice (str): Unique alpha-numeric identifier including hyphens and underscores
            recipient_name (str): Name of the recipient (max 100 characters)
            recipient_phone (str): 11-digit phone number of the recipient
            recipient_address (str): Address of the recipient (max 250 characters)
            cod_amount (str): Cash on delivery amount in BDT (must be >= 0)
            note (str): Delivery instructions or other notes

        Returns:
            dict: The API response as a dictionary
        """
        endpoint = f"{self.BASE_URL}/create_order"
        
        payload = {
            "invoice": invoice,
            "recipient_name": recipient_name,
            "recipient_phone": recipient_phone,
            "recipient_address": recipient_address,
            "cod_amount": cod_amount,
            "note": note
        }

        try:
            with httpx.Client() as client:
                response = client.post(endpoint, json=payload, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except httpx.RequestError as e:
            print(f"An error occurred  while making the request: {e}")
            return None

# Usage example:
if __name__ == "__main__":
    api_key = "dptfojmcrzwuiisyzpf7x3nij4q1wrw7"
    secret_key = "wjpuscff3dyaug7szimfm5qy"
    
    steadfast = SteadfastAPI(api_key, secret_key)
    
    order_result = steadfast.create_order(
        invoice="INV-001",
        recipient_name="Fahmidul Hasan",
        recipient_phone="01785863769",
        recipient_address="123 Main St, Dhaka, Bangladesh",
        cod_amount="1000",
        note="Please deliver during business hours"
    )
    
    if order_result:
        print("Order created successfully:")
        print(order_result)
    else:
        print("Failed to create order")