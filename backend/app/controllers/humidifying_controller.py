from typing import Union, List

from fastapi import APIRouter, Depends

from app.models.humidifying_models import (
    HumidifyingCreateRequest, HumidifyingFetchByBatchNumberRequest, HumidifyingUpdateRequest,
    HumidifyingDeleteRequest
)
from app.services import humidifying_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger


router = APIRouter(prefix="/humidifying", tags=["Humidifying"])


@router.post("/", summary="Insert Humidifying", description="Insert new humidifying record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_humidifying(
    data: Union[HumidifyingCreateRequest, List[HumidifyingCreateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info("Inserting humidifying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "created_by": current_user["id"]}
        for record in records
    ]

    return await humidifying_service.insert_humidifying(enriched, current_user["headers"])


@router.patch("/", summary="Update Humidifying", description="Update existing humidifying record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_humidifying(
    data: Union[HumidifyingUpdateRequest, List[HumidifyingUpdateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating humidifying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await humidifying_service.update_humidifying(enriched, current_user["headers"])


@router.delete("/", summary="Delete Humidifying", description="Soft-delete existing humidifying record(s)",
             dependencies=[Depends(require_roles(["admin"]))])
async def delete_humidifying(
    data: Union[HumidifyingDeleteRequest, List[HumidifyingDeleteRequest]],
    current_user: dict = Depends(require_roles(["admin"]))
):
    logger.info(f"Soft-deleting humidifying record/s")
    records = data if isinstance(data, list) else [data]
    enriched = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in records
    ]

    return await humidifying_service.delete_humidifying(enriched, current_user["headers"])


@router.get("/all", summary="Get All Humidifying", description="Fetch all humidifying records",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_all_humidifying(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all humidifying records")
    return await humidifying_service.get_all_humidifying(current_user["headers"])


@router.get("/batch/", summary="Get Humidifying Records by Batch Number", description="Fetch all humidifying records for a specific batch",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_humidifying_by_batch(
    batch: HumidifyingFetchByBatchNumberRequest,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching humidifying records for batch {batch.batch_number}")
    return await humidifying_service.get_all_humidifying_by_batch_number(batch.batch_number, current_user["headers"])


@router.get("/by-date", summary="Get Humidifying by Date", description="Fetch humidifying records by date",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_humidifying_by_date(
    date: str,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching humidifying records for date: {date}")
    return await humidifying_service.get_humidifying_by_date(date, current_user["headers"])