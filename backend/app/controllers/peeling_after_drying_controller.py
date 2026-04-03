from typing import Union, List

from fastapi import APIRouter, Depends

from app.models.peeling_after_drying_models import (
    PeelingAfterDryingCreateRequest,
    PeelingAfterDryingUpdateRequest,
    PeelingAfterDryingDeleteRequest,
    PeelingAfterDryingFetchByBatchNumberRequest,
)
from app.services import peeling_after_drying_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger


router = APIRouter(prefix="/peeling_after_drying", tags=["Peeling_after_drying"])


@router.post("/", summary="Insert Peeling after drying", description="Insert new peeling_after_drying record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_peeling_after_drying(
    data: Union[PeelingAfterDryingCreateRequest, List[PeelingAfterDryingCreateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info("Inserting peeling_after_drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "created_by": current_user["id"]}
        for record in records
    ]

    return await peeling_after_drying_service.insert_peeling_after_drying(enriched, current_user["headers"])


@router.patch("/", summary="Update Peeling after drying", description="Update existing peeling_after_drying record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_peeling_after_drying(
    data: Union[PeelingAfterDryingUpdateRequest, List[PeelingAfterDryingUpdateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating peeling_after_drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await peeling_after_drying_service.update_peeling_after_drying(enriched, current_user["headers"])


@router.delete("/", summary="Delete Peeling after drying", description="Soft-delete existing peeling_after_drying record(s)",
             dependencies=[Depends(require_roles(["admin"]))])
async def delete_peeling_after_drying(
    data: Union[PeelingAfterDryingDeleteRequest, List[PeelingAfterDryingDeleteRequest]],
    current_user: dict = Depends(require_roles(["admin"]))
):
    logger.info(f"Soft-deleting peeling_after_drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await peeling_after_drying_service.delete_peeling_after_drying(enriched, current_user["headers"])


@router.get("/all", summary="Get All Peeling after drying", description="Fetch all peeling_after_drying records",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_all_peeling_after_drying(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all peeling_after_drying records")
    return await peeling_after_drying_service.get_all_peeling_after_drying(current_user["headers"])


@router.get("/batch/", summary="Get Peeling after drying Records by Batch Number", description="Fetch all peeling_after_drying records for a specific batch",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_peeling_after_by_batch(
    batch: PeelingAfterDryingFetchByBatchNumberRequest,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching peeling_after_drying records for batch {batch.batch_number}")
    return await peeling_after_drying_service.get_all_peeling_after_drying_by_batch_number(batch.batch_number, current_user["headers"])


@router.get("/by-date", summary="Get Peeling after drying by Date", description="Fetch peeling_after_drying records by date",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_peeling_after_by_date(
    date: str,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching peeling_after_drying records for date: {date}")
    return await peeling_after_drying_service.get_peeling_after_drying_by_date(date, current_user["headers"])
