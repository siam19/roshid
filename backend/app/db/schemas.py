from pydantic import BaseModel

class ProductBase(BaseModel):
    id: str
    name: str
    price: float


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    details: object

