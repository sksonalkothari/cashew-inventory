from fastapi import HTTPException, APIRouter, Depends
from app.dependencies.role_dependency import require_roles
from app.services import batch_service
from app.utils.logger import logger
from app.models.batch_models import BatchCreateModel, BatchUpdateModel, InProgressBatchQueryModel

router = APIRouter(prefix="/batch", tags=["Batch"])

@router.get("/all", summary="Get all batches", description="Fetch all batches from batch table (admin, entry_operator, viewer)")
async def get_all_batches(current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info("Fetching all batches from batch table")
    batches = await batch_service.fetch_all_batches(current_user["headers"])
    return batches

@router.post("/", summary="Insert new batch", description="Insert a new batch (admin, entry_operator)")
async def insert_new_batch(
    batch: BatchCreateModel,
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Inserting new batch: {batch.batch_number}")
    enriched_data = {**batch.dict(), "created_by": current_user["id"]}
    result = await batch_service.insert_batch(enriched_data, current_user["headers"])
    return result

@router.post("/inprogress", summary="Get in-progress batches for a stage", description="Fetch batches with given stage IN_PROGRESS (admin, entry_operator, viewer)")
async def get_inprogress_batches_by_stage(
    query: InProgressBatchQueryModel,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching IN_PROGRESS batches for stage: {query.stage}")
    batches = await batch_service.fetch_inprogress_batches_by_stage(query.stage, current_user["headers"])
    return batches


# New endpoint: Update batch by batch number
@router.patch("/", summary="Update batch", description="Update batch details (admin, entry_operator)")
async def update_batch(
    batch: BatchUpdateModel,
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating batch: {batch.batch_number}")
    enriched_data = {**batch.dict(), "updated_by": current_user["id"]}
    result = await batch_service.update_batch(enriched_data, current_user["headers"])
    if not result:
        raise HTTPException(status_code=404, detail="Batch not found or update failed")
    return result