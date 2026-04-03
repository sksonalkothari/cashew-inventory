"""
Reports Data Access Object (DAO)

Generic utilities for building and executing report queries.
This module provides reusable functions for querying and filtering data.
"""

from typing import Optional, Any, Dict, List
import httpx
from urllib.parse import urlencode
from app.config import SUPABASE_URL
from app.utils.logger import logger
from app.exceptions.exceptions import ReportError


def build_query_string(
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    extra_filters: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Build a query string for Supabase API requests.
    
    Args:
        sort: Format "column:asc" or "column:desc"
        search: Global search term
        date_from: Start date filter (YYYY-MM-DD)
        date_to: End date filter (YYYY-MM-DD)
        extra_filters: Additional filters like {"status": "active"}
    
    Returns:
        URL-encoded query string
    """
    params = {}
    
    # Handle sort parameter
    if sort:
        try:
            col, direction = sort.rsplit(":", 1)
            direction = direction.lower() if direction in ["asc", "desc"] else "asc"
            params["order"] = f"{col}.{direction}"
        except ValueError:
            logger.warning(f"Invalid sort format: {sort}. Expected 'column:asc' or 'column:desc'")
    
    # Add extra filters
    if extra_filters:
        for key, value in extra_filters.items():
            if value is not None:
                params[key] = f"eq.{value}"
    
    # Add date range filters if provided
    if date_from:
        params["created_at"] = f"gte.{date_from}"
    if date_to:
        # For date_to, we need to use a more complex filter
        # This will be handled in the query string separately
        if date_from:
            params["and"] = f"(created_at.gte.{date_from},created_at.lte.{date_to})"
        else:
            params["created_at"] = f"lte.{date_to}"
    
    return urlencode(params) if params else ""


async def execute_report_query(
    table_name: str,
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    select_columns: str = "*",
    extra_filters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generic function to execute a paginated report query on Supabase.
    
    Args:
        table_name: Name of the table to query
        page: Page number (1-indexed)
        page_size: Items per page
        headers: Supabase auth headers
        sort: Sorting parameter (format: "column:asc" or "column:desc")
        search: Global search term (client-side filtering)
        date_from: Start date filter
        date_to: End date filter
        select_columns: Columns to select (default: "*")
        extra_filters: Additional filters as dict
    
    Returns:
        Dict with 'rows' and 'total' keys
    """
    try:
        # Build query string for server-side filters
        query_string = build_query_string(
            sort=sort,
            date_from=date_from,
            date_to=date_to,
            extra_filters=extra_filters,
        )
        
        # Add pagination
        offset = (page - 1) * page_size
        pagination = f"offset={offset}&limit={page_size}"
        
        # Combine all query parameters
        full_query = f"{query_string}&{pagination}" if query_string else pagination
        
        # Build the request URL
        url = f"{SUPABASE_URL}/rest/v1/{table_name}?{full_query}"
        
        # Add select columns
        if select_columns != "*":
            url = f"{SUPABASE_URL}/rest/v1/{table_name}?select={select_columns}&{full_query}"
        
        logger.info(f"Executing report query: {table_name}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code >= 400:
                error_msg = response.json().get("msg") if response.text else "Unknown error"
                logger.error(f"Report query failed for {table_name}: {error_msg}")
                raise ReportError(f"Failed to fetch report data: {error_msg}", status_code=response.status_code)
            
            rows = response.json()
            
            # Get total count
            count_url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=count=exact"
            if query_string:
                count_url = f"{count_url}&{query_string}"
            
            count_response = await client.get(count_url, headers=headers)
            total = int(count_response.headers.get("content-range", "0").split("/")[-1]) if count_response.ok else 0
            
            # Client-side search filtering if search term provided
            if search and rows:
                search_term = search.lower()
                rows = [
                    row for row in rows
                    if any(
                        search_term in str(value).lower()
                        for value in row.values()
                        if value is not None
                    )
                ]
            
            return {
                "rows": rows,
                "total": total,
            }
    
    except ReportError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in report query: {e}")
        raise ReportError(f"Unexpected error: {str(e)}", status_code=500)


# Report-specific query functions

async def fetch_rcn_closing_stock(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    DEPRECATED: This function is no longer used.
    
    The RCN closing stock report now aggregates data using asyncio.gather()
    in the service layer (reports_service.py) for concurrent data fetching
    from multiple tables (purchases, boiling, drying, humidifying, rcn_sales).
    
    See: ReportsService.get_rcn_closing_stock()
    """
    logger.warning("fetch_rcn_closing_stock is deprecated. Use ReportsService.get_rcn_closing_stock() instead")
    return {"rows": [], "total": 0}


async def fetch_outturn(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch outturn report - requires calculation from multiple tables.
    For now, returns batch data that would need to be aggregated.
    """
    return await execute_report_query(
        table_name="batch_summary",
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        select_columns="batch_number,rcn_in_kg,kernel_output_kg,outturn_percent,created_at as date",
    )


async def fetch_nw_percent(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch NW (net weight) percent report.
    """
    return await execute_report_query(
        table_name="batch_summary",
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        select_columns="batch_number,gross_weight_kg,net_weight_kg,nw_percent,created_at as date",
    )


async def fetch_drying_moisture_loss(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch drying moisture loss report.
    Queries the drying table with calculated moisture loss.
    """
    return await execute_report_query(
        table_name="drying",
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        select_columns="batch_number,initial_moisture_percent,final_moisture_percent,moisture_loss_percent,drying_duration_hours,created_at as date",
    )


async def fetch_humidification(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch humidification report.
    Queries the humidifying table with moisture change tracking.
    """
    return await execute_report_query(
        table_name="humidifying",
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        select_columns="batch_number,pre_humidification_moisture,post_humidification_moisture,moisture_added_percent,duration_hours,created_at as date",
    )
