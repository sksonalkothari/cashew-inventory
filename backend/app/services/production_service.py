from typing import List, Union
from app.dao import production_dao
from app.helper.production_helper import ProductionHelper
from app.utils.logger import logger
from app.exceptions.exceptions import ProductionError

async def insert_production(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]

    # batch_map = ProductionHelper.consolidate_batches(payloads)
    # await ProductionHelper.ensure_batches_exist(batch_map, headers)

    res = await production_dao.insert_production(data, headers)

    # await ProductionHelper.update_batch_quantities(batch_map, headers)

    return res


async def update_production(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]
    updated = await production_dao.update_production(data, headers)

    # batch_map = ProductionHelper.consolidate_batches(payloads)
    # await ProductionHelper.update_batch_quantities(batch_map, headers)

    return updated


async def soft_delete_production(data: list[dict], headers: dict):
    # records = data if isinstance(data, list) else [data]
    """ affected = []
    for item in records:
        existing = await production_dao.fetch_production_by_id(item.get('id'), headers)
        if existing:
            affected.append(existing[0]) """

    deleted = await production_dao.delete_production(data, headers)

    # batch_map = ProductionHelper.consolidate_batches(affected)
    # await ProductionHelper.update_batch_quantities(batch_map, headers)

    return deleted


async def fetch_all_production(headers: dict):
    return await production_dao.fetch_all_production(headers)


async def fetch_production_by_batch(batch_number: str, headers: dict):
    return await production_dao.fetch_all_production_by_batch_number(batch_number, headers)


async def fetch_production_by_date(date: str, headers: dict):
    return await production_dao.fetch_production_by_date(date, headers)