from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.database import SessionLocal, engine

from app.routers import items
from app.routers import ss_upload


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(ss_upload.router)


