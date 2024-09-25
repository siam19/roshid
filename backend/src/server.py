from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn

DEBUG = True

app = FastAPI()

# MongoDB connection string
mongodb_url = "mongodb://root:rootpassword@mongodb_container:27017/"

# Create a MongoClient
client = MongoClient(mongodb_url)

# Access a database
db = client.your_database_name

# Define a Pydantic model for the document structure
class User(BaseModel):
    name: str
    email: str
    age: int

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(mongodb_url)
    app.database = app.mongodb_client["your_database_name"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.post("/users/", response_model=User)
async def create_user(user: User):
    user_dict = user.dict()
    collection = app.database["users"]
    
    result = collection.insert_one(user_dict)
    
    if result.inserted_id:
        return user
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")

@app.get("/users/")
async def get_users():
    collection = app.database["users"]
    users = list(collection.find({}, {'_id': 0}))  # Exclude _id field
    return users

    
def main():
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()