# Service Layer - Quick Reference

## Three-Layer Architecture

```
HTTP Request
    ↓
@router.get("/report")
async def get_report(...):
    # ← CONTROLLER: Parse query params, call service
    result = await ReportsService.get_report(...)
    return result
    ↓
@staticmethod
async def get_report(...):
    # ← SERVICE: Business logic, calculations, enrichment
    result = await reports_dao.fetch_report(...)
    for row in result.get("rows", []):
        row["calculated_field"] = calculate(row)
    return result
    ↓
async def fetch_report(...):
    # ← DAO: Database query only
    return await execute_report_query(...)
    ↓
Supabase
```

---

## Service Layer Responsibilities

| Layer          | What It Does                          | Examples                           |
| -------------- | ------------------------------------- | ---------------------------------- |
| **Controller** | HTTP, routing, auth                   | `/api/reports/my-report?page=1`    |
| **Service**    | Calculations, enrichment, aggregation | Outturn %, NW %, grouping, metrics |
| **DAO**        | Database queries, filtering           | SELECT \* FROM table WHERE...      |

---

## Creating Reports: 3-Step Pattern

### Step 1: Service Method

```python
# In reports_service.py, add to ReportsService class

@staticmethod
async def get_my_report(page: int, page_size: int, headers: dict, **kwargs):
    # Fetch from DAO
    result = await reports_dao.fetch_my_report(page, page_size, headers, **kwargs)

    # Enrich with calculations
    for row in result.get("rows", []):
        row["percentage"] = calculate_percentage(row)

    return result
```

### Step 2: Controller Endpoint

```python
# In reports_controller.py

@router.get("/my-report")
async def get_my_report(query: ReportQuery = Depends(), current_user = Depends(get_current_user)):
    return await ReportsService.get_my_report(
        page=query.page, page_size=query.pageSize, sort=query.sort,
        search=query.search, date_from=query.dateFrom, date_to=query.dateTo,
        headers=current_user["headers"],
    )
```

### Step 3: DAO Query

```python
# In reports_dao.py

async def fetch_my_report(page: int, page_size: int, headers: dict, **kwargs):
    return await execute_report_query(
        table_name="my_table",
        page=page, page_size=page_size, headers=headers,
        select_columns="col1,col2,col3",
        **kwargs
    )
```

---

## Utility Functions

```python
# Percentages
ReportUtilsService.calculate_percentage(100, 500)              # 20.0
ReportUtilsService.calculate_percentage_change(100, 150)       # 50.0

# Safe math
ReportUtilsService.safe_divide(value, divisor, default=0)     # Avoids /0 errors
ReportUtilsService.format_currency(1000)                       # ₹1,000.00

# Grouping & aggregation
ReportUtilsService.group_by_field(rows, "location")           # Dict of grouped rows
ReportUtilsService.sum_field(rows, "amount")                  # Total of field
ReportUtilsService.average_field(rows, "price")               # Average of field

# Row enrichment
calcs = {"profit": lambda r: r["revenue"] - r["cost"]}
ReportUtilsService.enrich_row_with_calculations(row, calcs)   # Single row
ReportUtilsService.enrich_rows_with_calculations(rows, calcs) # Multiple rows
```

---

## Common Service Patterns

### Pattern 1: Simple Calculation

```python
@staticmethod
async def get_outturn(...):
    result = await reports_dao.fetch_outturn(...)
    for row in result.get("rows", []):
        row["outturn_percent"] = (row["kernel_output"] / row["rcn_input"]) * 100
    return result
```

### Pattern 2: Multi-Table Merge

```python
@staticmethod
async def get_batch_summary(...):
    batches = await reports_dao.fetch_batches(...)
    for batch in batches.get("rows", []):
        # Could fetch: boiling, drying, grades, etc.
        batch["processing_status"] = "Complete"
    return batches
```

### Pattern 3: Aggregation with Metrics

