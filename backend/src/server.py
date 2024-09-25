from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn

DEBUG = True

app = FastAPI()

mongodb_url = "mongodb://root:rootpassword@mongodb_container:27017/"

client = MongoClient(mongodb_url)

db = client.your_database_name

    
    
def main():
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()