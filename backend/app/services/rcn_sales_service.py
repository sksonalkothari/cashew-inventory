from typing import List, Union
from app.dao import rcn_sales_dao
from app.helper.rcn_sales_helper import RcnSalesHelper
from app.utils.logger import logger
from app.exceptions.exceptions import RcnSalesError

async def insert_rcn_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]

    # batch_map = RcnSalesHelper.consolidate_batches(payloads)
    # await RcnSalesHelper.ensure_batches_exist(batch_map, headers)

    res = await rcn_sales_dao.insert_rcn_sales(data, headers)

    # await RcnSalesHelper.update_batch_quantities(batch_map, headers)

    return res

async def update_rcn_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]
    updated = await rcn_sales_dao.update_rcn_sales(data, headers)

    # batch_map = RcnSalesHelper.consolidate_batches(payloads)
    # await RcnSalesHelper.update_batch_quantities(batch_map, headers)

    return updated

async def soft_delete_rcn_sales(data: list[dict], headers: dict):
    #records = data if isinstance(data, list) else [data]
    """ affected = []
    for item in records:
        existing = await rcn_sales_dao.fetch_rcn_sales_by_id(item.get('id'), headers)
        if existing:
            affected.append(existing[0]) """

    deleted = await rcn_sales_dao.delete_rcn_sales(data, headers)

    # batch_map = RcnSalesHelper.consolidate_batches(affected)
    # await RcnSalesHelper.update_batch_quantities(batch_map, headers)

    return deleted

async def fetch_all_rcn_sales(headers: dict):
    return await rcn_sales_dao.fetch_all_rcn_sales(headers)

async def fetch_rcn_sales_by_batch(batch_number: str, headers: dict):
    return await rcn_sales_dao.fetch_all_rcn_sales_by_batch_number(batch_number, headers)

async def fetch_rcn_sales_by_date(date: str, headers: dict):
    return await rcn_sales_dao.fetch_rcn_sales_by_date(date, headers)