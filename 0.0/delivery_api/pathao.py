import httpx
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

from .base import DeliveryAPI

class PathaoAPIError(Exception):
    """Base exception for PathaoAPI errors."""
    pass

class AuthenticationError(PathaoAPIError):
    """Raised when authentication fails."""
    pass



class Order(BaseModel):
    consignment_id: str
    merchant_order_id: Optional[str]
    order_status: str
    delivery_fee: float

class Store(BaseModel):
    store_id: int
    store_name: str
    store_address: str
    is_active: int
    city_id: int
    zone_id: int
    hub_id: int
    is_default_store: bool
    is_default_return_store: bool

class City(BaseModel):
    city_id: int
    city_name: str

class Zone(BaseModel):
    zone_id: int
    zone_name: str

class Area(BaseModel):
    area_id: int
    area_name: str

class PriceCalculation(BaseModel):
    delivery_fee: float
    total_charge: float
    cod_charge: Optional[float]

class StoreInfo(BaseModel):
    """{
        store name:"<string> // is provided by the merchant and not changeable. Name of the store"
        address:"<string, min:10, max:65> // is provided by the merchant and not changeable"
        contact name:"<string> // is provided by the merchant and not changeable. Contact person of the store need for issue related communication"
        contact phone:"<string> // is provided by the merchant and not changeable"
        secondary contact:"<string> // is provided by the merchant and not changeable"
        recipient city id:"<int> // is provided by merchant and not changeable"
        recipient zone id:"<int> // is provided by merchant and not changeable"
        recipient area id:"<int> // is provided by merchant and not changeable"
        }"""
    
    name: str
    contact_name: str
    contact_number:str
    secondary_contact:str
    address: str = Field(..., min_length=10, max_length=65)
    city_id: int
    zone_id: int
    area_id: int
    
class OrderInput(BaseModel):
    store_id: int
    recipient_name: str
    recipient_phone: str
    recipient_address: str = Field(..., min_length=10)
    recipient_city: int
    recipient_zone: int
    delivery_type: int # 48 for Normal Delivery, 12 for On Demand Delivery
    item_type: int  # 1 for Document, 2 for Parcel
    item_quantity: int
    item_weight: float = Field(..., ge=0.5, le=10.0)
    amount_to_collect: int
    merchant_order_id: Optional[Union[str, int]] = None
    recipient_area: Optional[str] =  None
    special_instruction: Optional[str] = None
    item_description: Optional[str] = None

    @field_validator('delivery_type')
    @classmethod
    def validate_delivery_type(cls, v):
        if v not in (48, 12):
            raise ValueError("delivery_type must be either 48 (Normal) or 12 (On Demand)")
        return v

    @field_validator('item_type')
    @classmethod
    def validate_item_type(cls, v):
        if v not in (1, 2):
            raise ValueError("item_type must be either 1 (Document) or 2 (Parcel)")
        return v
    
class PathaoAPI(DeliveryAPI):
    def __init__(self, client_id: str, client_secret: str, base_url: str = None):
        self.client_id = client_id
        self.client_secret = client_secret         
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.base_url = base_url if base_url is not None else "https://api-hermes.pathao.com"
        self.client = httpx.Client()

    def _get_headers(self) -> Dict[str, str]:
        if not self.access_token:
            raise AuthenticationError("Not authenticated. Call authenticate() first.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def authenticate(self, username: str, password: str) -> None:
        url = f"{self.base_url}/aladdin/api/v1/issue-token"
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": username,
            "password": password,
            "grant_type": "password"
        }
        response = self.client.post(url, json=data)

        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
        else:
            raise AuthenticationError(f"Authentication failed: {response.text}")

    def refresh_auth_token(self) -> None:
        url = f"{self.base_url}/aladdin/api/v1/issue-token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        response = self.client.post(url, json=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
        else:
            raise AuthenticationError(f"Token refresh failed: {response.text}")

    def create_bulk_order(self, orders: List[OrderInput]) -> Dict[str, Any]:
        url = f"{self.base_url}/aladdin/api/v1/orders/bulk"
        
        order_data = [order.model_dump(exclude_unset=True) for order in orders]
        
        payload = {"orders": order_data}
        
        response = self.client.post(url, headers=self._get_headers(), json=payload)
        
        if response.status_code == 202:
            return response.json()
        else:
            raise PathaoAPIError(f"Bulk order creation failed: {response.text}")
    
    def get_delivery_status(self):
        return NotImplemented

    def create_order(self, order_input: OrderInput) -> Order:
        url = f"{self.base_url}/aladdin/api/v1/orders"
        
        order_data = order_input.model_dump(exclude_unset=True)
        #print(order_data)
        response = self.client.post(url, headers=self._get_headers(), json=order_data)
        
        if response.status_code == 200:
            data = response.json()
            return Order(**data['data'])
        else:
            raise PathaoAPIError(f"Order creation failed: {response.text}")

    def get_delivery_stat(self, consignment_id: str) -> Order:
        url = f"{self.base_url}/aladdin/api/v1/orders/{consignment_id}/info"
        response = self.client.get(url, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            return Order(**data['data'])
        else:
            raise PathaoAPIError(f"Failed to get order info: {response.text}")
        
    def get_stores(self) -> List[Store]:
        url = f"{self.base_url}/aladdin/api/v1/stores"
        response = self.client.get(url, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            return [Store(**store) for store in data['data']['data']]
        else:
            raise PathaoAPIError(f"Failed to get stores: {response.text}")
        
    def create_store(self, store_data: StoreInfo) -> Store:
        url = f"{self.base_url}/aladdin/api/v1/stores"
        response = self.client.post(url, headers=self._get_headers(), json=store_data.model_dump(exclude_unset=True))
        if response.status_code == 200:
            data = response.json()
            return Store(**data['data'])
        else:
            raise PathaoAPIError(f"Store creation failed: {response.text}")
    def get_cities(self) -> List[City]:
        url = f"{self.base_url}/aladdin/api/v1/city-list"
        response = self.client.get(url, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            return [City(**city) for city in data['data']['data']]
        else:
            raise PathaoAPIError(f"Failed to get cities: {response.text}")

    def get_zones(self, city_id: int) -> List[Zone]:
        url = f"{self.base_url}/aladdin/api/v1/cities/{city_id}/zone-list"
        response = self.client.get(url, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            return [Zone(**zone) for zone in data['data']['data']]
        else:
            raise PathaoAPIError(f"Failed to get zones: {response.text}")

    def get_areas(self, zone_id: int) -> List[Area]:
        url = f"{self.base_url}/aladdin/api/v1/zones/{zone_id}/area-list"
        response = self.client.get(url, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            return [Area(**area) for area in data['data']['data']]
        else:
            raise PathaoAPIError(f"Failed to get areas: {response.text}")
    def calculate_price(self, price_data: Dict[str, Any]) -> PriceCalculation:
        url = f"{self.base_url}/aladdin/api/v1/merchant/price-plan"
        response = self.client.post(url, headers=self._get_headers(), json=price_data)
        if response.status_code == 200:
            data = response.json()
            return PriceCalculation(**data['data'])
        else:
            raise PathaoAPIError(f"Price calculation failed: {response.text}")