from app.config import SUPABASE_URL
from app.exceptions.exceptions import PeelingBeforeDryingError
import httpx
from app.utils.logger import logger
from app.utils.timestamp_utils import current_timestamp

TABLE = "peeling_before_drying"

async def insert_peeling_before_drying(data: list[dict], headers: dict):
    logger.info(f"Inserting peeling before drying records for batches {[item.get('batch_number') for item in data]}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json=[{**item, "is_deleted": False} for item in data]
            )
            result = response.json()
            if response.status_code >= 400:
                raise PeelingBeforeDryingError(f"Insert failed: {result}", status_code=response.status_code)
            return result
    except PeelingBeforeDryingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during inserting peeling_before_drying records for batches {[item.get('batch_number') for item in data]}")
        raise PeelingBeforeDryingError("Unexpected error", status_code=500)
    
async def update_peeling_before_drying(data: list[dict], headers: dict):
    logger.info(f"Updating peeling_before_drying records for IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            logger.debug(f"Updating peeling_before_drying ID {item.get('id')}")
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
                raise PeelingBeforeDryingError(f"Update failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("peeling_before_drying records updated successfully")
    return updated_records
    
async def delete_peeling_before_drying(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting peeling_before_drying record IDs {[item.get('id') for item in data]}")
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
                raise PeelingBeforeDryingError(f"Soft-delete failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("peeling_before_drying records Soft-deleted successfully")
    return updated_records

async def fetch_all_peeling_before_drying(headers: dict):
    logger.info("Fetching all peeling before drying records")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise PeelingBeforeDryingError(f"Fetch failed: {result}", status_code=response.status_code)
        return result


async def fetch_all_peeling_before_drying_by_batch_number(batch_number: str, headers: dict):
    logger.info(f"Fetching all peeling_before_drying records for batch {batch_number}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or response.text
                logger.error(f"Failed while fetching peeling_before_drying records for batch {batch_number}: {error_msg}")
                raise PeelingBeforeDryingError(f"Failed while fetching peeling_before_drying records for batch {batch_number}: {error_msg}", status_code=response.status_code)
            return result
    except PeelingBeforeDryingError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching peeling_before_drying records for batch {batch_number}")
        raise PeelingBeforeDryingError("Unexpected error", status_code=500)


async def fetch_peeling_before_drying_by_id(peel_id: str, headers: dict):
    logger.info(f"Fetching peeling_before_drying record for ID {peel_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{peel_id}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching peeling_before_drying record for ID {peel_id}: {error_msg}")
                raise PeelingBeforeDryingError(f"Failed while fetching peeling_before_drying record for ID {peel_id}: {error_msg}", status_code=response.status_code)
            return result
    except PeelingBeforeDryingError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching peeling_before_drying record for ID {peel_id}")
        raise PeelingBeforeDryingError("Unexpected error", status_code=500)


async def fetch_peeling_before_drying_by_date(date: str, headers: dict):
    logger.info(f"Fetching peeling_before_drying records for date: {date}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?peeling_date=eq.{date}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching peeling_before_drying records for date {date}: {error_msg}")
                raise PeelingBeforeDryingError(f"Failed while fetching peeling_before_drying records for date {date}: {error_msg}", status_code=response.status_code)
            return result
    except PeelingBeforeDryingError as ue:
        raise ue    
    except Exception:
        logger.exception(f"Unexpected error during fetching peeling_before_drying records for date {date}")
        raise PeelingBeforeDryingError("Unexpected error", status_code=500)