from app.dao import batch_dao

async def fetch_inprogress_batches_by_stage(stage: str, headers: dict):
    return await batch_dao.fetch_inprogress_batches_by_stage(stage, headers)

async def fetch_inprogress_batches(headers: dict):
    return await batch_dao.fetch_inprogress_batches(headers)

async def fetch_all_batches(headers: dict):
    # Add any business logic here if needed
    return await batch_dao.fetch_all_batches(headers)

async def insert_batch(data: dict, headers: dict):
    return await batch_dao.insert_batch(data, headers)

async def update_batch(data: dict, headers: dict):
    return await batch_dao.update_batch(data, headers)
