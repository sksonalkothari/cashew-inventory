import httpx
from app.utils.logger import logger
from app.utils.timestamp_utils import current_timestamp
from app.config import SUPABASE_URL
from app.exceptions.exceptions import BoilingError

TABLE = "boiling"

async def insert_boiling(data: list[dict], headers: dict):
    logger.info(f"Inserting boiling records for batches {[item.get('batch_number') for item in data]}")
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
                raise BoilingError(f"Insert failed for batches: {[item.get('batch_number') for item in data]}: {error_msg}", status_code=response.status_code)
            logger.info(f"Boiling records inserted successfully")
            return response_data
    except BoilingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during inserting boiling records for batches {[item.get('batch_number') for item in data]}")
        raise BoilingError("Unexpected error", status_code=500)

async def update_boiling(data: list[dict], headers: dict):
    logger.info(f"Updating boiling records for IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            logger.debug(f"Updating boiling ID {item.get('id')}")
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
                logger.error(f"Update failed for boiling ID {item.get('id')}: {result}")
                raise BoilingError(f"Update failed for boiling ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("Boiling records updated successfully")
    return updated_records

async def delete_boiling(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting boiling record IDs {[item.get('id') for item in data]}")
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
                logger.error(f"Soft-delete failed for boiling ID {item.get('id')}: {result}")
                raise BoilingError(f"Soft-delete failed for boiling ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("Boiling records Soft-deleted successfully")
    return updated_records

async def fetch_all_boiling(headers: dict):
    logger.info("Fetching all boiling records")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise BoilingError(f"Fetch failed: {result}", status_code=response.status_code)
        return result
    
async def fetch_all_boilings_by_batch_number(batch_number: str, headers: dict):
    logger.info(f"Fetching all boiling records for batch {batch_number}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching boiling records for batch {batch_number}: {error_msg}")
                raise BoilingError(f"Failed while fetching boiling records for batch {batch_number}: {error_msg}", status_code=response.status_code)
            return result
    except BoilingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching boiling records for batch {batch_number}")
        raise BoilingError("Unexpected error", status_code=500)


async def fetch_boiling_by_id(boiling_id: str, headers: dict):
    logger.info(f"Fetching boiling record for ID {boiling_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{boiling_id}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching boiling record for ID {boiling_id}: {error_msg}")
                raise BoilingError(f"Failed while fetching boiling record for ID {boiling_id}: {error_msg}", status_code=response.status_code)
            return result
    except BoilingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching boiling record for ID {boiling_id}")
        raise BoilingError("Unexpected error", status_code=500)
    
async def fetch_boiling_by_date(date: str, headers: dict):
    logger.info(f"Fetching boiling records for date: {date}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?boiling_date=eq.{date}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching boiling records for date {date}: {error_msg}")
                raise BoilingError(f"Failed while fetching boiling records for date {date}: {error_msg}", status_code=response.status_code)
            return result
    except BoilingError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching boiling records for date {date}")
        raise BoilingError("Unexpected error", status_code=500)
    
async def get_distinct_dates(headers: dict) -> list[str]:
    logger.info("Fetching boiling distinct dates")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?select=boiling_date&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()

            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching boiling distinct dates: {error_msg}")
                raise BoilingError(f"Failed while fetching boiling distinct dates: {error_msg}", status_code=response.status_code)

            # Extract and deduplicate dates
            dates = {row["boiling_date"] for row in result if "boiling_date" in row}
            return sorted(dates)

    except BoilingError as ue:
        raise ue
    except Exception:
        logger.exception("Unexpected error during fetching boiling distinct dates")
        raise BoilingError("Unexpected error", status_code=500)