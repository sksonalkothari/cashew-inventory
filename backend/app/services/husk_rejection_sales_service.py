from typing import List, Union
from app.dao import husk_rejection_sales_dao
from app.helper.husk_rejection_sales_helper import HuskRejectionSalesHelper
from app.utils.logger import logger
from app.exceptions.exceptions import HuskRejectionSalesError

async def insert_husk_rejection_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]

    # batch_map = HuskRejectionSalesHelper.consolidate_batches(payloads)
    # await HuskRejectionSalesHelper.ensure_batches_exist(batch_map, headers)

    res = await husk_rejection_sales_dao.insert_husk_rejection_sales(data, headers)

    # await HuskRejectionSalesHelper.update_batch_quantities(batch_map, headers)

    return res

async def update_husk_rejection_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]
    updated = await husk_rejection_sales_dao.update_husk_rejection_sales(data, headers)

    # batch_map = HuskRejectionSalesHelper.consolidate_batches(payloads)
    # await HuskRejectionSalesHelper.update_batch_quantities(batch_map, headers)

    return updated

async def soft_delete_husk_rejection_sales(data: list[dict], headers: dict):
    # records = data if isinstance(data, list) else [data]
    """ affected = []
    for item in records:
        existing = await husk_rejection_sales_dao.fetch_husk_rejection_sales_by_id(item.get('id'), headers)
        if existing:
            affected.append(existing[0]) """

    deleted = await husk_rejection_sales_dao.delete_husk_rejection_sales(data, headers)

    # batch_map = HuskRejectionSalesHelper.consolidate_batches(affected)
    # await HuskRejectionSalesHelper.update_batch_quantities(batch_map, headers)

    return deleted

async def fetch_all_husk_rejection_sales(headers: dict):
    return await husk_rejection_sales_dao.fetch_all_husk_rejection_sales(headers)

async def fetch_husk_rejection_sales_by_batch(batch_number: str, headers: dict):
    return await husk_rejection_sales_dao.fetch_all_husk_rejection_sales_by_batch_number(batch_number, headers)

async def fetch_husk_rejection_sales_by_date(date: str, headers: dict):
    return await husk_rejection_sales_dao.fetch_husk_rejection_sales_by_date(date, headers)