```python
@staticmethod
async def get_production_metrics(...):
    rows = await reports_dao.fetch_all(page=1, page_size=10000, ...)
    return {
        "rows": rows["rows"],
        "metrics": {
            "total": len(rows["rows"]),
            "sum": ReportUtilsService.sum_field(rows["rows"], "amount"),
            "avg": ReportUtilsService.average_field(rows["rows"], "amount"),
        }
    }
```

### Pattern 4: Row Enrichment

```python
@staticmethod
async def get_enriched_report(...):
    result = await reports_dao.fetch_report(...)
    calcs = {
        "margin": lambda r: (r["revenue"] - r["cost"]) / r["revenue"] * 100,
        "status": lambda r: "Profit" if r["revenue"] > r["cost"] else "Loss",
    }
    enriched = ReportUtilsService.enrich_rows_with_calculations(
        result.get("rows", []), calcs
    )
    return {"rows": enriched, "total": result.get("total")}
```

---

## Classes Available

```python
# Service methods for each report type
ReportsService.get_rcn_closing_stock(...)
ReportsService.get_outturn(...)
ReportsService.get_nw_percent(...)
ReportsService.get_drying_moisture_loss(...)
ReportsService.get_humidification(...)

# Advanced multi-table services (examples)
AdvancedReportsService.get_batch_processing_summary(...)
AdvancedReportsService.get_production_metrics(...)
AdvancedReportsService.get_quality_report(...)

# Utility functions
ReportUtilsService.calculate_percentage(...)
ReportUtilsService.safe_divide(...)
ReportUtilsService.format_currency(...)
ReportUtilsService.group_by_field(...)
ReportUtilsService.sum_field(...)
ReportUtilsService.average_field(...)
ReportUtilsService.enrich_row_with_calculations(...)
ReportUtilsService.enrich_rows_with_calculations(...)
```

---

## File Locations

```
backend/app/
├── controllers/
│   └── reports_controller.py        ← Endpoints (call service)
├── services/
│   └── reports_service.py           ← Business logic (NEW)
└── dao/
    └── reports_dao.py              ← Database queries
```

---

## Time to Create Report

| Task                    | Time       |
| ----------------------- | ---------- |
| Add service method      | 2 min      |
| Add controller endpoint | 1 min      |
| Add DAO query           | 1 min      |
| **Total**               | **~4 min** |

---

## Complete Example: Outturn Report

### Service (2-3 lines of logic)

```python
@staticmethod
async def get_outturn(...):
    result = await reports_dao.fetch_outturn(...)
    for row in result.get("rows", []):
        rcn_input = row.get("rcn_input_kg", 0)
        if rcn_input > 0:
            row["outturn_percent"] = round((row.get("kernel_output_kg", 0) / rcn_input) * 100, 2)
    return result
```

### Controller (1-line call)

```python
@router.get("/outturn")
async def get_outturn(query: ReportQuery = Depends(), current_user = Depends(get_current_user)):
    return await ReportsService.get_outturn(
        page=query.page, page_size=query.pageSize, sort=query.sort,
        search=query.search, date_from=query.dateFrom, date_to=query.dateTo,
        headers=current_user["headers"],
    )
```

### DAO (1 function call)

```python
async def fetch_outturn(...):
    return await execute_report_query(
        table_name="batch_summary",
        page=page, page_size=page_size, headers=headers,
        select_columns="batch_number,rcn_input_kg,kernel_output_kg,created_at as date",
        **kwargs
    )
```

**Total: ~15 lines of code = Complete working report!**

---

## Key Benefits

✨ **Clean Separation** - Controller, Service, DAO have distinct roles  
✨ **Reusable Logic** - Calculations in service, not scattered  
✨ **Easy Testing** - Service methods testable independently  
✨ **Scalable** - Add complex reports without chaos  
✨ **Maintainable** - Changes in one place affect all reports  
✨ **Flexible** - Support single-table, multi-table, aggregations equally

---

**Documentation:** See `SERVICE_LAYER_SUMMARY.md` for full details

**Backend Guide:** See `backend/app/controllers/REPORTS_SETUP.md` for patterns
