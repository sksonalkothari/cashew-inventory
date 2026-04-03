import jwt
from fastapi import Header
from app.utils.jwt_utils import decode_jwt_token
from app.exceptions.exceptions import AuthError
from app.utils.logger import logger
from app.utils.supabase_query import supabase_query
from app.config import get_user_headers

async def get_current_user(authorization: str = Header(...)):
    logger.debug(authorization)
    if not authorization.startswith("Bearer "):
        raise AuthError("Invalid authorization header", status_code=401)

    token = authorization.split(" ")[1]
    try:
        user_info = decode_jwt_token(token)
        logger.debug(user_info)
        user_id = user_info["sub"]

        headers = get_user_headers(token)

        roles_response = await supabase_query(
            "user_roles",
            {"user_id": f"eq.{user_id}"},
            "role_id,roles(name)",
            headers
        )
        logger.debug(f"Roles: {roles_response}")
        if len(roles_response) == 0:
            logger.error(f"Role fetch failed: {roles_response.error}")
            raise AuthError("Unable to fetch user roles", status_code=403)

        roles = [r["roles"]["name"] for r in roles_response]

        return {
            "headers": headers,
            "id": user_info["sub"],  # Supabase user ID
            "email": user_info.get("email"),
            "roles": roles
        }
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired for user")
        raise AuthError("Session expired. Please log in again.", status_code=401)
    except Exception as e:
        logger.error(f"Token decoding failed: {str(e)}")
        raise AuthError("Invalid or expired token", status_code=401)