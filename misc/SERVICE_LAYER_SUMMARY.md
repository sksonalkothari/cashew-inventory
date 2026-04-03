# Service Layer Addition - Summary

## What Was Added

A new **Service Layer** (`reports_service.py`) between the Controller and DAO layers to handle:

1. ✅ **Business Logic** - Aggregations, calculations, transformations
2. ✅ **Multi-Table Fetching** - Combine data from multiple tables
3. ✅ **Data Enrichment** - Add calculated/derived columns
4. ✅ **Utility Functions** - Common calculation patterns

## Architecture

```
Controller (HTTP API)
    ↓ calls
Service (Business Logic)  ← NEW LAYER
    ↓ calls
DAO (Database Queries)
    ↓
Supabase (Data)
```

## New Architecture Benefits

| Before               | After                      |
| -------------------- | -------------------------- |
| Controller → DAO     | Controller → Service → DAO |
| No calculations      | Centralized calculations   |
| No data enrichment   | Easy data enrichment       |
| Single table queries | Multi-table aggregation    |
| Limited utilities    | Rich utility functions     |

---

## Files Created/Modified

### Created Files

#### 1. `backend/app/services/reports_service.py` (NEW)

- **ReportsService** - Report-specific service methods (5 methods)
- **AdvancedReportsService** - Complex multi-table aggregations (3 example methods)
- **ReportUtilsService** - Utility functions (10+ utility methods)

#### 2. `backend/app/controllers/reports_controller.py` (MODIFIED)

- Changed import from `reports_dao` → `reports_service`
- All endpoints now call service methods instead of DAO directly
- Service methods handle data processing, DAO only handles queries

#### 3. `backend/app/controllers/REPORTS_SETUP.md` (ENHANCED)

- Added documentation for service layer
- Added 5 advanced service patterns
- Updated "Creating a New Report" to include service layer
- Separated "Advanced Service Patterns" from "Advanced DAO Patterns"

---

## Example: Reports Service Methods

### Simple Calculation Service

```python
@staticmethod
async def get_outturn(...) -> Dict[str, Any]:
    """Fetch and calculate outturn percentage."""
    # Step 1: Fetch from DAO
    result = await reports_dao.fetch_outturn(...)

    # Step 2: Calculate derived column
    for row in result.get("rows", []):
        rcn_input = row.get("rcn_input_kg", 0)
        kernel_output = row.get("kernel_output_kg", 0)
        if rcn_input > 0:
            row["outturn_percent"] = round((kernel_output / rcn_input) * 100, 2)

    # Step 3: Return enriched result
    return result
```

### Multi-Table Aggregation Service

```python
@staticmethod
async def get_batch_processing_summary(...) -> Dict[str, Any]:
    """Aggregate data from multiple tables."""
    # Fetch main batch data
    batches = await reports_dao.fetch_rcn_closing_stock(...)

    # For each batch, could fetch related data:
    # - boiling data
    # - drying data
    # - grades data
    # - peeling data

    # Combine and return enriched data
    enriched_rows = []
    for batch in batches.get("rows", []):
        enriched = {
            **batch,
            "processing_status": "Completed",
            # ... additional calculated fields ...
        }
        enriched_rows.append(enriched)

    return {"rows": enriched_rows, "total": batches.get("total")}
```

### Aggregation & Metrics Service

```python
@staticmethod
async def get_production_metrics(...) -> Dict[str, Any]:
    """Calculate aggregate production metrics."""
    # Fetch all data for aggregation
    data = await reports_dao.fetch_outturn(page=1, page_size=10000, ...)
    rows = data.get("rows", [])

    # Calculate metrics using utilities
    metrics = {
        "total_rcn_input_kg": ReportUtilsService.sum_field(rows, "rcn_input_kg"),
        "total_kernel_output_kg": ReportUtilsService.sum_field(rows, "kernel_output_kg"),
        "average_outturn": ReportUtilsService.average_field(rows, "outturn_percent"),
        "total_batches": len(rows),
    }

    # Return paginated results with metrics
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "rows": rows[start:end],
        "total": len(rows),
        "metrics": metrics,  # Aggregate metrics included
    }
```

---

## Utility Functions Available

### `ReportUtilsService` Class

```python
# Percentage calculations
calculate_percentage(value, total)           # Safe percentage
calculate_percentage_change(start, end)      # Percentage change

# Safe operations
safe_divide(numerator, denominator, default)  # Avoid division by zero
format_currency(amount, currency="₹")        # Currency formatting

# Aggregations
group_by_field(rows, field)                  # Group rows by field
sum_field(rows, field)                       # Sum numeric field
average_field(rows, field)                   # Average numeric field

# Row enrichment
enrich_row_with_calculations(row, calculations)        # Single row
enrich_rows_with_calculations(rows, calculations)      # Multiple rows
```

### Example Usage

