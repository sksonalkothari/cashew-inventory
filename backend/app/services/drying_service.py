from app.dao import drying_dao
from app.utils.logger import logger
from app.helper.drying_helper import DryingHelper


async def insert_drying(data: list[dict], headers: dict = None):
    """Accepts single dict or list of dicts; consolidates batches, ensures batch_summary rows exist, inserts via DAO and updates batch_summary quantities."""
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Inserting drying records for batches {[r.get('batch_number') for r in data]}")

    # consolidate and ensure batch_summary entries
    # batch_map = DryingHelper.consolidate_batches(records)
    # await DryingHelper.ensure_batches_exist(batch_map, headers)

    # perform DAO insert
    response = await drying_dao.insert_drying(data, headers)

    # update batch_summary drying quantities from DB totals
    # await DryingHelper.update_batch_quantities(batch_map, headers)
    return response


async def update_drying(data: list[dict], headers: dict = None):
    """Accepts single dict or list of dicts; ensures batches exist, updates via DAO and refreshes batch_summary drying quantities."""
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Updating drying records for IDs {[r.get('id') for r in data]}")

    # batch_map = DryingHelper.consolidate_batches(records)
    # await DryingHelper.ensure_batches_exist(batch_map, headers)

    updated = await drying_dao.update_drying(data, headers)

    # await DryingHelper.update_batch_quantities(batch_map, headers)
    return updated


async def delete_drying(data: list[dict], headers: dict = None):
    """Accepts single dict or list of dicts (each must contain id and updated_by). Soft-deletes via DAO and updates batch summaries."""
    # records = data if isinstance(data, list) else [data]
    logger.info(f"Soft-deleting drying records IDs {[r.get('id') for r in data]}")

    # determine affected batches
    """ affected_batches = {}
    for item in records:
        existing = await drying_dao.fetch_drying_by_id(item.get('id'), headers)
        if not existing:
            logger.warning(f"No existing drying record found for ID {item.get('id')}")
            continue
        rec = existing[0]
        bn = rec.get('batch_number')
        affected_batches.setdefault(bn, []).append(item) """

    deleted = await drying_dao.delete_drying(data, headers)

    # refresh batch summaries for affected batches
    """ for bn in affected_batches.keys():
        totals = await get_total_drying_quantity_for_batch(bn, headers)
        updater = next((it.get('updated_by') for it in affected_batches[bn] if it.get('updated_by')), None)
        await DryingHelper.update_drying_quantity_for_batch(bn, updater, headers, totals) """

    return deleted


async def get_all_drying(headers: dict = None):
    logger.info("Fetching all drying records")
    return await drying_dao.fetch_all_drying(headers)


async def get_all_drying_by_batch_number(batch_number: str, headers: dict = None):
    logger.info(f"Fetching all drying records for batch {batch_number}")
    return await drying_dao.fetch_all_drying_by_batch_number(batch_number, headers)


async def get_boiling_by_date(date: str, headers: dict = None):
    logger.info(f"Fetching drying records for date: {date}")
    return await drying_dao.fetch_drying_by_date(date, headers)


async def get_total_drying_quantity_for_batch(batch_number: str, headers: dict):
    drying_records = await get_all_drying_by_batch_number(batch_number, headers)
    drying_quantities = dict()
    drying_quantities['total_nw_wholes_in_quantity'] = sum(float(record.get('nw_wholes_in_kg', 0) or 0) for record in drying_records)
    drying_quantities['total_nw_pieces_in_quantity'] = sum(float(record.get('nw_pieces_in_kg', 0) or 0) for record in drying_records)
    drying_quantities['total_nw_rejection_in_quantity'] = sum(float(record.get('nw_rejection_in_kg', 0) or 0) for record in drying_records)
    drying_quantities['total_nw_wholes_out_quantity'] = sum(float(record.get('nw_wholes_out_kg', 0) or 0) for record in drying_records)
    drying_quantities['total_nw_pieces_out_quantity'] = sum(float(record.get('nw_pieces_out_kg', 0) or 0) for record in drying_records)
    drying_quantities['total_nw_rejection_out_quantity'] = sum(float(record.get('nw_rejection_out_kg', 0) or 0) for record in drying_records)
    return drying_quantities
