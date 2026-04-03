from typing import List, Union
from app.dao import husk_return_dao
from app.helper.husk_return_helper import HuskReturnHelper
from app.utils.logger import logger
from app.exceptions.exceptions import HuskReturnError

async def insert_husk_return(data: list[dict], headers: dict):
    # Consolidate batches and ensure batch_summary rows
    # batch_map = HuskReturnHelper.consolidate_batches(payloads)
    # await HuskReturnHelper.ensure_batches_exist(batch_map, headers)

    # Insert husk_return rows in bulk
    res = await husk_return_dao.insert_husk_return(data, headers)

    # Recalculate and update batch_summary quantities
    # await HuskReturnHelper.update_batch_quantities(batch_map, headers)

    return res

async def update_husk_return(data: list[dict], headers: dict):
    # Use DAO batch update
    updated = await husk_return_dao.update_husk_return(data, headers)

    # After updates, recalc affected batches
    # batch_map = HuskReturnHelper.consolidate_batches(payloads)
    # await HuskReturnHelper.update_batch_quantities(batch_map, headers)

    return updated

async def soft_delete_husk_return(data: list[dict], headers: dict):
    # records = data if isinstance(data, list) else [data]
    """ affected = []
    for item in records:
        existing = await husk_return_dao.fetch_husk_return_by_id(item.get('id'), headers)
        if existing:
            # existing is a list, pick first
            affected.append(existing[0]) """

    deleted = await husk_return_dao.delete_husk_return(data, headers)

    # batch_map = HuskReturnHelper.consolidate_batches(affected)
    # await HuskReturnHelper.update_batch_quantities(batch_map, headers)

    return deleted

async def fetch_all_husk_return(headers: dict):
    return await husk_return_dao.fetch_all_husk_return(headers)

async def fetch_husk_return_by_batch(batch_number: str, headers: dict):
    return await husk_return_dao.fetch_all_husk_return_by_batch_number(batch_number, headers)

async def fetch_husk_return_by_date(date: str, headers: dict):
    return await husk_return_dao.fetch_husk_return_by_date(date, headers)
