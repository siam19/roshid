from typing import List, Any
from typing import Optional
from bson import ObjectId
from utils.uuid import simple_uuid
import json


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
