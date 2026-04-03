from fastapi import Depends
from app.dependencies.auth_dependency import get_current_user
from app.exceptions.exceptions import AuthError
from app.utils.logger import logger

def require_roles(allowed_roles: list[str]):
    async def role_checker(user: dict = Depends(get_current_user)):
        user_roles = user.get("roles", [])
        logger.debug(f"roles: {user_roles}")
        if not any(role in allowed_roles for role in user_roles):
            raise AuthError("Access denied: insufficient permissions", status_code=403)
        return user
    return role_checker