from typing import Union, List

from fastapi import APIRouter, Depends
from app.models.purchase_models import (
    PurchaseCreateRequest, PurchaseUpdateRequest,
    PurchaseDeleteRequest
)
from app.services import purchase_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger

router = APIRouter(prefix="/purchase", tags=["Purchases"])

@router.post("/", summary="Insert Purchase", description="Insert a new purchase record",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def create_purchase(
    data: Union[PurchaseCreateRequest, List[PurchaseCreateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info("Inserting Purchase record/s")
    enriched_data = [
            {**record.model_dump(), "created_by": current_user["id"]}
            for record in data
        ]
    return await purchase_service.insert_purchase(enriched_data, current_user["headers"])

@router.patch("/", summary="Update Purchase", description="Update an existing purchase record",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_purchase(
    data: Union[PurchaseUpdateRequest, List[PurchaseUpdateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating purchase record/s")
    enriched_data = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in data
    ]
    return await purchase_service.update_purchase(enriched_data, current_user["headers"])
        
@router.delete("/", summary="Delete Purchase", description="Delete an existing purchase record",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def delete_purchase(
    data: Union[PurchaseDeleteRequest, List[PurchaseDeleteRequest]],
    current_user: dict = Depends(require_roles(["admin"]))
):
    logger.info(f"Soft-deleting purchase record/s")
    enriched_data = [
        {**record.model_dump(), "updated_by": current_user["id"]}
        for record in data
    ]
    return await purchase_service.soft_delete_purchase(enriched_data, current_user["headers"])

@router.get("/all", summary="Get All Purchases", description="Fetch all purchase records",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_all_purchases(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all purchase records")
    return await purchase_service.fetch_all_purchases(current_user["headers"])

@router.get("/by-date", summary="Get Purchases by Date", description="Fetch purchase records by date",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_purchases_by_date(
    date: str,
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info(f"Fetching purchase records for date: {date}")
    return await purchase_service.fetch_purchases_by_date(date, current_user["headers"])