from typing import List, Union
from fastapi import APIRouter, Depends
from app.models.husk_rejection_sales_models import (
    HuskRejectionSalesCreateRequest as HuskRejectionSalesCreate,
    HuskRejectionSalesUpdateRequest as HuskRejectionSalesUpdate,
    HuskRejectionSalesDeleteRequest as HuskRejectionSalesDelete,
)
from app.services import husk_rejection_sales_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger

router = APIRouter(prefix="/husk_rejection_sales", tags=["Husk_rejection_sales"])


@router.post("/", summary="Insert husk rejection sales records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_husk_rejection_sales(payload: Union[HuskRejectionSalesCreate, List[HuskRejectionSalesCreate]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Inserting husk rejection sales record(s)")
    records = payload if isinstance(payload, list) else [payload]
    enriched = [{**rec.model_dump(), "created_by": current_user["id"]} for rec in records]
    return await husk_rejection_sales_service.insert_husk_rejection_sales(enriched, current_user["headers"])


@router.patch("/", summary="Update husk rejection sales records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_husk_rejection_sales(payload: Union[HuskRejectionSalesUpdate, List[HuskRejectionSalesUpdate]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Updating husk rejection sales record(s)")
    records = payload if isinstance(payload, list) else [payload]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await husk_rejection_sales_service.update_husk_rejection_sales(enriched, current_user["headers"])


@router.delete("/", summary="Soft delete husk rejection sales records", dependencies=[Depends(require_roles(["admin"]))])
async def delete_husk_rejection_sales(payload: Union[HuskRejectionSalesDelete, List[HuskRejectionSalesDelete]], current_user: dict = Depends(require_roles(["admin"]))):
    logger.info("Soft-deleting husk rejection sales record(s)")
    records = payload if isinstance(payload, list) else [payload]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await husk_rejection_sales_service.soft_delete_husk_rejection_sales(enriched, current_user["headers"])


@router.get("/all", status_code=200)
async def get_all_husk_rejection_sales(current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info("Fetching all husk rejection sales records")
    return await husk_rejection_sales_service.fetch_all_husk_rejection_sales(current_user["headers"])


@router.get("/batch", status_code=200)
async def get_husk_rejection_sales_by_batch(batch_number: str, current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info(f"Fetching husk rejection sales records for batch: {batch_number}")
    return await husk_rejection_sales_service.fetch_husk_rejection_sales_by_batch(batch_number, current_user["headers"])


@router.get("/by-date", status_code=200)
async def get_husk_rejection_sales_by_date(date: str, current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info(f"Fetching husk rejection sales records for date: {date}")
    return await husk_rejection_sales_service.fetch_husk_rejection_sales_by_date(date, current_user["headers"])
