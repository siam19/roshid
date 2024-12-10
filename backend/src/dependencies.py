from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils.auth_utils import verify_token  # Import from wherever you placed auth_utils
from dal import AuthDAL  # Import your AuthDAL class

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_auth_dal() -> AuthDAL:
    """
    Dependency that provides AuthDAL instance.
    This gets the AuthDAL instance from the app state.
    """
    from server import app  # Import here to avoid circular imports
    return app.auth_dal

# Create a reusable dependency
AuthDep = Annotated[AuthDAL, Depends(get_auth_dal)]

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_dal: AuthDep
):
    """
    Dependency that provides the current authenticated user.
    Uses the JWT token from the Authorization header.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = await verify_token(token)
    if not user_id:
        raise credentials_exception
    
    user = await auth_dal.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
        
    return user

# Create a reusable dependency for the current user
CurrentUser = Annotated[dict, Depends(get_current_user)]