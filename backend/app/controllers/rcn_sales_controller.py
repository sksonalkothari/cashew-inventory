from typing import List, Union
from fastapi import APIRouter, Depends
from app.models.rcn_sales_models import (
    RcnSalesCreateRequest,
    RcnSalesUpdateRequest,
    RcnSalesDeleteRequest,
)
from app.services import rcn_sales_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger

router = APIRouter(prefix="/rcn_sales", tags=["RCN_sales"])

@router.post("/", summary="Insert RCN sales records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def insert_rcn_sales(data: Union[RcnSalesCreateRequest, List[RcnSalesCreateRequest]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Inserting rcn_sales record(s)")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "created_by": current_user["id"]} for rec in records]
    return await rcn_sales_service.insert_rcn_sales(enriched, current_user["headers"])

@router.patch("/", summary="Update rcn sales records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_rcn_sales(data: Union[RcnSalesUpdateRequest, List[RcnSalesUpdateRequest]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Updating rcn_sales record(s)")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await rcn_sales_service.update_rcn_sales(enriched, current_user["headers"])

@router.delete("/", summary="Soft delete rcn sales records", dependencies=[Depends(require_roles(["admin"]))])
async def soft_delete_rcn_sales(data: Union[RcnSalesDeleteRequest, List[RcnSalesDeleteRequest]], current_user: dict = Depends(require_roles(["admin"]))):
    logger.info("Soft-deleting rcn_sales record(s)")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await rcn_sales_service.soft_delete_rcn_sales(enriched, current_user["headers"])

@router.get("/all", summary="Fetch all rcn_sales records", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_all_rcn_sales(current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info("Fetching all rcn_sales records")
    return await rcn_sales_service.fetch_all_rcn_sales(current_user["headers"])

@router.get("/batch", summary="Fetch rcn_sales records by batch", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_rcn_sales_by_batch(batch_number: str, current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info(f"Fetching rcn_sales records for batch: {batch_number}")
    return await rcn_sales_service.fetch_rcn_sales_by_batch(batch_number, current_user["headers"])

@router.get("/by-date", summary="Fetch rcn_sales records by date", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_rcn_sales_by_date(date: str, current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info(f"Fetching rcn_sales records for date: {date}")
    return await rcn_sales_service.fetch_rcn_sales_by_date(date, current_user["headers"])