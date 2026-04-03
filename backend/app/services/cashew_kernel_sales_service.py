from typing import List, Union
from app.dao import cashew_kernel_sales_dao
from app.helper.cashew_kernel_sales_helper import CashewKernelSalesHelper
from app.utils.logger import logger
from app.exceptions.exceptions import CashewKernelSalesError


async def insert_cashew_kernel_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]

    # batch_map = CashewKernelSalesHelper.consolidate_batches(payloads)
    # await CashewKernelSalesHelper.ensure_batches_exist(batch_map, headers)

    res = await cashew_kernel_sales_dao.insert_cashew_kernel_sales(data, headers)

    # await CashewKernelSalesHelper.update_batch_quantities(batch_map, headers)

    return res

async def update_cashew_kernel_sales(data: list[dict], headers: dict):
    # payloads = data if isinstance(data, list) else [data]
    updated = await cashew_kernel_sales_dao.update_cashew_kernel_sales(data, headers)

    #batch_map = CashewKernelSalesHelper.consolidate_batches(payloads)
    #await CashewKernelSalesHelper.update_batch_quantities(batch_map, headers)

    return updated

async def soft_delete_cashew_kernel_sales(data: list[dict], headers: dict):
    # records = data if isinstance(data, list) else [data]
    """ affected = []
    for item in records:
        existing = await cashew_kernel_sales_dao.fetch_cashew_kernel_sale_by_id(item.get('id'), headers)
        if existing:
            affected.append(existing[0]) """

    deleted = await cashew_kernel_sales_dao.delete_cashew_kernel_sales(data, headers)

    # batch_map = CashewKernelSalesHelper.consolidate_batches(affected)
    # await CashewKernelSalesHelper.update_batch_quantities(batch_map, headers)

    return deleted

async def fetch_all_cashew_kernel_sales(headers: dict):
    return await cashew_kernel_sales_dao.fetch_all_cashew_kernel_sales(headers)

async def fetch_cashew_kernel_sales_by_batch(batch_number: str, headers: dict):
    return await cashew_kernel_sales_dao.fetch_all_cashew_kernel_sales_by_batch_number(batch_number, headers)

async def fetch_cashew_kernel_sales_by_date(date: str, headers: dict):
    return await cashew_kernel_sales_dao.fetch_cashew_kernel_sales_by_date(date, headers)
