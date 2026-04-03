from typing import Union, List

from fastapi import APIRouter, Depends

from app.models.drying_models import (
    DryingCreateRequest, DryingUpdateRequest, DryingDeleteRequest, DryingFetchByBatchNumberRequest
)
from app.services import drying_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger


router = APIRouter(prefix="/drying", tags=["Drying"])


@router.post("/", summary="Insert Drying", description="Insert a new drying record",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_drying(
    data: Union[DryingCreateRequest, List[DryingCreateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info("Inserting Drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "created_by": current_user["id"]}
        for record in records
    ]

    return await drying_service.insert_drying(enriched, current_user["headers"])


@router.patch("/", summary="Update Drying", description="Update an existing drying record",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_drying(
    data: Union[DryingUpdateRequest, List[DryingUpdateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await drying_service.update_drying(enriched, current_user["headers"])


@router.delete("/", summary="Delete Drying", description="Soft-delete an existing drying record",
             dependencies=[Depends(require_roles(["admin"]))])
async def delete_drying(
    data: Union[DryingDeleteRequest, List[DryingDeleteRequest]],
    current_user: dict = Depends(require_roles(["admin"]))
):
    logger.info(f"Soft-deleting drying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await drying_service.delete_drying(enriched, current_user["headers"])


@router.get("/all", summary="Get All Drying", description="Fetch all drying records",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_all_drying_records(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all drying records")
    return await drying_service.get_all_drying(current_user["headers"]) 


@router.get("/batch/", summary="Get Drying Records by Batch Number", description="Fetch all drying records for a specific batch",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_drying_records_by_batch(
    data: DryingFetchByBatchNumberRequest,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching drying records for batch {data.batch_number}")
    return await drying_service.get_all_drying_by_batch_number(data.batch_number, current_user["headers"]) 


@router.get("/by-date", summary="Get Drying by Date", description="Fetch drying records by date",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_drying_by_date(
    date: str,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching drying records for date: {date}")
    return await drying_service.get_boiling_by_date(date, current_user["headers"]) 