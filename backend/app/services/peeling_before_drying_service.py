from app.dao import peeling_before_drying_dao
from app.utils.logger import logger
from app.helper.peeling_before_drying_helper import PeelingBeforeDryingHelper


async def insert_peeling_before_drying(data: list[dict], headers: dict = None):
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Inserting peeling_before_drying records for batches {[r.get('batch_number') for r in data]}")

    # batch_map = PeelingBeforeDryingHelper.consolidate_batches(records)
    # await PeelingBeforeDryingHelper.ensure_batches_exist(batch_map, headers)

    response = await peeling_before_drying_dao.insert_peeling_before_drying(data, headers)

    # await PeelingBeforeDryingHelper.update_batch_quantities(batch_map, headers)
    return response


async def update_peeling_before_drying(data: list[dict], headers: dict = None):
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Updating peeling_before_drying records for IDs {[r.get('id') for r in data]}")

    # batch_map = PeelingBeforeDryingHelper.consolidate_batches(records)
    # await PeelingBeforeDryingHelper.ensure_batches_exist(batch_map, headers)

    updated = await peeling_before_drying_dao.update_peeling_before_drying(data, headers)

    # await PeelingBeforeDryingHelper.update_batch_quantities(batch_map, headers)
    return updated


async def delete_peeling_before_drying(data: list[dict], headers: dict = None):
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Soft-deleting peeling_before_drying records IDs {[r.get('id') for r in data]}")

    """ affected_batches = {}
    for item in records:
        existing = await peeling_before_drying_dao.fetch_peeling_before_drying_by_id(item.get('id'), headers)
        if not existing:
            logger.warning(f"No existing peeling_before_drying record found for ID {item.get('id')}")
            continue
        rec = existing[0]
        bn = rec.get('batch_number')
        affected_batches.setdefault(bn, []).append(item) """

    deleted = await peeling_before_drying_dao.delete_peeling_before_drying(data, headers)

    """ for bn, items in affected_batches.items():
        totals = await get_total_peeling_before_drying_quantity_for_batch(bn, headers)
        updater = next((it.get('updated_by') for it in items if it.get('updated_by')), None)
        await PeelingBeforeDryingHelper.update_peeling_quantity_for_batch(bn, updater, headers, totals)
 """
    return deleted


async def get_all_peeling_before_drying(headers: dict = None):
    logger.info("Fetching all peeling_before_drying records")
    return await peeling_before_drying_dao.fetch_all_peeling_before_drying(headers)


async def get_all_peeling_before_drying_by_batch_number(batch_number: str, headers: dict = None):
    logger.info(f"Fetching all peeling_before_drying records for batch {batch_number}")
    return await peeling_before_drying_dao.fetch_all_peeling_before_drying_by_batch_number(batch_number, headers)


async def get_peeling_before_drying_by_date(date: str, headers: dict = None):
    logger.info(f"Fetching peeling_before_drying records for date: {date}")
    return await peeling_before_drying_dao.fetch_peeling_before_drying_by_date(date, headers)


async def get_total_peeling_before_drying_quantity_for_batch(batch_number: str, headers: dict):
    peeling_records = await get_all_peeling_before_drying_by_batch_number(batch_number, headers)
    total_peeling_quantity = dict()
    total_peeling_quantity['total_wholes_kg'] = sum(float(record.get('wholes_kg', 0) or 0) for record in peeling_records)
    total_peeling_quantity['total_pieces_kg'] = sum(float(record.get('pieces_kg', 0) or 0) for record in peeling_records)
    total_peeling_quantity['total_unpeeled_kg'] = sum(float(record.get('unpeeled_kg', 0) or 0) for record in peeling_records)
    total_peeling_quantity['total_swp_kg'] = sum(float(record.get('swp_kg', 0) or 0) for record in peeling_records)
    total_peeling_quantity['total_bb_kg'] = sum(float(record.get('bb_kg', 0) or 0) for record in peeling_records)
    total_peeling_quantity['total_rejection_kg'] = sum(float(record.get('rejection_kg', 0) or 0) for record in peeling_records)
    total_peeling_quantity['total_husk_kg'] = sum(float(record.get('husk_kg', 0) or 0) for record in peeling_records)
    return total_peeling_quantity
