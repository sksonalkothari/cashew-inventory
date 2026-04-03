from typing import Union, List

from fastapi import APIRouter, Depends

from app.models.boiling_models import (
    BoilingCreateRequest, BoilingUpdateRequest, BoilingDeleteRequest
)
from app.services import boiling_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger


router = APIRouter(prefix="/boiling", tags=["Boiling"])


@router.post("/", summary="Insert Boiling", description="Insert a new boiling record",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_boiling(
    data: Union[BoilingCreateRequest, List[BoilingCreateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info("Inserting Boiling record/s")
    # normalize to list for uniform processing
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "created_by": current_user["id"]}
        for record in records
    ]

    # Delegate batch/single handling to service layer
    return await boiling_service.insert_boiling(enriched, current_user["headers"])


@router.patch("/", summary="Update Boiling", description="Update an existing boiling record",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_boiling(
    data: Union[BoilingUpdateRequest, List[BoilingUpdateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating boiling record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    # Delegate batch/single handling to service layer
    return await boiling_service.update_boiling(enriched, current_user["headers"])


@router.delete("/", summary="Delete Boiling", description="Soft-delete an existing boiling record",
             dependencies=[Depends(require_roles(["admin"]))])
async def delete_boiling(
    data: Union[BoilingDeleteRequest, List[BoilingDeleteRequest]],
    current_user: dict = Depends(require_roles(["admin"]))
):
    logger.info(f"Soft-deleting boiling record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    # Delegate batch/single handling to service layer
    return await boiling_service.delete_boiling(enriched, current_user["headers"])


@router.get("/all", summary="Get All Boiling", description="Fetch all boiling records",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_all_boiling_records(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all boiling records")
    return await boiling_service.get_all_boiling(current_user["headers"]) 

@router.get("/by-date", summary="Get Boiling by Date", description="Fetch boiling records by date",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_boiling_by_date(
    date: str,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching boiling records for date: {date}")
    return await boiling_service.get_boiling_by_date(date, current_user["headers"])