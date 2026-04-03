# app/controllers/calendar_controller.py
from fastapi import APIRouter, Depends, Query
from app.services import calendar_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger

router = APIRouter(prefix="/calendar_dashboard", tags=["Calendar Dashboard"])

@router.get("/entries/dates-with-data", summary="Returns all dates with any entry", description="Fetch all boiling records",
             dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_dates_with_data(
     current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all dates with any entry")
    return await calendar_service.get_dates_with_data(current_user["headers"]) 

@router.get("/entries/by-date", summary="Returns all entries grouped by module",
            dependencies=[Depends(require_roles(["admin", "entry_operator", "viewer"]))])
async def get_entries_by_date(
    date: str = Query(..., description="YYYY-MM-DD"),
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all entries grouped by module")
    return await calendar_service.get_entries_by_date(date, current_user["headers"])