# Backend Reports Infrastructure Guide

## Overview

The backend reports infrastructure provides a unified, generic system for querying and filtering data from Supabase. It's designed to minimize code duplication and make adding new reports straightforward.

## Key Components

### 1. reports_controller.py

Handles all report API endpoints with consistent query parameter handling.

**Base Query Parameters:**

```python
@router.get("/report-name", summary="Report Title")
async def get_report_name(
    query: ReportQuery = Depends(),  # Parses all query parameters
    current_user: dict = Depends(get_current_user),  # Authentication
):
```

**ReportQuery** automatically parses:

- `page` (int, ≥1) - Page number (1-indexed)
- `pageSize` (int, 1-500) - Items per page
- `sort` (string) - Format: `column:asc` or `column:desc`
- `search` (string) - Global search term
- `dateFrom` (string) - ISO date (YYYY-MM-DD)
- `dateTo` (string) - ISO date (YYYY-MM-DD)

### 2. reports_service.py (Service Layer)

**NEW** - Handles business logic between controller and DAO:

- Fetching and aggregating data from multiple tables
- Calculating and transforming data
- Building complex queries
- Post-processing results

**Key Classes:**

#### `ReportsService`

Contains service methods for each report type.

```python
result = await ReportsService.get_outturn(
    page=1,
    page_size=25,
    headers=headers,
    sort="batch_number:asc",
    search=None,
    date_from="2025-01-01",
    date_to="2025-01-31",
)
```

Each method:

- Calls DAO to fetch base data
- Performs calculations and transformations
- Enriches rows with calculated columns
- Returns formatted result

Example - Calculating outturn percentage:

```python
@staticmethod
async def get_outturn(...):
    # Fetch data from DAO
    result = await reports_dao.fetch_outturn(...)

    # Enrich with calculations
    for row in result.get("rows", []):
        if "outturn_percent" not in row or row["outturn_percent"] is None:
            rcn_input = row.get("rcn_input_kg", 0)
            kernel_output = row.get("kernel_output_kg", 0)
            if rcn_input > 0:
                row["outturn_percent"] = round((kernel_output / rcn_input) * 100, 2)

    return result
```

#### `AdvancedReportsService`

Complex multi-table aggregations (examples):

```python
# Get comprehensive batch processing summary
await AdvancedReportsService.get_batch_processing_summary(...)

# Get aggregated production metrics
await AdvancedReportsService.get_production_metrics(...)

# Get quality report with grade distribution
await AdvancedReportsService.get_quality_report(...)
```

For multi-table aggregations:

1. Fetch from multiple DAOs
2. Combine and merge data
3. Calculate aggregate metrics
4. Return combined result

#### `ReportUtilsService`

Utility functions for calculations and transformations:

```python
# Safe calculations
percentage = ReportUtilsService.calculate_percentage(100, 500)  # 20.0
pct_change = ReportUtilsService.calculate_percentage_change(100, 150)  # 50.0

# Safe division
result = ReportUtilsService.safe_divide(numerator, denominator, default=0)

# Currency formatting
formatted = ReportUtilsService.format_currency(1000)  # ₹1,000.00

# Grouping and aggregations
grouped = ReportUtilsService.group_by_field(rows, "category")
total = ReportUtilsService.sum_field(rows, "amount")
avg = ReportUtilsService.average_field(rows, "percentage")

# Row enrichment with calculations
calculations = {
    "profit_margin": lambda r: (r["revenue"] - r["cost"]) / r["revenue"] * 100,
    "status": lambda r: "Active" if r["amount"] > 0 else "Inactive",
}
enriched = ReportUtilsService.enrich_row_with_calculations(row, calculations)
enriched_rows = ReportUtilsService.enrich_rows_with_calculations(rows, calculations)
```

### 3. reports_dao.py

Core data access module with reusable utilities.

**Key Functions:**

#### `build_query_string()`

Builds URL-encoded query parameters for Supabase requests.

