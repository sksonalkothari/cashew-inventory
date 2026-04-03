import httpx
from app.utils.logger import logger
from app.exceptions.exceptions import BatchError
from app.config import SUPABASE_URL
from app.dao.batch_mapping import map_batch_to_batchlistitem
from app.utils.timestamp_utils import current_timestamp

TABLE = "batch"

async def fetch_inprogress_batches_by_stage(stage: str, headers: dict):
    logger.info(f"Fetching IN_PROGRESS batches for stage: {stage}")
    try:
        status_col = f"{stage}_status"
        logger.debug(f"Using status column: {status_col}")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false&{status_col}=eq.In_Progress",
                headers=headers
            )
            result = response.json()
            logger.debug(f"Response for IN_PROGRESS batches for stage {stage}: {result}")
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Fetch IN_PROGRESS batches for stage {stage} failed: {error_msg}")
                raise BatchError(f"Fetch IN_PROGRESS batches for stage {stage} failed: {error_msg}", status_code=response.status_code)
            return [map_batch_to_batchlistitem(row) for row in result]
    except BatchError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching IN_PROGRESS batches for stage {stage}")
        raise BatchError("Unexpected error", status_code=500)
    
async def fetch_inprogress_batches(headers: dict):
    logger.info("Fetching IN_PROGRESS batches from batch table")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false&status=eq.In_Progress",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Fetch IN_PROGRESS batches failed: {error_msg}")
                raise BatchError(f"Fetch IN_PROGRESS batches failed: {error_msg}", status_code=response.status_code)
            return [map_batch_to_batchlistitem(row) for row in result]
    except BatchError as ue:
        raise ue
    except Exception:
        logger.exception("Unexpected error during fetching IN_PROGRESS batches")
        raise BatchError("Unexpected error", status_code=500)

async def fetch_all_batches(headers: dict):
    logger.info("Fetching all batches from batch table")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false&order=batch_entry_date.asc",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Fetch all batches failed: {error_msg}")
                raise BatchError(f"Fetch all batches failed: {error_msg}", status_code=response.status_code)
            # Map each row to BatchListItem structure
            return [map_batch_to_batchlistitem(row) for row in result]
    except BatchError as ue:
        raise ue
    except Exception:
        logger.exception("Unexpected error during fetching all batches")
        raise BatchError("Unexpected error", status_code=500)

async def insert_batch(data: dict, headers: dict):
    logger.info(f"Inserting new batch: {data.get('batch_number')}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json={**data, "is_deleted": False}
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Insert failed for batch {data.get('batch_number')}: {error_msg}")
                raise BatchError(f"Insert failed for batch {data.get('batch_number')}: {error_msg}", status_code=response.status_code)
            logger.info(f"Batch inserted successfully: {data.get('batch_number')}")
            return result
    except BatchError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during inserting batch {data.get('batch_number')}")
        raise BatchError("Unexpected error", status_code=500)

async def update_batch(data: dict, headers: dict):
    """
    Update batch record. Automatically sets *_updated_at and *_updated_by
    for any stage status provided in `data`.
    """
    batch_number = data.get("batch_number")
    logger.info(f"Updating batch: {batch_number}")

    logger.debug(f"Update data received for batch {batch_number}: {data}")
    # Build payload
    payload = {}
    payload["updated_by"] = data.get("updated_by")
    logger.debug(f"Set updated_by for batch {batch_number}: {payload['updated_by']}")
    logger.debug(f"Current timestamp for batch {batch_number}: {current_timestamp()}")
    payload["updated_at"] = current_timestamp()
    logger.debug(f"Set updated_at for batch {batch_number}: {payload['updated_at']}")

    logger.debug(f"Initial update payload for batch {batch_number}: {payload}")

    # Always allow updating origin, entry_date, etc.
    for field in ["origin", "batch_entry_date", "is_deleted"]:
        if field in data:
            payload[field] = data[field]

    # Map of stage names to their status fields
    stage_fields = [
        "purchase",
        "boiling",
        "nw_drying",
        "nw_humidification",
        "peeling_before_drying",
        "peeling_after_drying",
        "production",
        "cashew_kernel_sales",
        "rcn_sales",
    ]

    for stage in stage_fields:
        status_field = f"{stage}_status"
        if status_field in data:
            payload[status_field] = data[status_field]
            payload[f"{stage}_updated_at"] = current_timestamp()
            payload[f"{stage}_updated_by"] = data.get("updated_by")
    logger.debug(f"Update payload for batch {batch_number}: {payload}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}",
                headers=headers,
                json=payload,
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = (
                    result.get("msg")
                    or result.get("error", {}).get("message")
                    or response.text
                )
                logger.error(f"Update failed for batch {batch_number}: {error_msg}")
                raise BatchError(
                    f"Update failed for batch {batch_number}: {error_msg}",
                    status_code=response.status_code,
                )
            logger.info(f"Batch updated successfully: {batch_number}")
            return result
    except BatchError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during updating batch {batch_number}")
        raise BatchError("Unexpected error", status_code=500)
