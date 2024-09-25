from fastapi import APIRouter, HTTPException, Depends
from ..db import crud, schemas, models
from ..db.database import SessionLocal, engine
from sqlalchemy.orm import Session

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products", response_model=list[schemas.Product])
def get_all_products(skip=0, limit=0, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip, limit)
    print(products)
    return products


@router.post("/products", response_model=schemas.Product)
def create_product(product_name:str, price:float, details={}, db: Session = Depends(get_db)):
    db_product = crud.create_product(db, product_name, price, details)
    return db_product



