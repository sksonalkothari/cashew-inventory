import httpx
from app.utils.timestamp_utils import current_timestamp
from app.utils.supabase_query import supabase_query
from app.config import SUPABASE_URL, HEADERS
from app.exceptions.exceptions import UserError
from app.utils.logger import logger

TABLE = "users"

async def insert_user_metadata(user_data: dict):
    email = user_data.get("email", "unknown")
    logger.info(f"Inserting metadata for {email}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=HEADERS,
                json=[{**user_data, "is_deleted": False}]
            )
            if response.status_code >= 400:
                result = response.json()
                error_msg = result.get("msg") or response.text
                error_code = result.get("error_code", "unknown_code")
                logger.error(f"Metadata insert failed [{error_code}] for {email}: {error_msg}")
                raise UserError(f"Metadata insert failed: {error_msg}", status_code=response.status_code)
    except UserError as ae:
        # Let AuthError pass through with its original message and status
        raise ae
    except Exception:
        logger.exception(f"Unexpected error during metadata insert for {email}")
        raise UserError("Unexpected error during metadata insert", status_code=500)

async def update_user_status(user_id: str, status: str, is_deleted: bool, headers: dict):
    logger.info(f"Updating status for user ID {user_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{user_id}",
                headers=headers,
                json={
                    "status": status,
                    "is_deleted": is_deleted,
                    "updated_at": current_timestamp()
                }
            )
            
            if response.status_code >= 400:
                result = response.json()
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Status update failed for user ID {user_id}: {error_msg}")
                raise UserError(f"Status update failed: {error_msg}", status_code=response.status_code)
            return "Status of User updated successfully"
    except UserError as ae:
        # Let UserError pass through with its original message and status
        raise ae
    except Exception:
        logger.exception(f"Unexpected error during status update for user ID {user_id}")
        raise UserError("Unexpected error during status update", status_code=500)

async def get_user_metadata(user_id: str, headers: dict):
    logger.info(f"Fetching metadata for user ID {user_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{user_id}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            logger.debug(result)
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Metadata fetch failed for user ID {user_id}: {error_msg}")
                raise UserError(f"Metadata fetch failed: {error_msg}", status_code=response.status_code)
            return result
    except Exception:
        logger.exception(f"Unexpected error during metadata fetch for user ID {user_id}")
        raise UserError("Unexpected error during metadata fetch", status_code=500)

async def get_user_metadata_by_email(email: str, headers: dict):
    logger.info(f"Fetching metadata for user having email ID as {email}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?email=eq.{email}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            logger.debug(result)
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Metadata fetch failed for user with email ID as {email}: {error_msg}")
                raise UserError(f"Metadata fetch failed: {error_msg}", status_code=response.status_code)
            return result
    except UserError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during metadata fetch for user with email ID as {email}")
        raise UserError("Unexpected error", status_code=500)

async def get_user_roles(user_id: str, headers: dict) -> list[str]:
    user_roles = await supabase_query(
        "user_roles",
        {"user_id": f"eq.{user_id}", "is_deleted": "eq.false"},
        "role_id",
        headers
    )
    if not user_roles:
        return []
    role_ids = [r["role_id"] for r in user_roles]
    roles = []
    for role_id in role_ids:
        role_data = await supabase_query("roles", {"id": f"eq.{role_id}"}, "name", headers)
        if role_data:
            roles.append(role_data[0]["name"])
    return roles

async def insert_or_reactivate_user_role(user_id: str, role_name: str, created_by: str, headers: dict):
    logger.info(f"Inserting or reactivating user's role {role_name} for user ID {user_id}")
    try:
        role_data = await supabase_query("roles", {"name": f"eq.{role_name}"}, "id", headers)
        if not role_data:
            raise UserError(f"Role '{role_name}' not found", status_code=404)
        role_id = role_data[0]["id"]
        payload = {
            "user_id": user_id,
            "role_id": role_id,
            "is_deleted": False,
            "created_by":created_by,
            "updated_by": created_by,
            "updated_at":current_timestamp()
        }

        # Add upsert header
        upsert_headers = {
            **headers,
            "Prefer": "resolution=merge-duplicates"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/user_roles",
                json=payload,
                headers=upsert_headers
            )

            if response.status_code >= 400:
                raise UserError(f"Failed to assign role '{role_name}'", status_code=response.status_code)
    except UserError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during insert or reactivate user roles for user {user_id}")
        raise UserError("Unexpected error", status_code=500)

async def delete_user_role(user_id: str, role_name: str, updated_by: str, headers: dict):
    role_data = await supabase_query("roles", {"name": f"eq.{role_name}"}, "id", headers)
    if not role_data:
        raise UserError(f"Role '{role_name}' not found", status_code=404)
    role_id = role_data[0]["id"]
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{SUPABASE_URL}/rest/v1/user_roles?user_id=eq.{user_id}&role_id=eq.{role_id}",
            headers=headers,
            json={
                "is_deleted": True,
                "updated_by": updated_by,
                "updated_at": current_timestamp()
            }
        )
        if response.status_code >= 400:
            raise UserError(f"Failed to remove role '{role_name}'", status_code=response.status_code)