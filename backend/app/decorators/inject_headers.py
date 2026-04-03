from fastapi import Request
from functools import wraps
from app.config import get_user_headers
from app.utils.logger import logger

def inject_headers(func):
    logger.debug("Decorator outside function")
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.debug("Decorator inner function")
        # Extract FastAPI request object from kwargs
        request: Request = kwargs.get("request")
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        logger.debug(f"request: {request}")
        if not request:
            raise ValueError("Request object not found in route")

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise ValueError("Missing or invalid Authorization header")

        access_token = auth_header.split(" ")[1]
        headers = get_user_headers(access_token)

        # Inject token and headers into kwargs
        kwargs["token"] = access_token
        kwargs["headers"] = headers
        return await func(*args, **kwargs)

    return wrapper