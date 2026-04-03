from typing import Union, List

from fastapi import APIRouter, Depends

from app.models.peeling_before_drying_models import (
    PeelingBeforeDryingCreateRequest,
    PeelingBeforeDryingUpdateRequest,
    PeelingBeforeDryingDeleteRequest,
    PeelingBeforeDryingFetchByBatchNumberRequest,
)
from app.services import peeling_before_drying_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger


router = APIRouter(prefix="/peeling_before_drying", tags=["Peeling_before_drying"])


@router.post("/", summary="Insert Peeling before drying", description="Insert new peeling_before_drying record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_peeling_before_drying(
    data: Union[PeelingBeforeDryingCreateRequest, List[PeelingBeforeDryingCreateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info("Inserting peeling_before_drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "created_by": current_user["id"]}
        for record in records
    ]

    return await peeling_before_drying_service.insert_peeling_before_drying(enriched, current_user["headers"])


@router.patch("/", summary="Update Peeling before drying", description="Update existing peeling_before_drying record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_peeling_before_drying(
    data: Union[PeelingBeforeDryingUpdateRequest, List[PeelingBeforeDryingUpdateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating peeling_before_drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await peeling_before_drying_service.update_peeling_before_drying(enriched, current_user["headers"])


@router.delete("/", summary="Delete Peeling before drying", description="Soft-delete existing peeling_before_drying record(s)",
             dependencies=[Depends(require_roles(["admin"]))])
async def delete_peeling_before_drying(
    data: Union[PeelingBeforeDryingDeleteRequest, List[PeelingBeforeDryingDeleteRequest]],
    current_user: dict = Depends(require_roles(["admin"]))
):
    logger.info(f"Soft-deleting peeling_before_drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await peeling_before_drying_service.delete_peeling_before_drying(enriched, current_user["headers"])


@router.get("/all", summary="Get All Peeling before drying", description="Fetch all peeling_before_drying records",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_all_peeling_before_drying(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all peeling_before_drying records")
    return await peeling_before_drying_service.get_all_peeling_before_drying(current_user["headers"])


@router.get("/batch/", summary="Get Peeling before drying Records by Batch Number", description="Fetch all peeling_before_drying records for a specific batch",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_peeling_by_batch(
    batch: PeelingBeforeDryingFetchByBatchNumberRequest,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching peeling_before_drying records for batch {batch.batch_number}")
    return await peeling_before_drying_service.get_all_peeling_before_drying_by_batch_number(batch.batch_number, current_user["headers"])


@router.get("/by-date", summary="Get Peeling before drying by Date", description="Fetch peeling_before_drying records by date",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_peeling_by_date(
    date: str,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching peeling_before_drying records for date: {date}")
    return await peeling_before_drying_service.get_peeling_before_drying_by_date(date, current_user["headers"])