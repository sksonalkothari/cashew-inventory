from typing import List, Union
from fastapi import APIRouter, Depends
from app.models.husk_return_models import (
    HuskReturnCreateRequest,
    HuskReturnUpdateRequest,
    HuskReturnDeleteRequest,
    HuskReturnFetchByBatchNumberRequest,
)
from app.services import husk_return_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger


router = APIRouter(prefix="/husk_return", tags=["Husk_return"])


@router.post("/", summary="Insert husk return records", description="Insert new husk return record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def insert_husk_return(
    payload: Union[HuskReturnCreateRequest, List[HuskReturnCreateRequest]], 
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    headers = current_user.get("headers")
    records = payload if isinstance(payload, list) else [payload]

    enriched = [
        {**rec.model_dump(), "created_by": current_user.get("id")}
        for rec in records
    ]

    res = await husk_return_service.insert_husk_return(enriched, headers)
    return res


@router.patch("/", summary="Update husk return records", description="Update existing husk return record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def update_husk_return(
    payload: Union[HuskReturnUpdateRequest, List[HuskReturnUpdateRequest]], 
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    headers = current_user.get("headers")
    records = payload if isinstance(payload, list) else [payload]

    enriched = [
        {**rec.model_dump(), "updated_by": current_user.get("id")}
        for rec in records
    ]

    res = await husk_return_service.update_husk_return(enriched, headers)
    return res


@router.delete("/", summary="Soft delete husk return records", description="Soft-delete existing husk return record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator"]))])
async def soft_delete_husk_return(
    payload: Union[HuskReturnDeleteRequest, List[HuskReturnDeleteRequest]], 
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    headers = current_user.get("headers")
    records = payload if isinstance(payload, list) else [payload]
    enriched = [
        {**rec.model_dump(), "updated_by": current_user.get("id")}
        for rec in records
    ]

    res = await husk_return_service.soft_delete_husk_return(enriched, headers)
    return res


@router.get("/all", summary="Fetch all husk return records", description="Fetch all existing husk return record(s)",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_all_husk_return(current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))):
    headers = current_user.get("headers")
    return await husk_return_service.fetch_all_husk_return(headers)


@router.get("/batch", summary="Fetch husk return by batch number", description="Fetch existing husk return record(s) by batch number",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_husk_return_by_batch(
    batch_number: str, 
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    headers = current_user.get("headers")
    return await husk_return_service.fetch_husk_return_by_batch(batch_number, headers)


@router.get("/by-date", summary="Fetch husk return by date", description="Fetch existing husk return record(s) by date",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def fetch_husk_return_by_date(
    date: str, 
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    headers = current_user.get("headers")
    return await husk_return_service.fetch_husk_return_by_date(date, headers)
