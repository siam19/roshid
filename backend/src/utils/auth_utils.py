from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from typing import Optional
import re

SECRET_KEY = "your-secret-key-here"  # Move to environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

class UserRegistration(BaseModel):
    name: str # Constrain name length
    phone: str
    email: str

    @validator('phone')
    def validate_phone(cls, v):
        # Remove any spaces or dashes
        phone = re.sub(r'[\s-]', '', v)
        if not phone.isdigit() or len(phone) != 11:
            raise ValueError('Phone number must be 11 digits')
        return phone

class UserResponse(BaseModel):
    name: str
    phone: str
    email: str
    id: str

def create_tokens(user_data: dict):
    """Create access and refresh tokens for the user"""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_token(
        data={"sub": str(user_data["id"]), "type": "access"},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_token(
        data={"sub": str(user_data["id"]), "type": "refresh"},
        expires_delta=refresh_token_expires
    )
    
    return access_token, refresh_token

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str, token_type: str = "access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type_from_payload: str = payload.get("type")
        
        if user_id is None or token_type_from_payload != token_type:
            return None
            
        return user_id
    except JWTError:
        return None
