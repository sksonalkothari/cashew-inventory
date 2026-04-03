from app.dao import boiling_dao
from app.utils.logger import logger
from app.helper.boiling_helper import BoilingHelper


async def insert_boiling(data: list[dict], headers: dict = None):
    """Accepts either a single dict or a list of dicts. Delegates DAO insert and updates batch summaries per batch."""
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Inserting boiling records for batches {[r.get('batch_number') for r in data]}")

    # consolidate and ensure batches exist
    # batch_map = BoilingHelper.consolidate_batches(records)
    # await BoilingHelper.ensure_batches_exist(batch_map, headers)

    # insert via DAO (DAO expects list)
    response = await boiling_dao.insert_boiling(data, headers)

    # update batch summary quantities using helper (calculates totals from DB)
    # await BoilingHelper.update_batch_quantities(batch_map, headers)

    return response


async def update_boiling(data: list[dict], headers: dict = None):
    """Accepts single dict or list of dicts, updates via DAO and refreshes batch summaries."""
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Updating boiling records for IDs {[r.get('id') for r in data]}")

    # ensure batches exist for any new batch_numbers being used in updates
    # batch_map = BoilingHelper.consolidate_batches(records)
    # await BoilingHelper.ensure_batches_exist(batch_map, headers)

    updated = await boiling_dao.update_boiling(data, headers)

    # refresh batch summaries for affected consolidated batches using helper
    # await BoilingHelper.update_batch_quantities(batch_map, headers)

    return updated


async def delete_boiling(data: list[dict], headers: dict = None):
    """Accepts single dict or list of dicts (each must contain id and updated_by). Soft-deletes via DAO and updates batch summaries."""
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Soft-deleting boiling records IDs {[r.get('id') for r in data]}")

    # fetch existing records to determine affected batches
    """ affected_batches = {}
    for item in records:
        existing = await boiling_dao.fetch_boiling_by_id(item.get('id'), headers)
        if not existing:
            logger.warning(f"No existing boiling record found for ID {item.get('id')}")
            continue
        rec = existing[0]
        bn = rec.get('batch_number')
        affected_batches.setdefault(bn, []).append(item) """

    # perform soft-delete
    deleted = await boiling_dao.delete_boiling(data, headers)

    # update batch summaries for affected batches
    """ for bn, items in affected_batches.items():
        total_quantity = await get_total_boiling_quantity_for_batch(bn, headers)
        # pick an updater from the delete request items
        updater = next((it.get('updated_by') for it in items if it.get('updated_by')), None)
        await BoilingHelper.update_boiling_quantity_for_batch(bn, updater, headers, total_quantity)
 """
    return deleted


async def get_all_boiling(headers: dict = None):
    logger.info("Fetching all boiling records")
    return await boiling_dao.fetch_all_boiling(headers)


async def get_all_boiling_by_batch_number(batch_number: str, headers: dict = None):
    logger.info(f"Fetching all boiling records for batch {batch_number}")
    return await boiling_dao.fetch_all_boilings_by_batch_number(batch_number, headers)

async def get_boiling_by_date(date: str, headers: dict = None):
    logger.info(f"Fetching boiling records for date: {date}")
    return await boiling_dao.fetch_boiling_by_date(date, headers)

async def get_total_boiling_quantity_for_batch(batch_number: str, headers: dict):
    boiling_records = await get_all_boiling_by_batch_number(batch_number, headers)
    total_quantity = sum(record.get('quantity_kg', 0) for record in boiling_records)
    return total_quantity

async def get_entry_dates(headers: dict = None):
    return await boiling_dao.get_distinct_dates()
