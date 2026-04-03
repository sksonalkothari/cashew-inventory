import httpx
from app.utils.timestamp_utils import current_timestamp
from app.utils.supabase_query import supabase_query
from app.config import SUPABASE_URL, HEADERS
from app.exceptions.exceptions import AuthError
from app.utils.logger import logger

async def signup_user(email: str, password: str):
    logger.info(f"Calling Supabase signup for {email}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/auth/v1/signup",
                headers=HEADERS,
                json={"email": email.strip(), "password": password}
            )
            result = response.json()
            logger.debug(result)
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                error_code = result.get("error_code", "unknown_code")
                logger.error(f"Supabase signup failed [{error_code}] for {email}: {error_msg}")
                raise AuthError(f"Signup failed: {error_msg}", status_code=response.status_code)
            return result
    except AuthError as ae:
        # Let AuthError pass through with its original message and status
        raise ae

    except Exception:
        logger.exception(f"Unexpected error during Supabase signup for {email}")
        raise AuthError("Unexpected error during signup", status_code=500)

async def login_user(email: str, password: str):
    logger.info(f"Calling Supabase login for {email}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
                headers=HEADERS,
                json={"email": email, "password": password}
            )
            result = response.json()
            logger.debug(f"Parsed login result: {result}")
            logger.debug(f"Supabase login response status: {response.status_code}")
            logger.debug(f"Supabase login response body: {response.text}")
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                error_code = result.get("error_code", "unknown_code")
                logger.error(f"Supabase login failed [{error_code}] for {email}: {error_msg}")
                raise AuthError(f"Login failed: {error_msg}", status_code=response.status_code)
            return result
    except AuthError as ae:
        # Let AuthError pass through with its original message and status
        raise ae
    except Exception:
        logger.exception(f"Unexpected error during Supabase login for {email}")
        raise AuthError("Unexpected error during login", status_code=500)