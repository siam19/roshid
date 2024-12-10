from typing import List, Any, Literal, Optional, get_args
from typing import Optional
from bson import ObjectId
from utils.uuid import simple_uuid
import json
from collections import OrderedDict
from pydantic import BaseModel, ValidationError, create_model
from utils.exceptions import RoshidAttributeError

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Any, Type, Union
from uuid import uuid4



class Block(BaseModel):
    block_type: str  # Could be made into Enum if types are fixed
    block_content: dict

class Page(BaseModel):
    text: str
    images: List[str]
    products: List[str]  # List of product IDs
    blocks: List[Block]

class ProductContent(BaseModel):
    name: str
    description: str 
    images: List[str]

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    availability: bool
    price: float
    content: ProductContent
    delivery_method: str

class CustomerInfo(BaseModel):
    name: str
    phone: str
    address: str

class CreateOrderRequest(BaseModel):
    customer_info: CustomerInfo
    products: List[str]  # List of product IDs
    delivery_method: str

class UserSettings(BaseModel):
    # Flexible structure for config and integration credentials
    
    pass

class User(BaseModel):
    id: str | None = None
    name: str
    phone: str
    address: str
    pages: list[str]
    user_settings: UserSettings



class DeliveryInfo(BaseModel):
    name: str
    phone: str
    address: str
    instructions: Optional[str] = None

