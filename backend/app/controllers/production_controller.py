from typing import List, Union
from fastapi import APIRouter, Depends
from app.models.production_models import (
    ProductionCreateRequest,
    ProductionUpdateRequest,
    ProductionDeleteRequest,
    ProductionFetchByBatchNumberRequest,
)
from app.services import production_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger


router = APIRouter(prefix="/production", tags=["Production"])


@router.post("/", summary="Insert production records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def insert_production(data: Union[ProductionCreateRequest, List[ProductionCreateRequest]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Inserting production record(s)")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "created_by": current_user["id"]} for rec in records]
    return await production_service.insert_production(enriched, current_user["headers"])


@router.patch("/", summary="Update production records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_production(data: Union[ProductionUpdateRequest, List[ProductionUpdateRequest]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Updating production record(s)")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await production_service.update_production(enriched, current_user["headers"])


@router.delete("/", summary="Soft delete production records", dependencies=[Depends(require_roles(["admin"]))])
async def soft_delete_production(data: Union[ProductionDeleteRequest, List[ProductionDeleteRequest]], current_user: dict = Depends(require_roles(["admin"]))):
    logger.info("Soft-deleting production record(s)")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await production_service.soft_delete_production(enriched, current_user["headers"])


@router.get("/all", summary="Fetch all production records", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_all_production(current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info("Fetching all production records")
    return await production_service.fetch_all_production(current_user["headers"])


@router.get("/batch", summary="Fetch production records by batch", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_production_by_batch(
    batch_number: str, 
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
    ):
    logger.info(f"Fetching production records for batch: {batch_number}")
    return await production_service.fetch_production_by_batch(batch_number, current_user["headers"])


@router.get("/by-date", summary="Fetch production records by date", 
            dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_production_by_date(
    date: str, current_user: 
    dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
    ):
    logger.info(f"Fetching production records for date: {date}")
    return await production_service.fetch_production_by_date(date, current_user["headers"])
