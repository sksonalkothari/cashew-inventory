from app.config import SUPABASE_URL
from app.exceptions.exceptions import ProductionError
import httpx
from app.utils.logger import logger
from app.utils.timestamp_utils import current_timestamp

TABLE = "production"


async def insert_production(data: list[dict], headers: dict):
    logger.info(f"Inserting production records for batches {[item.get('batch_number') for item in data]}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json=[{**item, "is_deleted": False} for item in data]
            )
            result = response.json()
            if response.status_code >= 400:
                raise ProductionError(f"Insert failed: {result}", status_code=response.status_code)
            return result
    except ProductionError as pe:
        raise pe
    except Exception:
        logger.exception("Unexpected error during inserting production records")
        raise ProductionError("Unexpected error", status_code=500)


async def update_production(data: list[dict], headers: dict):
    logger.info(f"Updating production records for IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            logger.debug(f"Updating production ID {item.get('id')}")
            patch_data = {
                **{k: v for k, v in item.items() if k != "id" and v is not None},
                "updated_by": item.get("updated_by"),
                "updated_at": current_timestamp()
            }

            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{item['id']}&is_deleted=eq.false",
                headers=headers,
                json=patch_data
            )
            result = response.json()
            if response.status_code >= 400:
                raise ProductionError(f"Update failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("production records updated successfully")
    return updated_records


async def delete_production(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting production record IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{item['id']}&is_deleted=eq.false",
                headers=headers,
                json={
                    "is_deleted": True,
                    "updated_by": item.get("updated_by"),
                    "updated_at": current_timestamp()
                }
            )
            result = response.json()
            if response.status_code >= 400:
                raise ProductionError(f"Soft-delete failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("production records Soft-deleted successfully")
    return updated_records


async def fetch_all_production(headers: dict):
    logger.info("Fetching all production records")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise ProductionError(f"Fetch failed: {result}", status_code=response.status_code)
        return result


async def fetch_all_production_by_batch_number(batch_number: str, headers: dict):
    logger.info(f"Fetching all production records for batch {batch_number}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise ProductionError(f"Failed while fetching production records for batch {batch_number}: {result}", status_code=response.status_code)
        return result


async def fetch_production_by_id(prod_id: str, headers: dict):
    logger.info(f"Fetching production record for ID {prod_id}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{prod_id}&is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise ProductionError(f"Failed while fetching production record for ID {prod_id}: {result}", status_code=response.status_code)
        return result


async def fetch_production_by_date(date: str, headers: dict):
    logger.info(f"Fetching production records for date: {date}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?production_date=eq.{date}&is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise ProductionError(f"Failed while fetching production records for date {date}: {result}", status_code=response.status_code)
        return result
