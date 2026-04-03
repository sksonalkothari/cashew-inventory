# Reports Infrastructure - Quick Reference

## Create a New Report in 5 Minutes

### Frontend (3 steps)

**Step 1: Add to registry** (`frontend/src/pages/report/reportRegistry.ts`)

```typescript
"my-report": {
  id: "my-report",
  title: "My Report",
  subtitle: "Description",
  endpoint: "/api/v1/reports/my-report",
  category: "Stock",
  tags: ["keyword"],
  columns: [
    { key: "field", label: "Label", sortable: true, type: "number" },
  ],
},
```

**Step 2: Create component** (`frontend/src/pages/report/MyReport.tsx`)

```typescript
import { createSimpleReport } from "./createSimpleReport";

type Row = { field: number };

const columns = [{ key: "field", label: "Label", sortable: true }];

export default createSimpleReport<Row>({
  title: "My Report",
  subtitle: "Description",
  endpoint: "/api/v1/reports/my-report",
  columns,
  initialPageSize: 10,
  exportFilename: "my_report.csv",
});
```

**Step 3: Done!** ✅

### Backend (2 steps)

**Step 1: Add endpoint** (`backend/app/controllers/reports_controller.py`)

```python
@router.get("/my-report", summary="My Report")
async def get_my_report(query: ReportQuery = Depends(), current_user: dict = Depends(get_current_user)):
    logger.info("Fetching my report")
    try:
        result = await reports_dao.fetch_my_report(
            page=query.page, page_size=query.pageSize, sort=query.sort,
            search=query.search, date_from=query.dateFrom, date_to=query.dateTo,
            headers=current_user["headers"],
        )
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

**Step 2: Add DAO query** (`backend/app/dao/reports_dao.py`)

```python
async def fetch_my_report(page: int, page_size: int, headers: dict, sort=None, search=None, date_from=None, date_to=None):
    return await execute_report_query(
        table_name="my_table",
        page=page, page_size=page_size, headers=headers,
        sort=sort, search=search, date_from=date_from, date_to=date_to,
        select_columns="col1,col2,col3",
    )
```

**Done!** ✅

---

## Key Files

| File                                               | Purpose                                |
| -------------------------------------------------- | -------------------------------------- |
| `frontend/src/pages/report/reportRegistry.ts`      | Central registry of all reports        |
| `frontend/src/pages/report/createSimpleReport.tsx` | Factory for creating report components |
| `backend/app/controllers/reports_controller.py`    | All report endpoints                   |
| `backend/app/dao/reports_dao.py`                   | Query builder and data access          |
| `frontend/src/pages/report/REPORTS_SETUP.md`       | Frontend detailed guide                |
| `backend/app/controllers/REPORTS_SETUP.md`         | Backend detailed guide                 |

---

## Query Parameters

All endpoints support:

```
?page=1                          # Page (1-indexed)
&pageSize=25                     # Items per page
&sort=column:asc                 # Sort by column (asc/desc)
&search=term                     # Global search
&dateFrom=2025-01-01             # Start date (ISO)
&dateTo=2025-01-31               # End date (ISO)
```

Example:

```
GET /api/v1/reports/rcn-closing-stock?page=1&pageSize=10&sort=batch_number:asc&dateFrom=2025-01-01
```

---

## Column Definition

```typescript
type ColumnDef<T> = {
  key: keyof T; // Field name
  label: string; // Display label
  type?: "string" | "number" | "date"; // Data type
  width?: number; // Width in pixels
  sortable?: boolean; // Allow sorting
  render?: (value, row) => React.ReactNode; // Custom render
};
```

---

## Example: Sales Report

### Frontend

**registry.ts**

```typescript
"kernel-sales": {
  id: "kernel-sales",
  title: "Kernel Sales",
  subtitle: "Cashew kernel sales tracking",
  endpoint: "/api/v1/reports/kernel-sales",
  category: "Sales",
  tags: ["sales", "kernel"],
  columns: [
    { key: "batch_number", label: "Batch", sortable: true },
    { key: "quantity_kg", label: "Qty (kg)", type: "number", sortable: true },
    { key: "price_per_kg", label: "Price (₹/kg)", type: "number", sortable: true },
    { key: "total_amount", label: "Total (₹)", type: "number", sortable: true },
    { key: "date", label: "Date", type: "date", sortable: true },
  ],
},
```

**KernelSales.tsx**

```typescript
import { createSimpleReport } from "./createSimpleReport";

type KernelSalesRow = {
  batch_number: string;
  quantity_kg: number;
  price_per_kg: number;
  total_amount: number;
  date: string;
};

const columns = [
  /* from registry */
];

