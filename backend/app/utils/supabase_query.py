import httpx
from app.config import SUPABASE_URL
from app.exceptions.exceptions import AuthError
from app.utils.logger import logger

async def supabase_query(
    table: str,
    filters: dict,
    select: str = "*",
    headers: dict = None
) -> list[dict]:
    """
    Executes a GET request to Supabase REST API with filters.
    Example: supabase_query("user_roles", {"user_id": "eq.abc", "is_deleted": "eq.false"}, "role_id", headers)
    """
    try:
        filter_query = "&".join([f"{key}={value}" for key, value in filters.items()])
        url = f"{SUPABASE_URL}/rest/v1/{table}?{filter_query}&select={select}"
        logger.debug(f"Executing Supabase query: {url}")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            result = response.json()
            logger.debug(result)

            if response.status_code >= 400:
                error_msg = result.get("message") or response.text
                logger.error(f"Supabase query failed: {error_msg}")
                raise AuthError(f"Query failed: {error_msg}", status_code=response.status_code)

            return result
    
    except AuthError as ae:
        # Let AuthError pass through with its original message and status
        raise ae
    except Exception as e:
        logger.exception("Unexpected error during Supabase query")
        raise AuthError("Unexpected error during query", status_code=500)