from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/products", response_model=list[schemas.Product])
def get_all_products(skip=0, limit=0, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip, limit)
    print(products)
    return products


@app.post("/prodcuts", response_model=schemas.Product)
def create_product(product_name:str, price:float, details={}, db: Session = Depends(get_db)):
    db_product = crud.create_product(db, product_name, price, details)
    return db_product
