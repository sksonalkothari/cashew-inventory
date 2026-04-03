import httpx
from app.config import SUPABASE_URL
from app.utils.timestamp_utils import current_timestamp
from app.exceptions.exceptions import PurchaseError
from app.utils.logger import logger

TABLE = "purchases"

async def insert_purchase(data: list[dict], headers: dict):
    logger.info(f"Inserting purchase records for bills {[item['bill_number'] for item in data]}")
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
                logger.warning(f"Insert failed for bills: {[item['bill_number'] for item in failed]}")
                
            if response.status_code >= 400:
                error_msg = response_data.get("msg") or response.text
                logger.error(f"Insert failed for bills: {[item['bill_number'] for item in data]}: {error_msg}")
                raise PurchaseError(f"Insert failed for bills: {[item['bill_number'] for item in data]}: {error_msg}", status_code=response.status_code)
            
            logger.info(f"Purchase records inserted successfully")
            return response_data

    except PurchaseError as ue:
        raise ue
    except Exception as e:
        logger.error(f"Unexpected error during inserting purchase for bills {[item['bill_number'] for item in data]}: {e}")
        raise PurchaseError("Unexpected error", status_code=500)

async def update_purchase(data: list[dict], headers: dict):
    logger.info(f"Updating purchase records for bills {[item['bill_number'] for item in data]}")
    updated_records = []

    async with httpx.AsyncClient() as client:
        for item in data:
            patch_data = {
                **{k: v for k, v in item.items() if k != "id" and v is not None},
                "updated_by": item["updated_by"],
                "updated_at": current_timestamp(),
                "is_deleted": False
            }

            try:
                response = await client.patch(
                    f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{item['id']}&is_deleted=eq.false",
                    headers=headers,
                    json=patch_data
                )
                result = response.json()
                if response.status_code >= 400:
                    logger.error(f"Update failed for bill {item['bill_number']}: {result}")
                    raise PurchaseError(f"Update failed for bill {item['bill_number']}: {result}", status_code=response.status_code)
                updated_records.extend(result if isinstance(result, list) else [result])
            except PurchaseError as ue:
                raise ue
            except Exception as e:
                logger.error(f"Unexpected error during update for bill {item['bill_number']}: {e}")
                raise PurchaseError("Unexpected error during update", status_code=500)

    logger.info("Purchase records updated successfully")
    logger.debug(f"Updated records: {updated_records}")
    return updated_records

async def soft_delete_purchase(data: list[dict], headers: dict):
    logger.info(f"Soft-deleting purchase IDs {[item['id'] for item in data]}")
    async with httpx.AsyncClient() as client:
        updated_records = []
        try:
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
                    logger.error(f"Soft-delete failed for bill {item['bill_number']}: {result}")
                    raise PurchaseError(f"Soft-delete failed for bill {item['bill_number']}: {result}", status_code=response.status_code)
                updated_records.extend(result if isinstance(result, list) else [result])
        except PurchaseError as ue:
            raise ue
        except Exception as e:
            logger.error(f"Unexpected error during soft-delete for bill {item['bill_number']}: {e}")
            raise PurchaseError("Unexpected error during soft-delete", status_code=500)

    logger.info("Purchase records Soft-deleted successfully")
    logger.debug(f"Soft-deleted records: {updated_records}")
    return updated_records

async def fetch_all_purchases(headers: dict):
    logger.info("Fetching all purchases")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching all Purchase records: {error_msg}")
                raise PurchaseError(f"Failed while fetching all Purchase records: {error_msg}", status_code=response.status_code)
            return result
    except PurchaseError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching all Purchase records")
        raise PurchaseError("Unexpected error", status_code=500)

def detect_failed_inserts(sent: list[dict], returned: list[dict], key: str = "batch_number"):
    returned_keys = {row[key] for row in returned}
    failed = [row for row in sent if row[key] not in returned_keys]
    return failed

async def fetch_purchases_by_date(date: str, headers: dict):
    logger.info(f"Fetching purchases for date {date}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?purchase_date=eq.{date}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching Purchase records for date {date}: {error_msg}")
                raise PurchaseError(f"Failed while fetching Purchase records for date {date}: {error_msg}", status_code=response.status_code)
            return result
    except PurchaseError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching Purchase records for date {date}")
        raise PurchaseError("Unexpected error", status_code=500)
    
async def fetch_purchase_by_id(purchase_id: str, headers: dict):
    logger.info(f"Fetching purchase for ID {purchase_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{purchase_id}&is_deleted=eq.false",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                logger.error(f"Failed while fetching Purchase record for ID {purchase_id}: {error_msg}")
                raise PurchaseError(f"Failed while fetching Purchase record for ID {purchase_id}: {error_msg}", status_code=response.status_code)
            return result
    except PurchaseError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching Purchase record for ID {purchase_id}")
        raise PurchaseError("Unexpected error", status_code=500)