```python
query_string = build_query_string(
    sort="column:asc",
    search="term",
    date_from="2025-01-01",
    date_to="2025-01-31",
    extra_filters={"status": "active"}
)
```

#### `execute_report_query()`

Generic function that handles pagination, sorting, and filtering on any Supabase table.

```python
result = await execute_report_query(
    table_name="batch_summary",
    page=1,
    page_size=25,
    headers=headers,
    sort="batch_number:asc",
    search="batch123",
    date_from="2025-01-01",
    date_to="2025-01-31",
    select_columns="batch_number,quantity,date",
    extra_filters={"status": "active"}
)

# Returns:
# {
#     "rows": [...],
#     "total": 100
# }
```

**Parameters:**

- `table_name` (str) - Supabase table or view name
- `page` (int) - Page number (1-indexed)
- `page_size` (int) - Items per page
- `headers` (dict) - Supabase auth headers
- `sort` (Optional[str]) - Sort format: "column:asc" or "column:desc"
- `search` (Optional[str]) - Search term (client-side filtering)
- `date_from` (Optional[str]) - Start date filter
- `date_to` (Optional[str]) - End date filter
- `select_columns` (str) - CSV of columns to select (default: "\*")
- `extra_filters` (Optional[Dict]) - Domain-specific filters

## Creating a New Report Endpoint

### Three-Layer Architecture

**1. Controller Layer** - Request handling & routing

```python
@router.get("/my-report")
async def get_my_report(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """API endpoint definition."""
    logger.info("Controller: Fetching my report")
    try:
        result = await ReportsService.get_my_report(...)
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

**2. Service Layer** - Business logic & calculations

```python
@staticmethod
async def get_my_report(page: int, page_size: int, headers: dict, **kwargs):
    """Fetch and process data."""
    # Get base data from DAO
    result = await reports_dao.fetch_my_report(page, page_size, headers, **kwargs)

    # Transform and calculate
    for row in result.get("rows", []):
        # Calculate new columns
        row["new_column"] = calculate_value(row)
        # Add derived data
        row["status"] = "Active" if row["amount"] > 0 else "Inactive"

    return result
```

**3. DAO Layer** - Database queries

```python
async def fetch_my_report(page: int, page_size: int, headers: dict, **kwargs):
    """Query database."""
    return await execute_report_query(
        table_name="my_table",
        page=page,
        page_size=page_size,
        headers=headers,
        select_columns="col1,col2,col3",
        **kwargs
    )
