from typing import List, Union
from fastapi import APIRouter, Depends
from app.models.cashew_kernel_sales_models import (
    CashewKernelSalesCreateRequest as CashewKernelSalesCreate,
    CashewKernelSalesUpdateRequest as CashewKernelSalesUpdate,
    CashewKernelSalesDeleteRequest as CashewKernelSalesDelete,
)
from app.services import cashew_kernel_sales_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger

router = APIRouter(prefix="/cashew_kernel_sales", tags=["Cashew_kernel_sales"])


@router.post("/", summary="Insert cashew kernel sales records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_cashew_kernel_sales(payload: Union[CashewKernelSalesCreate, List[CashewKernelSalesCreate]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Inserting cashew kernel sales record(s)")
    records = payload if isinstance(payload, list) else [payload]
    enriched = [{**rec.model_dump(), "created_by": current_user["id"]} for rec in records]
    return await cashew_kernel_sales_service.insert_cashew_kernel_sales(enriched, current_user["headers"])


@router.patch("/", summary="Update cashew kernel sales records", dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_cashew_kernel_sales(payload: Union[CashewKernelSalesUpdate, List[CashewKernelSalesUpdate]], current_user: dict = Depends(require_roles(["admin", "entry_operator"]))):
    logger.info("Updating cashew kernel sales record(s)")
    records = payload if isinstance(payload, list) else [payload]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await cashew_kernel_sales_service.update_cashew_kernel_sales(enriched, current_user["headers"])


@router.delete("/", summary="Soft delete cashew kernel sales records", dependencies=[Depends(require_roles(["admin"]))])
async def delete_cashew_kernel_sales(payload: Union[CashewKernelSalesDelete, List[CashewKernelSalesDelete]], current_user: dict = Depends(require_roles(["admin"]))):
    logger.info("Soft-deleting cashew kernel sales record(s)")
    records = payload if isinstance(payload, list) else [payload]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    return await cashew_kernel_sales_service.soft_delete_cashew_kernel_sales(enriched, current_user["headers"])


@router.get("/all", summary="Fetch all cashew kernel sales records", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_all_cashew_kernel_sales(current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info("Fetching all cashew kernel sales records")
    return await cashew_kernel_sales_service.fetch_all_cashew_kernel_sales(current_user["headers"])


@router.get("/batch", summary="Fetch cashew kernel sales records by batch", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_cashew_kernel_sales_by_batch(batch_number: str, current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info(f"Fetching cashew kernel sales records for batch: {batch_number}")
    return await cashew_kernel_sales_service.fetch_cashew_kernel_sales_by_batch(batch_number, current_user["headers"])


@router.get("/by-date", summary="Fetch cashew kernel sales records by date", dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_cashew_kernel_sales_by_date(date: str, current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    logger.info(f"Fetching cashew kernel sales records for date: {date}")
    return await cashew_kernel_sales_service.fetch_cashew_kernel_sales_by_date(date, current_user["headers"])
