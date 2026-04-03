from app.config import SUPABASE_URL
from app.exceptions.exceptions import HumidifyingError
import httpx
from app.utils.logger import logger
from app.utils.timestamp_utils import current_timestamp

TABLE = "humidifying"

async def insert_humidifying(data: list[dict], headers: dict):
    logger.info(f"Inserting humidifying records for batches {[item.get('batch_number') for item in data]}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json=[{**item, "is_deleted": False} for item in data]
            )
            response_data = response.json()
            if response.status_code >= 400:
                error_msg = response_data.get("msg") or response.text
                logger.error(f"Insert failed for batches: {[item.get('batch_number') for item in data]}: {error_msg}")
                raise HumidifyingError(f"Insert failed for batches: {[item.get('batch_number') for item in data]}: {error_msg}", status_code=response.status_code)
            logger.info(f"Humidifying records inserted successfully")
            return response_data
    except HumidifyingError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during inserting humidifying records for batches {[item.get('batch_number') for item in data]}")
        raise HumidifyingError("Unexpected error", status_code=500)
    
async def update_humidifying(data: list[dict], headers: dict):
    logger.info(f"Updating humidifying records for IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            logger.debug(f"Updating humidifying ID {item.get('id')}")
            patch_data = {
                **{k: v for k, v in item.items() if k != "id" and v is not None},
                "updated_by": item["updated_by"],
                "updated_at": current_timestamp(),
                "is_deleted": False
            }

            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{item['id']}&is_deleted=eq.false",
                headers=headers,
                json=patch_data
            )
            result = response.json()
            if response.status_code >= 400:
                logger.error(f"Update failed for humidifying ID {item.get('id')}: {result}")
                raise HumidifyingError(f"Update failed for humidifying ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("Humidifying records updated successfully")
    return updated_records
    
async def delete_humidifying(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting humidifying record IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{item['id']}&is_deleted=eq.false",
                headers=headers,
                json={
                    "is_deleted": True,
                    "updated_by": item["updated_by"],
                    "updated_at": current_timestamp()
                }
            )
            result = response.json()
            if response.status_code >= 400:
                logger.error(f"Soft-delete failed for humidifying ID {item.get('id')}: {result}")
                raise HumidifyingError(f"Soft-delete failed for humidifying ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("Humidifying records Soft-deleted successfully")
    return updated_records

async def fetch_all_humidifying(headers: dict):
    logger.info("Fetching all humidifying records")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise HumidifyingError(f"Fetch failed: {result}", status_code=response.status_code)
        return result
    
async def fetch_all_humidifying_by_batch_number(batch_number: str, headers: dict):
    logger.info(f"Fetching all humidifying records for batch {batch_number}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or response.text
                logger.error(f"Failed while fetching humidifying records for batch {batch_number}: {error_msg}")
                raise HumidifyingError(f"Failed while fetching humidifying records for batch {batch_number}: {error_msg}", status_code=response.status_code)
            return result
    except HumidifyingError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching humidifying records for batch {batch_number}")
        raise HumidifyingError("Unexpected error", status_code=500)


async def fetch_humidifying_by_id(humid_id: str, headers: dict):
    logger.info(f"Fetching humidifying record for ID {humid_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{humid_id}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching humidifying record for ID {humid_id}: {error_msg}")
                raise HumidifyingError(f"Failed while fetching humidifying record for ID {humid_id}: {error_msg}", status_code=response.status_code)
            return result
    except HumidifyingError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching humidifying record for ID {humid_id}")
        raise HumidifyingError("Unexpected error", status_code=500)


async def fetch_humidifying_by_date(date: str, headers: dict):
    logger.info(f"Fetching humidifying records for date: {date}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?humidifying_date=eq.{date}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching humidifying records for date {date}: {error_msg}")
                raise HumidifyingError(f"Failed while fetching humidifying records for date {date}: {error_msg}", status_code=response.status_code)
            return result
    except HumidifyingError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching humidifying records for date {date}")
        raise HumidifyingError("Unexpected error", status_code=500)