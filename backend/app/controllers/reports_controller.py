from typing import Optional, Any, Dict, List
from fastapi import APIRouter, Query, Depends
from app.services import reports_service
from app.dependencies.auth_dependency import get_current_user
from app.utils.logger import logger

router = APIRouter(prefix="/reports", tags=["Reports"])

# Query parameter models for better documentation
class ReportQuery:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number (1-indexed)"),
        pageSize: int = Query(25, ge=1, le=10000, description="Items per page"),
        sort: Optional[str] = Query(None, description="Sort format: 'column:asc' or 'column:desc'"),
        search: Optional[str] = Query(None, description="Global search across all text fields"),
        dateFrom: Optional[str] = Query(None, description="Filter from date (ISO format: YYYY-MM-DD)"),
        dateTo: Optional[str] = Query(None, description="Filter to date (ISO format: YYYY-MM-DD)"),
    ):
        self.page = page
        self.pageSize = pageSize
        self.sort = sort
        self.search = search
        self.dateFrom = dateFrom
        self.dateTo = dateTo

@router.get("/rcn-closing-stock", summary="RCN Closing Stock Report")
async def get_rcn_closing_stock(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """
    Report showing the closing stock of RCN by Batch No.
    
    Query Parameters:
    - page: Page number (1-indexed)
    - pageSize: Items per page (default 25)
    - sort: Sorting (format: 'column:asc' or 'column:desc')
    - search: Global search across batch_number, origin
    - dateFrom: Filter from date (YYYY-MM-DD)
    - dateTo: Filter to date (YYYY-MM-DD)
    """
    logger.info("Controller: Fetching RCN closing stock report")
    try:
        result = await reports_service.ReportsService.get_rcn_closing_stock(
            page=query.page,
            page_size=query.pageSize,
            sort=query.sort,
            search=query.search,
            date_from=query.dateFrom,
            date_to=query.dateTo,
            headers=current_user["headers"],
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching RCN closing stock: {e}")
        raise

@router.get("/outturn", summary="Outturn Report")
async def get_outturn(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """
    Outturn percentage and yield analysis by batch.
    """
    logger.info("Controller: Fetching outturn report")
    try:
        result = await reports_service.ReportsService.get_outturn(
            page=query.page,
            page_size=query.pageSize,
            sort=query.sort,
            search=query.search,
            date_from=query.dateFrom,
            date_to=query.dateTo,
            headers=current_user["headers"],
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching outturn report: {e}")
        raise

@router.get("/nw-percent", summary="NW Percent Report")
async def get_nw_percent(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """
    Net weight percentage analysis.
    """
    logger.info("Controller: Fetching NW percent report")
    try:
        result = await reports_service.ReportsService.get_nw_percent(
            page=query.page,
            page_size=query.pageSize,
            sort=query.sort,
            search=query.search,
            date_from=query.dateFrom,
            date_to=query.dateTo,
            headers=current_user["headers"],
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching NW percent report: {e}")
        raise

@router.get("/drying-moisture-loss", summary="Drying Moisture Loss Report")
async def get_drying_moisture_loss(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """
    Moisture loss during drying process.
    """
    logger.info("Controller: Fetching drying moisture loss report")
    try:
        result = await reports_service.ReportsService.get_drying_moisture_loss(
            page=query.page,
            page_size=query.pageSize,
            sort=query.sort,
            search=query.search,
            date_from=query.dateFrom,
            date_to=query.dateTo,
            headers=current_user["headers"],
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching drying moisture loss report: {e}")
        raise

@router.get("/humidification", summary="Humidification Report")
async def get_humidification(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """
    Humidification process tracking - moisture rehydration.
    """
    logger.info("Controller: Fetching humidification report")
    try:
        result = await reports_service.ReportsService.get_humidification(
            page=query.page,
            page_size=query.pageSize,
            sort=query.sort,
            search=query.search,
            date_from=query.dateFrom,
            date_to=query.dateTo,
            headers=current_user["headers"],
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching humidification report: {e}")
        raise
