from fastapi import APIRouter, Request
from functools import wraps

class BaseRouter(APIRouter):
    """A custom router class that extends FastAPI's APIRouter to provide database access layer (DAL) handling.

    This router automatically injects the DAL instance from the FastAPI app into route handlers.

    Example usage:
        router = BaseRouter()

        @router.post("/page/create") 
        @router.dal_handler
        async def create_page(page_data: dict, dal):
            page_id = await dal.pages_dal.create_page(page_data)
            return {"page_id": page_id}
    """

    def dal_handler(self, func):
        """Decorator that injects the DAL instance into route handlers.
        
        Args:
            func: The route handler function to wrap

        Returns:
            The wrapped function that receives the DAL instance

        The decorator extracts the DAL from the FastAPI app instance and passes it 
        to the route handler as a 'dal' parameter, allowing direct access to data 
        access layer methods.
        """
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            dal = request.app
            return await func(*args, dal=dal, **kwargs)
        return wrapper