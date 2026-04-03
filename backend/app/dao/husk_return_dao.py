from app.config import SUPABASE_URL
from app.exceptions.exceptions import HuskReturnError
import httpx
from app.utils.logger import logger
from app.utils.timestamp_utils import current_timestamp

TABLE = "husk_return"

async def insert_husk_return(data: list[dict], headers: dict):
    logger.info(f"Inserting husk_return records for batches {[item.get('batch_number') for item in data]}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json=[{**item, "is_deleted": False} for item in data]
            )
            result = response.json()
            if response.status_code >= 400:
                raise HuskReturnError(f"Insert failed: {result}", status_code=response.status_code)
            return result
    except HuskReturnError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during inserting husk_return records for batches {[item.get('batch_number') for item in data]}")
        raise HuskReturnError("Unexpected error", status_code=500)


async def update_husk_return(data: list[dict], headers: dict):
    logger.info(f"Updating husk_return records for IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            logger.debug(f"Updating husk_return ID {item.get('id')}")
            patch_data = {
                **{k: v for k, v in item.items() if k != "id" and v is not None},
                "updated_by": item["updated_by"],
                "updated_at": current_timestamp()
            }

            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{item['id']}&is_deleted=eq.false",
                headers=headers,
                json=patch_data
            )
            result = response.json()
            if response.status_code >= 400:
                raise HuskReturnError(f"Update failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("husk_return records updated successfully")
    return updated_records


async def delete_husk_return(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting husk_return record IDs {[item.get('id') for item in data]}")
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
                raise HuskReturnError(f"Soft-delete failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("husk_return records Soft-deleted successfully")
    return updated_records


async def fetch_all_husk_return(headers: dict):
    logger.info("Fetching all husk_return records")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise HuskReturnError(f"Fetch failed: {result}", status_code=response.status_code)
        return result


async def fetch_all_husk_return_by_batch_number(batch_number: str, headers: dict):
    logger.info(f"Fetching all husk_return records for batch {batch_number}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or response.text
                logger.error(f"Failed while fetching husk_return records for batch {batch_number}: {error_msg}")
                raise HuskReturnError(f"Failed while fetching husk_return records for batch {batch_number}: {error_msg}", status_code=response.status_code)
            return result
    except HuskReturnError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching husk_return records for batch {batch_number}")
        raise HuskReturnError("Unexpected error", status_code=500)


async def fetch_husk_return_by_id(husk_id: str, headers: dict):
    logger.info(f"Fetching husk_return record for ID {husk_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{husk_id}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching husk_return record for ID {husk_id}: {error_msg}")
                raise HuskReturnError(f"Failed while fetching husk_return record for ID {husk_id}: {error_msg}", status_code=response.status_code)
            return result
    except HuskReturnError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching husk_return record for ID {husk_id}")
        raise HuskReturnError("Unexpected error", status_code=500)


async def fetch_husk_return_by_date(date: str, headers: dict):
    logger.info(f"Fetching husk_return records for date: {date}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?return_date=eq.{date}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching husk_return records for date {date}: {error_msg}")
                raise HuskReturnError(f"Failed while fetching husk_return records for date {date}: {error_msg}", status_code=response.status_code)
            return result
    except HuskReturnError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching husk_return records for date {date}")
        raise HuskReturnError("Unexpected error", status_code=500)
