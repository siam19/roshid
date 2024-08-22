from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str
    details: object
    
