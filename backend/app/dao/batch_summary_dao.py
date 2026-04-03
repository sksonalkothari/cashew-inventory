import httpx
from app.config import SUPABASE_URL
from app.utils.timestamp_utils import current_timestamp
from app.exceptions.exceptions import BatchSummaryError
from app.utils.logger import logger

TABLE = "batch_summary"

async def insert_batch(data: list[dict], headers: dict):
    logger.info(f"Inserting batches {[item['batch_number'] for item in data]}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json=[{**item, "is_deleted": False} for item in data]
            )
            response_data = response.json()
            inserted = response_data if isinstance(response_data, list) else [] 
            failed = detect_failed_inserts(data, inserted)
            if failed:
                logger.warning(f"Insert failed for batches: {[item['batch_number'] for item in failed]}")
            
            if response.status_code >= 400:
                result = response.json()
                error_msg = result.get("msg") or response.text
                logger.error(f"Insert failed for batches: {[item['batch_number'] for item in data]}: {error_msg}")
                raise BatchSummaryError(f"Insert failed: {error_msg}", status_code=response.status_code)
            
            logger.info(f"Batches {[item['batch_number'] for item in data]} inserted successfully")
            return response_data
        
    except BatchSummaryError as ue:
        raise ue
    except Exception as e:
        logger.error(f"Unexpected error during inserting batches: {[item['batch_number'] for item in data]}: {e}")
        raise BatchSummaryError("Unexpected error", status_code=500)

async def update_batch(data: dict, headers: dict):
    logger.info(f"Updating batch {data['batch_number']}")
    try:
        patch_data = {
            **{k: v for k, v in data.items() if k != "batch_number" and v is not None},
            "updated_by": data["updated_by"],
            "updated_at": current_timestamp()
        }
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{data['batch_number']}&is_deleted=eq.false",
                headers=headers,
                json=patch_data
            )
            if response.status_code >= 400:
                result = response.json()
                error_msg = result.get("msg") or response.text
                logger.error(f"Update failed for batch: {data['batch_number']}: {error_msg}")
                raise BatchSummaryError(f"Update failed: {error_msg}", status_code=response.status_code)
            logger.info(f"Batch {data['batch_number']} updated successfully")
            return f"Batch: {data['batch_number']} updated successfully"
    except BatchSummaryError as ue:
        raise ue
    except Exception:
        logger.error(f"Unexpected error during updating batch: {data['batch_number']}")
        raise BatchSummaryError("Unexpected error", status_code=500)

async def soft_delete_batch(data: dict, headers: dict):
    logger.info(f"Soft-deleting batch {data['batch_number']}")
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{data['batch_number']}&is_deleted=eq.false",
            headers=headers,
            json={
                "is_deleted": True,
                "updated_by": data["updated_by"],
                "updated_at": current_timestamp()
            }
        )
        if response.status_code >= 400:
            raise BatchSummaryError(f"Delete failed for {data['batch_number']}", status_code=response.status_code)

async def fetch_all_batches(headers: dict):
    logger.info("Fetching all batches")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise BatchSummaryError("Fetch all batches failed", status_code=response.status_code)
        return result

async def fetch_unsold_batches(headers: dict):
    logger.info("Fetching unsold batches")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?status=neq.Sold&is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise BatchSummaryError("Fetch unsold batches failed", status_code=response.status_code)
        return result
    
async def fetch_batch_by_number(batch_number: str, headers: dict):
    logger.info(f"Fetching batch {batch_number}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or response.text
                logger.error(f"Fetch failed for batch: {batch_number}: {error_msg}")
                raise BatchSummaryError(f"Fetch failed for batch {batch_number}", status_code=response.status_code)
            return result
    except BatchSummaryError as ue:
        raise ue
    except Exception:
        logger.error(f"Unexpected error during fetching batch: {batch_number}")
        raise BatchSummaryError("Unexpected error", status_code=500)

async def fetch_batch_by_number_and_origin(batch_number: str, origin: str, headers: dict):
    logger.info(f"Fetching batch ({batch_number}, {origin})")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&origin=eq.{origin}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or response.text
                logger.error(f"Fetch failed for batch ({batch_number}, {origin}): {error_msg}")
                raise BatchSummaryError(f"Fetch failed for batch ({batch_number}, {origin})", status_code=response.status_code)
            return result
    except BatchSummaryError as ue:
        raise ue
    except Exception:
        logger.error(f"Unexpected error during fetching batch: ({batch_number}, {origin})")
        raise BatchSummaryError("Unexpected error", status_code=500)

def detect_failed_inserts(sent: list[dict], returned: list[dict], key: str = "batch_number"):
    returned_keys = {row[key] for row in returned}
    failed = [row for row in sent if row[key] not in returned_keys]
    return failed