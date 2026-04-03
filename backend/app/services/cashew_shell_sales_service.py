from typing import List, Union
from app.dao import cashew_shell_sales_dao
from app.helper.cashew_shell_sales_helper import CashewShellSalesHelper
from app.utils.logger import logger
from app.exceptions.exceptions import CashewShellSalesError

async def insert_cashew_shell_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]

    # batch_map = CashewShellSalesHelper.consolidate_batches(payloads)
    # await CashewShellSalesHelper.ensure_batches_exist(batch_map, headers)

    res = await cashew_shell_sales_dao.insert_cashew_shell_sales(data, headers)

    # await CashewShellSalesHelper.update_batch_quantities(batch_map, headers)

    return res

async def update_cashew_shell_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]
    updated = await cashew_shell_sales_dao.update_cashew_shell_sales(data, headers)

    # batch_map = CashewShellSalesHelper.consolidate_batches(payloads)
    # await CashewShellSalesHelper.update_batch_quantities(batch_map, headers)

    return updated

async def soft_delete_cashew_shell_sales(data: list[dict], headers: dict):
    # records = data if isinstance(data, list) else [data]
    """ affected = []
    for item in records:
        existing = await cashew_shell_sales_dao.fetch_cashew_shell_sale_by_id(item.get('id'), headers)
        if existing:
            affected.append(existing[0]) """

    deleted = await cashew_shell_sales_dao.delete_cashew_shell_sales(data, headers)

    # batch_map = CashewShellSalesHelper.consolidate_batches(affected)
    # await CashewShellSalesHelper.update_batch_quantities(batch_map, headers)

    return deleted

async def fetch_all_cashew_shell_sales(headers: dict):
    return await cashew_shell_sales_dao.fetch_all_cashew_shell_sales(headers)

async def fetch_cashew_shell_sales_by_batch(batch_number: str, headers: dict):
    return await cashew_shell_sales_dao.fetch_all_cashew_shell_sales_by_batch_number(batch_number, headers)

async def fetch_cashew_shell_sales_by_date(date: str, headers: dict):
    return await cashew_shell_sales_dao.fetch_cashew_shell_sales_by_date(date, headers)