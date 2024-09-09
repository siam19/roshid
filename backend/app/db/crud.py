from sqlalchemy.orm import Session

from . import models, schemas
from app.utils.uuid import simple_uuid


def get_products(db: Session, skip: int = 0, limit: int = 100):
    #query = db.query(models.Product).offset(skip).limit(limit)
    #skip and limit isnt quite working so temporarily disabling it 
    query = db.query(models.Product)
    results = query.all()
    print(f"Query: {query}")
    print(f"Results: {results}")
    return results


def create_product(db: Session, name:str, price:float, details):
    db_product = models.Product(id=simple_uuid(4) ,name=name, price=price, details=details)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product