```python
# Calculate percentage safely
profit_percent = ReportUtilsService.calculate_percentage(100, 500)  # 20.0

# Avoid division errors
ratio = ReportUtilsService.safe_divide(value, divisor, default=0)

# Format amounts
display = ReportUtilsService.format_currency(1000000)  # ₹1,000,000.00

# Group and aggregate
grouped = ReportUtilsService.group_by_field(rows, "location")
for location, location_rows in grouped.items():
    total = ReportUtilsService.sum_field(location_rows, "amount")
    average = ReportUtilsService.average_field(location_rows, "price")

# Enrich with calculations
calculations = {
    "profit_margin": lambda r: (r["revenue"] - r["cost"]) / r["revenue"] * 100,
    "status": lambda r: "Active" if r["amount"] > 0 else "Inactive",
    "display_amount": lambda r: ReportUtilsService.format_currency(r["amount"]),
}
enriched_rows = ReportUtilsService.enrich_rows_with_calculations(rows, calculations)
```

---

## Creating a New Report with Service Layer

### 1. Create Service Method (in `reports_service.py`)

```python
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

    # Fetch from DAO
    result = await reports_dao.fetch_my_report(
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )

    # Enrich with calculations
    for row in result.get("rows", []):
        # Add calculated columns
        row["percentage"] = ReportUtilsService.calculate_percentage(
            row.get("value", 0), row.get("total", 0)
        )
        row["status"] = "Active" if row.get("amount", 0) > 0 else "Inactive"

    return result
```

### 2. Create Controller Endpoint (in `reports_controller.py`)

```python
@router.get("/my-report", summary="My Report Title")
async def get_my_report(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """Report description."""
    logger.info("Controller: Fetching my report")
    try:
        result = await ReportsService.get_my_report(  # Calls service, not DAO!
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
        logger.error(f"Error: {e}")
        raise
```

### 3. Create DAO Query (in `reports_dao.py`)

```python
async def fetch_my_report(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch my report data from database."""
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

**Total: 3 simple functions = Complete report with calculations!**

---

## Advanced Service Patterns

### Pattern 1: Multi-Table Queries

```python
@staticmethod
async def get_complete_batch_summary(...):
    # Fetch from multiple sources
    batch_data = await reports_dao.fetch_batches(...)

    enriched = []
    for batch in batch_data.get("rows", []):
        batch_id = batch.get("id")

        # Could fetch related data
        # boiling = await reports_dao.fetch_boiling_by_batch_id(batch_id, ...)
        # drying = await reports_dao.fetch_drying_by_batch_id(batch_id, ...)
        # grades = await reports_dao.fetch_grades_by_batch_id(batch_id, ...)

        # Merge and enhance
        enriched.append({
            **batch,
            # ...merged data from other tables...
        })

    return {"rows": enriched, "total": len(enriched)}
```

### Pattern 2: Aggregations with Metrics

```python
@staticmethod
async def get_dashboard_metrics(...):
    # Fetch detailed data
    data = await reports_dao.fetch_all_records(page=1, page_size=10000, ...)
    rows = data.get("rows", [])

    # Group by categories
    by_category = ReportUtilsService.group_by_field(rows, "category")

    # Calculate metrics per category
    metrics_by_category = {}
    for cat, cat_rows in by_category.items():
        metrics_by_category[cat] = {
            "count": len(cat_rows),
            "total_amount": ReportUtilsService.sum_field(cat_rows, "amount"),
            "average_price": ReportUtilsService.average_field(cat_rows, "price"),
        }

    return {
        "rows": rows,
        "total": len(rows),
        "metrics": metrics_by_category,
        "summary": {
            "total_records": len(rows),
            "total_amount": ReportUtilsService.sum_field(rows, "amount"),
        }
    }
```

### Pattern 3: Row Enrichment

```python
@staticmethod
async def get_enriched_sales_report(...):
    result = await reports_dao.fetch_sales(...)

    # Define rich calculations
    calculations = {
        "gross_profit": lambda r: r.get("revenue", 0) - r.get("cost", 0),
        "profit_margin": lambda r: ReportUtilsService.calculate_percentage(
            r.get("revenue", 0) - r.get("cost", 0),
            r.get("revenue", 0)
        ),
        "status_label": lambda r: "Profitable" if r.get("gross_profit", 0) > 0 else "Loss",
        "formatted_amount": lambda r: ReportUtilsService.format_currency(r.get("revenue", 0)),
    }

    enriched = ReportUtilsService.enrich_rows_with_calculations(
        result.get("rows", []), calculations
    )

    return {"rows": enriched, "total": result.get("total")}
```

---

## Key Design Principles

1. **Separation of Concerns**

   - Controller: HTTP & routing
   - Service: Business logic & calculations
   - DAO: Database queries

2. **Reusable Calculations**

   - Common calculations in `ReportUtilsService`
   - Single source of truth for formulas

3. **Data Enrichment**

   - Add calculated fields without modifying schema
   - Lambda-based flexible calculations

4. **Multi-Table Support**

   - Service layer can call multiple DAO functions
   - Combine and aggregate results

5. **Easy Testing**
   - Service layer can be tested independently
   - Mock DAO calls during testing

---

## Summary

The **Service Layer** provides:

✅ **Centralized Business Logic** - One place for calculations  
✅ **Data Enrichment** - Easy to add calculated columns  
✅ **Multi-Table Aggregation** - Combine data from multiple sources  
✅ **Utility Functions** - Common patterns (percentage, currency, grouping, etc.)  
✅ **Clean Architecture** - Clear separation of concerns  
✅ **Easy Maintenance** - Logic isolated from HTTP and database layers  
✅ **Scalability** - Easy to add complex reports without cluttering controller

**Result:** Cleaner, more maintainable, more scalable report infrastructure! 🚀
