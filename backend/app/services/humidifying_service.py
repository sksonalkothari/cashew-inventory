from app.dao import humidifying_dao
from app.utils.logger import logger
from app.helper.humidifying_helper import HumidifyingHelper


async def insert_humidifying(data: list[dict], headers: dict = None):
    """Accepts single dict or list; consolidates batches, ensures batch_summary rows exist, inserts via DAO and updates batch_summary."""
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Inserting humidifying records for batches {[r.get('batch_number') for r in data]}")

    # batch_map = HumidifyingHelper.consolidate_batches(records)
    # await HumidifyingHelper.ensure_batches_exist(batch_map, headers)

    response = await humidifying_dao.insert_humidifying(data, headers)

    # await HumidifyingHelper.update_batch_quantities(batch_map, headers)
    return response


async def update_humidifying(data: list[dict], headers: dict = None):
    #records = data if isinstance(data, list) else [data]
    logger.info(f"Updating humidifying records for IDs {[r.get('id') for r in data]}")

    # batch_map = HumidifyingHelper.consolidate_batches(records)
    # await HumidifyingHelper.ensure_batches_exist(batch_map, headers)

    updated = await humidifying_dao.update_humidifying(data, headers)

    # await HumidifyingHelper.update_batch_quantities(batch_map, headers)
    return updated


async def delete_humidifying(data: list[dict], headers: dict = None):
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Soft-deleting humidifying records IDs {[r.get('id') for r in data]}")

    """ affected_batches = {}
    for item in records:
        existing = await humidifying_dao.fetch_humidifying_by_id(item.get('id'), headers)
        if not existing:
            logger.warning(f"No existing humidifying record found for ID {item.get('id')}")
            continue
        rec = existing[0]
        bn = rec.get('batch_number')
        affected_batches.setdefault(bn, []).append(item) """

    deleted = await humidifying_dao.delete_humidifying(data, headers)

    """ for bn, items in affected_batches.items():
        totals = await get_total_humidifying_quantity_for_batch(bn, headers)
        updater = next((it.get('updated_by') for it in items if it.get('updated_by')), None)
        await HumidifyingHelper.update_humidifying_quantity_for_batch(bn, updater, headers, totals) """

    return deleted


async def get_all_humidifying(headers: dict = None):
    logger.info("Fetching all humidifying records")
    return await humidifying_dao.fetch_all_humidifying(headers)


async def get_all_humidifying_by_batch_number(batch_number: str, headers: dict = None):
    logger.info(f"Fetching all humidifying records for batch {batch_number}")
    return await humidifying_dao.fetch_all_humidifying_by_batch_number(batch_number, headers)


async def get_humidifying_by_date(date: str, headers: dict = None):
    logger.info(f"Fetching humidifying records for date: {date}")
    return await humidifying_dao.fetch_humidifying_by_date(date, headers)


async def get_total_humidifying_quantity_for_batch(batch_number: str, headers: dict):
    humidifying_records = await get_all_humidifying_by_batch_number(batch_number, headers)
    total_humidifying_quantity = dict()
    total_humidifying_quantity['total_nw_wholes_in_kg'] = sum(float(record.get('nw_wholes_in_kg', 0) or 0) for record in humidifying_records)
    total_humidifying_quantity['total_nw_pieces_in_kg'] = sum(float(record.get('nw_pieces_in_kg', 0) or 0) for record in humidifying_records)
    total_humidifying_quantity['total_nw_rejection_in_kg'] = sum(float(record.get('nw_rejection_in_kg', 0) or 0) for record in humidifying_records)
    total_humidifying_quantity['total_nw_wholes_out_kg'] = sum(float(record.get('nw_wholes_out_kg', 0) or 0) for record in humidifying_records)
    total_humidifying_quantity['total_nw_pieces_out_kg'] = sum(float(record.get('nw_pieces_out_kg', 0) or 0) for record in humidifying_records)
    total_humidifying_quantity['total_nw_rejection_out_kg'] = sum(float(record.get('nw_rejection_out_kg', 0) or 0) for record in humidifying_records)
    return total_humidifying_quantity