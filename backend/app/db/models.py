from sqlalchemy import Boolean, Column, ForeignKey, Float, String, JSON

from .database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    details = Column(JSON)
