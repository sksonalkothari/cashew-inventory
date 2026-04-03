from app.config import SUPABASE_URL
from app.exceptions.exceptions import DryingError
import httpx
from app.utils.logger import logger
from app.utils.timestamp_utils import current_timestamp

TABLE = "drying"

async def insert_drying(data: list[dict], headers: dict):
    logger.info(f"Inserting drying records for batches {[item.get('batch_number') for item in data]}")
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
                raise DryingError(f"Insert failed for batches: {[item.get('batch_number') for item in data]}: {error_msg}", status_code=response.status_code)
            logger.info(f"Drying records inserted successfully")
            return response_data
    except DryingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during inserting drying records for batches {[item.get('batch_number') for item in data]}")
        raise DryingError("Unexpected error", status_code=500)

async def update_drying(data: list[dict], headers: dict):
    logger.info(f"Updating drying records for IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            logger.debug(f"Updating drying ID {item.get('id')}")
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
                logger.error(f"Update failed for drying ID {item.get('id')}: {result}")
                raise DryingError(f"Update failed for drying ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("Drying records updated successfully")
    return updated_records

async def delete_drying(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting drying record IDs {[item.get('id') for item in data]}")
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
                logger.error(f"Soft-delete failed for drying ID {item.get('id')}: {result}")
                raise DryingError(f"Soft-delete failed for drying ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("Drying records Soft-deleted successfully")
    return updated_records

async def fetch_all_drying(headers: dict):
    logger.info("Fetching all drying records")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise DryingError(f"Fetch failed: {result}", status_code=response.status_code)
        return result

async def fetch_all_drying_by_batch_number(batch_number: str, headers: dict):
    logger.info(f"Fetching all drying records for batch {batch_number}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or response.text
                logger.error(f"Failed while fetching drying records for batch {batch_number}: {error_msg}")
                raise DryingError(f"Failed while fetching drying records for batch {batch_number}: {error_msg}", status_code=response.status_code)
            return result
    except DryingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching drying records for batch {batch_number}")
        raise DryingError("Unexpected error", status_code=500)


async def fetch_drying_by_id(drying_id: str, headers: dict):
    logger.info(f"Fetching drying record for ID {drying_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{drying_id}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching drying record for ID {drying_id}: {error_msg}")
                raise DryingError(f"Failed while fetching drying record for ID {drying_id}: {error_msg}", status_code=response.status_code)
            return result
    except DryingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching drying record for ID {drying_id}")
        raise DryingError("Unexpected error", status_code=500)


async def fetch_drying_by_date(date: str, headers: dict):
    logger.info(f"Fetching drying records for date: {date}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?drying_date=eq.{date}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching drying records for date {date}: {error_msg}")
                raise DryingError(f"Failed while fetching drying records for date {date}: {error_msg}", status_code=response.status_code)
            return result
    except DryingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching drying records for date {date}")
        raise DryingError("Unexpected error", status_code=500)