from fastapi import APIRouter, Depends
from app.decorators.inject_headers import inject_headers
from app.dependencies.role_dependency import require_roles
from app.services import batch_summary_service
from app.utils.logger import logger
from app.utils.response_wrapper import wrap_response

router = APIRouter(prefix="/batch", tags=["Batch Summary"])

@router.get("/all", summary="Get all batches", description="Fetch all batches (admin, entry_operator, viewer)" )
async def get_all_batches(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all batches")
    return wrap_response(await batch_summary_service.fetch_all_batches(current_user["headers"]))

@router.get("/unsold", summary="Get unsold batches", description="Fetch unsold batches (admin, entry_operator, viewer)")
@inject_headers
async def get_unsold_batches(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching unsold batches")
    return wrap_response(await batch_summary_service.fetch_unsold_batches(current_user["headers"]))