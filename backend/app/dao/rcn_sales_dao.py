from app.config import SUPABASE_URL
from app.exceptions.exceptions import RcnSalesError
import httpx
from app.utils.logger import logger
from app.utils.timestamp_utils import current_timestamp

TABLE = "rcn_sales"


async def insert_rcn_sales(data: list[dict], headers: dict):
    logger.info(f"Inserting rcn_sales records for bills {[item.get('bill_number') for item in data]}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json=[{**item, "is_deleted": False} for item in data]
            )
            result = response.json()
            if response.status_code >= 400:
                raise RcnSalesError(f"Insert failed: {result}", status_code=response.status_code)
            return result
    except RcnSalesError as re:
        raise re
    except Exception:
        logger.exception("Unexpected error during inserting rcn_sales records")
        raise RcnSalesError("Unexpected error", status_code=500)


async def update_rcn_sales(data: list[dict], headers: dict):
    logger.info(f"Updating rcn_sales records for IDs {[item.get('id') for item in data]}")
    updated_records = []
    async with httpx.AsyncClient() as client:
        for item in data:
            logger.debug(f"Updating rcn_sales ID {item.get('id')}")
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
                raise RcnSalesError(f"Update failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("rcn_sales records updated successfully")
    return updated_records


async def delete_rcn_sales(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting rcn_sales record IDs {[item.get('id') for item in data]}")
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
                raise RcnSalesError(f"Soft-delete failed for ID {item.get('id')}: {result}", status_code=response.status_code)
            updated_records.extend(result if isinstance(result, list) else [result])

    logger.info("rcn_sales records Soft-deleted successfully")
    return updated_records


async def fetch_all_rcn_sales(headers: dict):
    logger.info("Fetching all rcn_sales records")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise RcnSalesError(f"Fetch failed: {result}", status_code=response.status_code)
        return result


async def fetch_all_rcn_sales_by_batch_number(batch_number: str, headers: dict):
    logger.info(f"Fetching all rcn_sales records for batch {batch_number}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?batch_number=eq.{batch_number}&is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise RcnSalesError(f"Failed while fetching rcn_sales records for batch {batch_number}: {result}", status_code=response.status_code)
        return result


async def fetch_rcn_sales_by_id(sale_id: str, headers: dict):
    logger.info(f"Fetching rcn_sales record for ID {sale_id}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{sale_id}&is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise RcnSalesError(f"Failed while fetching rcn_sales record for ID {sale_id}: {result}", status_code=response.status_code)
        return result


async def fetch_rcn_sales_by_date(date: str, headers: dict):
    logger.info(f"Fetching rcn_sales records for date: {date}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?sale_date=eq.{date}&is_deleted=eq.false",
            headers=headers
        )
        result = response.json()
        if response.status_code >= 400:
            raise RcnSalesError(f"Failed while fetching rcn_sales records for date {date}: {result}", status_code=response.status_code)
        return result
