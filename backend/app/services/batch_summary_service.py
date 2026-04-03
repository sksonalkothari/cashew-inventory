from app.dao import batch_summary_dao
from app.utils.logger import logger

async def insert_batch(data: list[dict], headers: dict):
    logger.info(f"Inserting batches {[item['batch_number'] for item in data]}")
    return await batch_summary_dao.insert_batch(data, headers)

async def update_batch(data: dict, headers: dict):
    logger.info(f"Updating batch {data['batch_number']}")
    return await batch_summary_dao.update_batch(data, headers)

async def soft_delete_batch(data: dict, headers: dict):
    logger.info(f"Soft deleting batch {data['batch_number']}")
    return await batch_summary_dao.soft_delete_batch(data, headers)

async def fetch_all_batches(headers: dict):
    logger.info("Fetching all batches")
    return await batch_summary_dao.fetch_all_batches(headers)

async def fetch_unsold_batches(headers: dict):
    logger.info("Fetching unsold batches")
    return await batch_summary_dao.fetch_unsold_batches(headers)

async def fetch_batch_by_number(batch_number: str, headers: dict):
    logger.info(f"Fetching batch {batch_number}")
    return await batch_summary_dao.fetch_batch_by_number(batch_number, headers)

async def fetch_batch_by_number_and_origin(batch_number: str, origin: str,  headers: dict):
    logger.info(f"Fetching batch ({batch_number}, {origin})")
    return await batch_summary_dao.fetch_batch_by_number_and_origin(batch_number, origin, headers)
