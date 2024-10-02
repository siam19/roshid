from typing import List, Any, Literal, Optional, get_args
from typing import Optional
from bson import ObjectId
from utils.uuid import simple_uuid
import json
from collections import OrderedDict
from pydantic import BaseModel, ValidationError
from utils.exceptions import RoshidAttributeError

from pydantic import BaseModel, Field
from typing import List, Optional, Any
from uuid import uuid4

class ProductVariant(BaseModel):
    name: str
    description: Optional[str] = None
    possible_values: List[Any] = Field(default_factory=list)

    def add_possible_value(self, value: Any):
        self.possible_values.append(value)
    
    def remove_possible_value(self, value: Any):
        self.possible_values.remove(value)
    
    def __repr__(self) -> str:
        return f"PVariant({self.name}={self.possible_values})"

class Product(BaseModel):

    name: str
    base_price: float
    weight_category: str  # TODO: Change to Literal later
    image: Optional[str] = None
    description: Optional[str] = None
    variants: List[ProductVariant] = Field(default_factory=list)

    def __repr__(self) -> str:
        return f"Product(name={self.name}, price={self.base_price}, description={self.description}, variants={self.variants})"

    def create_variant(self, name: str, possible_values: List[Any], description: Optional[str] = None) -> ProductVariant:
        variant = ProductVariant(name=name, description=description, possible_values=possible_values)
        self.variants.append(variant)
        return variant
    
    def color_variant(self, colors: List[str]):
        return self.create_variant("Color", colors, "The color of the product")
    
    def size_variant(self, sizes: List[str]):
        return self.create_variant("Size", sizes, "The size of the product")

    def add_variant(self, variant: ProductVariant):
        self.variants.append(variant)

    def get_variants(self) -> List[ProductVariant]:
        return self.variants
    
    @classmethod
    def from_doc(cls, data: dict):
        variants = [ProductVariant(**v) for v in data.get('variants', [])]
        return cls(**{**data, 'variants': variants})
    
    def to_doc(self) -> dict:
        return self.model_dump(by_alias=True)

class OrderTemplate(BaseModel):
    customer_data: dict[str, str]
    product_data: dict[str, Any]

class Order(BaseModel):
    order_id: str
    created: str
    last_updated: str


class Attribute(BaseModel):
    attribute_name: str
    datatype: Literal['string', 'number', 'boolean']  # Restrict to specific values
    description: Optional[str] = None  # Description is optional
    is_required: bool = False

class CustomerConfig:

    '''
    This class represents the data that is to be extracted. It doesnt hold
    any customer data, but instead is used to generate prompts for the LLM to digest. 
    The reasoning behind creating a different class for this is so that users can 
    create and extract arbritary attributes from a screenshot.
    '''
    def __init__(self) -> None:
        self.attributes: set[Attribute] = []
        self.attributes.append(Attribute(attribute_name="name", datatype="string", description="Name of the customer", is_required=True))
        self.attributes.append(Attribute(attribute_name="address", datatype="string", description="The delivery address mentioned by the customer", is_required=True))
        self.attributes.append(Attribute(attribute_name="phone", datatype="string", description="Phone number mentioned by the customer in the format: '01X XXXX XXXX'", is_required=True))
        self.attributes.append(Attribute(attribute_name="instructions", datatype="string", description="Verbatim copy of any delivery instruction given by the customer. Enter N/A if no instructions are provided.", is_required=True))
    
    def generate_description(self) -> str:
        attribute_descriptions = [
            f"{attr.attribute_name} ({attr.datatype}): {attr.description or 'No description provided'}"
            for attr in self.attributes
        ]
        return f"Extract {', '.join(attribute_descriptions)} from the text:"
    
    def add_attribute(self, name:str, datatype: str, description: str):
        '''
        attribute_name: str = Name of the attribute (e.g 'Email', 'Secondary Contact')\n\n
        datatype: str ='string', 'number' or 'boolean'\n\n
        description: str = Description of the attribute for the LLM to accurately locate and extract the attribute
        is_required: bool = true for attributes that are needed to place an order
        '''
        try:
            if name.lower() in [attr.attribute_name.lower() for attr in self.attributes]: # checks if the attribute name already exists
                raise RoshidAttributeError("Attribute name already exists. Choose a different name.")
            else:
                self.attributes.append(Attribute(attribute_name=name, datatype=datatype, description=description))

        except ValidationError as e:
            print("Something went wrong when creating Attrbute.")
            print(e)

    def expected_json(self) -> str:
        """
        Returns a JSON schema that defines the structure of the expected output from the LLM.
        """

        schema = {}
        for attb in self.attributes:
            schema[attb.attribute_name] = f"{attb.description} (type={attb.datatype}, mandatory_to_extract={attb.is_required})"

        return json.dumps(schema)
    
class CustomerData(BaseModel):
    name: str
    phone: str
    address: str
    instructions: str

class DeliveryConfig(BaseModel):
    vendor: str
    api_key: str
    api_secret: str
    config: dict[str, Any]