export default createSimpleReport<KernelSalesRow>({
  title: "Kernel Sales",
  subtitle: "Cashew kernel sales tracking",
  endpoint: "/api/v1/reports/kernel-sales",
  columns,
  exportFilename: "kernel_sales.csv",
});
```

### Backend

**reports_controller.py**

```python
@router.get("/kernel-sales")
async def get_kernel_sales(query: ReportQuery = Depends(), current_user = Depends(get_current_user)):
    logger.info("Fetching kernel sales")
    return await reports_dao.fetch_kernel_sales(
        page=query.page, page_size=query.pageSize, sort=query.sort,
        search=query.search, date_from=query.dateFrom, date_to=query.dateTo,
        headers=current_user["headers"],
    )
```

**reports_dao.py**

```python
async def fetch_kernel_sales(page: int, page_size: int, headers: dict, **kwargs):
    return await execute_report_query(
        table_name="cashew_kernel_sales",
        page=page, page_size=page_size, headers=headers,
        select_columns="batch_number,quantity_kg,price_per_kg,total_amount,created_at as date",
        **kwargs
    )
```

---

## Features Included

✅ **Pagination** - Automatic offset-based pagination  
✅ **Sorting** - Sort by any column (asc/desc)  
✅ **Search** - Global text search across all fields  
✅ **Filtering** - Date range and custom filters  
✅ **Export** - Download as CSV  
✅ **Responsive** - Mobile-friendly table UI  
✅ **Error Handling** - Built-in error messages  
✅ **Performance** - Pagination prevents data overload  
✅ **Security** - RLS integration via auth headers

---

## Using Reports Utilities

Get all reports:

```typescript
import { getAllReportsMetadata } from "./reportRegistry";
const reports = getAllReportsMetadata();
```

Get reports by category:

```typescript
import { getReportsByCategory } from "./reportRegistry";
const grouped = getReportsByCategory();
// { "Stock": [...], "Sales": [...], ... }
```

Search reports:

```typescript
import { searchReports } from "./reportRegistry";
const results = searchReports("moisture");
```

---

## Common Patterns

### With Custom Rendering

```typescript
const columns: ColumnDef<Row>[] = [
  {
    key: "amount",
    label: "Amount",
    render: (value) => `₹${value.toLocaleString()}`,
  },
];
```

### With Custom Filter

```typescript
@router.get("/report")
async def get_report(
    query: ReportQuery = Depends(),
    location: str = Query(None),  // Custom param
    current_user = Depends(get_current_user),
):
    return await reports_dao.fetch_report(
        ..., extra_filters={"location": location}, ...
    )
```

### With Database View

```python
# Create view in Supabase
CREATE VIEW sales_summary AS
SELECT batch_number, SUM(qty) as total, COUNT(*) as transactions
FROM cashew_kernel_sales GROUP BY batch_number;

# Then query it
async def fetch_sales_summary(...):
    return await execute_report_query(
        table_name="sales_summary",  # Use view name
        ...
    )
```

---

## Response Format

```json
{
  "rows": [
    { "batch_number": "B001", "quantity_kg": 100, "date": "2025-01-26" },
    { "batch_number": "B002", "quantity_kg": 150, "date": "2025-01-26" }
  ],
  "total": 245
}
```

---

## Testing

**curl:**

```bash
curl "http://localhost:8000/api/v1/reports/rcn-closing-stock?page=1&pageSize=10"
```

**With auth header:**

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/v1/reports/rcn-closing-stock?page=1"
```

---

## Checklist for New Report

- [ ] Add to `reportRegistry.ts`
- [ ] Create component file
- [ ] Add endpoint to `reports_controller.py`
- [ ] Add DAO function to `reports_dao.py`
- [ ] Verify table/view exists in Supabase
- [ ] Test endpoint with curl or Postman
- [ ] Check data displays in frontend
- [ ] Test filtering, sorting, pagination
- [ ] Test export functionality
- [ ] Done! 🎉

---

## Troubleshooting

| Issue          | Solution                                            |
| -------------- | --------------------------------------------------- |
| 404 Not Found  | Check endpoint name matches registry and controller |
| Empty data     | Verify table name and column names in DAO           |
| Sorting broken | Check sort format: `column:asc` or `column:desc`    |
| Slow queries   | Add indexes, reduce pageSize, use specific columns  |
| Auth errors    | Verify JWT token, check RLS policies                |

---

## Full Documentation

- **Frontend details:** `frontend/src/pages/report/REPORTS_SETUP.md`
- **Backend details:** `backend/app/controllers/REPORTS_SETUP.md`

---

**Time to create a new report: ~5 minutes** ⚡