```

### Minimal Implementation

**1. Add controller method:**

```python
@router.get("/my-report", summary="My Report Title")
async def get_my_report(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """Report description and documentation."""
    logger.info("Controller: Fetching my report")
    try:
        result = await ReportsService.get_my_report(
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
        logger.error(f"Error fetching my report: {e}")
        raise
```

**2. Add service method:**

```python
# In reports_service.py, add to ReportsService class

@staticmethod
async def get_my_report(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """Get my report with calculations."""
    logger.info("Service: Fetching my report")

    # Get data from DAO
    result = await reports_dao.fetch_my_report(
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )

    # Post-process: Add calculated columns
    for row in result.get("rows", []):
        # Example calculations
        if row.get("total") > 0:
            row["percentage"] = round((row.get("value", 0) / row["total"]) * 100, 2)
        row["status"] = "Active" if row.get("amount", 0) > 0 else "Inactive"

    return result
```

**3. Add DAO method:**

```python
# In reports_dao.py

async def fetch_my_report(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch my report data."""
    return await execute_report_query(
        table_name="my_table",
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        select_columns="col1,col2,col3",
    )
```

That's it! ✅

**That's it!** You now have:

- ✅ Pagination
- ✅ Sorting
- ✅ Global search
- ✅ Date filtering
- ✅ Error handling
- ✅ Logging

---

## Advanced Service Patterns

### Pattern 1: Single-Table with Calculations

Calculate derived columns from existing data:

```python
@staticmethod
async def get_outturn(...):
    result = await reports_dao.fetch_outturn(...)

    for row in result.get("rows", []):
        if "outturn_percent" not in row or row["outturn_percent"] is None:
            rcn_input = row.get("rcn_input_kg", 0)
            kernel_output = row.get("kernel_output_kg", 0)
            if rcn_input > 0:
                row["outturn_percent"] = round((kernel_output / rcn_input) * 100, 2)

    return result
```

### Pattern 2: Multi-Table Aggregation

Fetch and combine data from multiple tables:

```python
@staticmethod
async def get_batch_processing_summary(page: int, page_size: int, headers: dict, **kwargs):
    batch_data = await reports_dao.fetch_rcn_closing_stock(page, page_size, headers, **kwargs)

    enriched_rows = []
    for batch in batch_data.get("rows", []):
        enriched = {**batch, "processing_status": "Completed"}
        enriched_rows.append(enriched)

    return {"rows": enriched_rows, "total": batch_data.get("total", 0)}
```

### Pattern 3: Aggregation & Metrics

```python
@staticmethod
async def get_production_metrics(page: int, page_size: int, headers: dict, **kwargs):
    data = await reports_dao.fetch_outturn(page=1, page_size=10000, headers=headers, **kwargs)
    rows = data.get("rows", [])

    metrics = {
        "total_rcn_input_kg": ReportUtilsService.sum_field(rows, "rcn_input_kg"),
        "average_outturn": ReportUtilsService.average_field(rows, "outturn_percent"),
    }

    start = (page - 1) * page_size
    return {"rows": rows[start:start+page_size], "total": len(rows), "metrics": metrics}
```

---

## Advanced DAO Patterns

### Pattern 1: Domain-Specific Filters

Add custom filters to your endpoint:

```python
@router.get("/batch-report")
async def get_batch_report(
    query: ReportQuery = Depends(),
    origin: Optional[str] = Query(None, description="Filter by origin"),
    status: Optional[str] = Query(None, description="Filter by batch status"),
    current_user: dict = Depends(get_current_user),
):
    """Report filtered by origin and status."""
    try:
        result = await reports_dao.fetch_batch_report(
            page=query.page,
            page_size=query.pageSize,
            sort=query.sort,
            search=query.search,
            date_from=query.dateFrom,
            date_to=query.dateTo,
            headers=current_user["headers"],
            origin=origin,  # Pass custom filter
            status=status,
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching batch report: {e}")
        raise
```

```python
# In DAO:
async def fetch_batch_report(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    origin: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Report with custom filters."""
    return await execute_report_query(
        table_name="batch_summary",
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        select_columns="batch_number,origin,status,created_at",
        extra_filters={
            "origin": origin,
            "status": status,
        },
    )
```

### Pattern 2: Custom Supabase View

For complex calculations, create a database view in Supabase:

```sql
-- Supabase SQL Editor
CREATE VIEW outturn_report_view AS
SELECT
  b.id,
  b.batch_number,
  b.origin,
  b.rcn_in_kg,
  COALESCE(SUM(g.kernel_output_kg), 0) as kernel_output_kg,
  CASE
    WHEN b.rcn_in_kg > 0
    THEN ROUND((COALESCE(SUM(g.kernel_output_kg), 0) / b.rcn_in_kg) * 100, 2)
    ELSE 0
  END as outturn_percent,
  b.created_at as date
FROM batch_summary b
LEFT JOIN grades g ON b.id = g.batch_id
GROUP BY b.id, b.batch_number, b.origin, b.rcn_in_kg, b.created_at
ORDER BY b.created_at DESC;
```

Then query it simply:

```python
async def fetch_outturn(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch outturn from pre-calculated view."""
    return await execute_report_query(
        table_name="outturn_report_view",  # Use view name
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )
```

### Pattern 3: Row-Level Security Compliance

The current implementation passes `headers` from the authenticated user to Supabase. This ensures Row-Level Security (RLS) policies are applied.

```python
# RLS will filter data based on the user's role/permissions
result = await execute_report_query(
    table_name="sensitive_data",
    headers=current_user["headers"],  # Auth headers ensure RLS is applied
    # ...
)
```

Make sure your RLS policies are set up in Supabase to restrict access appropriately.

### Pattern 4: Real-time Aggregations

For performance-critical aggregations, use Supabase PostgREST filters:

```python
async def fetch_daily_summary(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch pre-aggregated daily summary."""
    return await execute_report_query(
        table_name="daily_summary",  # Pre-aggregated table
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )
```

---

## Query Building Logic

### Sort Parameter Format

Expected format: `column:asc` or `column:desc`

```python
# Input: "batch_number:asc"
# Output in URL: "order=batch_number.asc"

# Input: "rcn_in_kg:desc"
# Output in URL: "order=rcn_in_kg.desc"
```

### Date Filtering

Supports date range filtering with `dateFrom` and `dateTo`:

```python
# Single condition (from date):
# ?dateFrom=2025-01-01
# Converted to: created_at >= 2025-01-01

# Single condition (to date):
# ?dateTo=2025-01-31
# Converted to: created_at <= 2025-01-31

# Range (both):
# ?dateFrom=2025-01-01&dateTo=2025-01-31
# Converted to: created_at >= 2025-01-01 AND created_at <= 2025-01-31
```

### Pagination

Offset-based pagination:

```python
offset = (page - 1) * page_size
# page=1, pageSize=25  → offset=0, limit=25   (rows 1-25)
# page=2, pageSize=25  → offset=25, limit=25  (rows 26-50)
# page=3, pageSize=10  → offset=20, limit=10  (rows 21-30)
```

### Search

Client-side search through returned rows (case-insensitive):

```python
# Input: ?search=batch123
# Searches all string values in all columns for "batch123"
# Returns matching rows
```

---

## Response Format

All endpoints return:

```json
{
  "rows": [
    {
      "column1": "value1",
      "column2": 123,
      "column3": "2025-01-26"
    }
    // ... more rows ...
  ],
  "total": 450
}
```

- `rows` - Array of matching records (paginated)
- `total` - Total count of matching records (before pagination)

---

## Error Handling

Errors are automatically caught and formatted:

```python
# ReportError is raised for database/query errors
# Caught by @app.exception_handler(BaseAppException) in main.py
# Response:
# {
#   "errors": [
#     {
#       "field": "general",
#       "message": "Failed to fetch report data: [error details]"
#     }
#   ]
# }
```

Log all errors for debugging:

```python
logger.error(f"Error fetching report: {e}")
```

---

## Performance Considerations

1. **Use Column Selection**

   ```python
   select_columns="batch_number,rcn_in_kg,created_at"  # Only needed columns
   # NOT: select_columns="*"  (fetches unused data)
   ```

2. **Leverage Database Indexes**

   - Create indexes on frequently sorted/filtered columns
   - Supabase automatically indexes primary keys and foreign keys

3. **Use Views for Complex Calculations**

   - Pre-calculate aggregations in database views
   - Let the database do the heavy lifting

4. **Pagination is Essential**

   - Always paginate (never fetch all records at once)
   - Default limit is 500 items per request

5. **Consider Table Partitioning**
   - For very large tables (millions of rows)
   - Partition by date or batch ID

---

## Existing Report Implementations

### RCN Closing Stock

- Table: `batch_summary`
- Columns: batch_number, origin, rcn_in_kg, rcn_to_boiling_kg, rcn_sold_kg, adjustments_kg, closing_stock_kg
- Endpoint: GET `/api/v1/reports/rcn-closing-stock`

### Outturn

- Table/View: `batch_summary` (or `outturn_report_view` if created)
- Columns: batch_number, rcn_input_kg, kernel_output_kg, outturn_percent, date
- Endpoint: GET `/api/v1/reports/outturn`

### NW Percent

- Table: `batch_summary`
- Columns: batch_number, gross_weight_kg, net_weight_kg, nw_percent, date
- Endpoint: GET `/api/v1/reports/nw-percent`

### Drying Moisture Loss

- Table: `drying`
- Columns: batch_number, initial_moisture_percent, final_moisture_percent, moisture_loss_percent, drying_duration_hours, date
- Endpoint: GET `/api/v1/reports/drying-moisture-loss`

### Humidification

- Table: `humidifying`
- Columns: batch_number, pre_humidification_moisture, post_humidification_moisture, moisture_added_percent, duration_hours, date
- Endpoint: GET `/api/v1/reports/humidification`

---

## Testing Reports

### Manual Testing with curl

```bash
# Basic query
curl "http://localhost:8000/api/v1/reports/rcn-closing-stock?page=1&pageSize=10"

# With sorting
curl "http://localhost:8000/api/v1/reports/rcn-closing-stock?page=1&pageSize=10&sort=batch_number:asc"

# With search and date range
curl "http://localhost:8000/api/v1/reports/outturn?page=1&pageSize=25&search=batch&dateFrom=2025-01-01&dateTo=2025-01-31"

# With custom filter
curl "http://localhost:8000/api/v1/reports/batch-report?page=1&origin=India&status=completed"
```

### Using Postman or Insomnia

1. Create request to: `http://localhost:8000/api/v1/reports/[report-name]`
2. Add query parameters in "Params" tab
3. Add Authorization header with valid JWT token
4. Send GET request

---

## Database Schema Requirements

For a report to work, the Supabase table/view must:

1. **Have columns matching your select_columns** (or use "\*")
2. **Support authentication headers** (for RLS policies)
3. **Have proper indexes** on sorted/filtered columns
4. **Define RLS policies** (if using row-level security)

Example table schema:

```sql
CREATE TABLE batch_summary (
  id BIGSERIAL PRIMARY KEY,
  batch_number VARCHAR(50) NOT NULL UNIQUE,
  origin VARCHAR(100),
  rcn_in_kg DECIMAL(10, 2),
  rcn_to_boiling_kg DECIMAL(10, 2),
  rcn_sold_kg DECIMAL(10, 2),
  adjustments_kg DECIMAL(10, 2),
  closing_stock_kg DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT NOW(),
  created_by BIGINT REFERENCES auth.users(id),
  updated_at TIMESTAMP DEFAULT NOW(),
  updated_by BIGINT REFERENCES auth.users(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

-- Create indexes for performance
CREATE INDEX idx_batch_number ON batch_summary(batch_number);
CREATE INDEX idx_created_at ON batch_summary(created_at);
CREATE INDEX idx_origin ON batch_summary(origin);
```

---

## Troubleshooting

### Report returns 404

- Verify endpoint exists in `reports_controller.py`
- Check the route registration in `main.py`
- Ensure import statement includes `reports_controller`

### Report returns empty data

- Verify table/view name is correct in DAO
- Check column names match database schema
- Ensure data exists in the table
- Verify RLS policies aren't blocking access

### Sorting not working

- Confirm column name is correct (case-sensitive in Supabase)
- Verify sort format: `column:asc` or `column:desc`
- Check column exists in the table

### Slow queries

- Add indexes to sorted/filtered columns
- Reduce pageSize
- Use select_columns instead of "\*"
- Consider creating a pre-aggregated view

### Authentication errors

- Verify user has valid JWT token
- Check RLS policies allow access to the table
- Ensure headers are passed correctly to Supabase

---

## Summary

The backend reports infrastructure provides:

✅ **Reusable Query Builder** - Generic `execute_report_query()` handles all common cases
✅ **Consistent Parameter Handling** - Standard query parameters across all endpoints
✅ **Error Handling** - Built-in exception handling and logging
✅ **Security** - Row-level security integration via auth headers
✅ **Performance** - Pagination, selective column loading, index support
✅ **Extensibility** - Easy to add custom filters and domain-specific logic

Happy reporting! 📊
