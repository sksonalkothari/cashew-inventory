from time import perf_counter
from app.helper.purchase_helper import PurchaseHelper
from app.dao import purchase_dao
from app.utils.logger import logger

async def insert_purchase(data: list[dict], headers: dict):
    logger.info(f"Starting purchase insert for bills: {[item['bill_number'] for item in data]}")

    start = perf_counter()

    # Step 1: Consolidate batch quantities
    # batch_map = PurchaseHelper.consolidate_batches(data)

    # Step 2: Ensure batch_summary entries exist
    # await PurchaseHelper.ensure_batches_exist(batch_map, headers)

    # Step 3: Insert purchase records
    logger.info("Inserting purchase records...")
    response = await purchase_dao.insert_purchase(data, headers)
    logger.info("Purchase records inserted successfully.")

    # Step 4: Update batch_summary quantities
    # await PurchaseHelper.update_batch_quantities(batch_map, headers)

    end = perf_counter() 

    # Step 5: Return response
    logger.info(f"Purchase flow completed successfully in {end - start:.4f} seconds.")
    return response

""" async def update_purchase(data: list[dict], headers: dict):
    logger.info(f"Starting purchase update for bills: {[item['bill_number'] for item in data]}")
    updated_records = []

    start = perf_counter()

    for item in data:
        purchase_id = item["id"]
    
        existing = await purchase_dao.fetch_purchase_by_id(purchase_id, headers)
        if not existing:
            logger.warning(f"No existing purchase found for ID {purchase_id}")
            continue

        old = existing[0]
        await PurchaseHelper.handle_batch_adjustments(old, item, item["updated_by"], headers)
        
        updated = await purchase_dao.update_purchase([item], headers)
        updated_records.extend(updated if isinstance(updated, list) else [updated])

    end = perf_counter() 
    logger.info(f"Purchase update flow completed in {end - start:.4f} seconds.")
    return updated_records """

async def update_purchase(data: list[dict], headers: dict):
    logger.info(f"Starting purchase update for bills: {[item['bill_number'] for item in data]}")
    # payloads = data if isinstance(data, list) else [data]
    updated = await purchase_dao.update_purchase(data, headers)
    return updated

""" async def soft_delete_purchase(data: list[dict], headers: dict):
    logger.info(f"Starting soft-delete for purchase IDs: {[d['id'] for d in data]}")
    deleted_records = []

    start = perf_counter()

    for item in data:
        purchase_id = item["id"]

        # Fetch existing purchase
        existing = await fetch_purchase_by_id(purchase_id, headers)
        if not existing:
            logger.warning(f"No purchase found for ID {purchase_id}")
            continue

        purchase = existing[0]
        batch_number = purchase["batch_number"]
        qty = float(purchase["quantity_kg"])

        # Soft-delete purchase
        await purchase_dao.soft_delete_purchase([item], headers)
        deleted_records.append(purchase)

        # Adjust batch_summary
        await PurchaseHelper.adjust_batch_summary_after_removal(batch_number, qty, item["updated_by"], headers)

    end = perf_counter()
    logger.info(f"Soft-delete for purchase completed in {end - start:.4f} seconds.")    
    return deleted_records """

async def soft_delete_purchase(data: list[dict], headers: dict):
    logger.info(f"Starting soft-delete for purchase IDs: {[d['id'] for d in data]}")
    # records = data if isinstance(data, list) else [data]
    deleted = await purchase_dao.soft_delete_purchase(data, headers)
    logger.info(f"Soft-delete for purchase completed.")   
    return deleted

async def fetch_all_purchases(headers: dict):
    logger.info("Fetching all purchase records")
    return await purchase_dao.fetch_all_purchases(headers)

async def fetch_purchases_by_date(date: str, headers: dict):
    logger.info(f"Fetching purchase records for date: {date}")
    start = perf_counter()
    result = await purchase_dao.fetch_purchases_by_date(date, headers)
    end = perf_counter()
    logger.info(f"Fetching purchase records for date: {date} completed in {end - start:.4f} seconds.")
    return result

async def fetch_purchase_by_id(purchase_id: str, headers: dict):
    logger.info(f"Fetching purchase record for ID: {purchase_id}")
    return await purchase_dao.fetch_purchase_by_id(purchase_id, headers)