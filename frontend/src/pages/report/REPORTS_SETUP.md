# Reports Infrastructure Setup Guide

## Overview

This document explains the new scalable report infrastructure for the Cashew Inventory Management App. It provides a unified, simple way to create and manage reports across the application.

## Architecture

The infrastructure consists of three layers:

### 1. Frontend Layer (`src/pages/report/`)

- **reportRegistry.ts** - Central registry of all reports with metadata
- **createSimpleReport.tsx** - Factory function to generate report components with minimal code
- Individual report components (RCNClosingStock.tsx, Outturn.tsx, etc.)

### 2. Backend Layer (`app/controllers/` and `app/dao/`)

- **reports_controller.py** - API endpoints for all reports
- **reports_dao.py** - Generic data access utilities and report-specific queries

### 3. Data Layer

- Supabase PostgreSQL database tables and views

---

## How It Works

### Frontend Flow

```
Report Registry
    ↓
createSimpleReport(config)  ← Minimal boilerplate
    ↓
ReportView Component        ← Handles UI (table, sorting, filtering, export)
    ↓
fetchDefinedReport (API)    ← Calls backend endpoint
```

### Backend Flow

```
API Request (/api/v1/reports/*)
    ↓
reports_controller.py       ← Route handler + query parsing
    ↓
reports_dao.py              ← Build & execute database query
    ↓
Supabase                    ← Fetch data
    ↓
Response (rows + total)
```

---

## Creating a New Report

### Step 1: Add to Frontend Registry

Edit `frontend/src/pages/report/reportRegistry.ts`:

```typescript
export const REPORTS_REGISTRY: Record<string, ReportConfig> = {
  // ... existing reports ...

  "my-new-report": {
    id: "my-new-report",
    title: "My New Report",
    subtitle: "Description of what this report shows",
    description: "Longer explanation (optional)",
    endpoint: "/api/v1/reports/my-new-report",
    category: "Stock", // Group reports by category
    tags: ["keyword1", "keyword2"], // For searching
    icon: "📊", // Optional emoji
    columns: [
      {
        key: "field_name",
        label: "Display Label",
        sortable: true,
        type: "number",
      },
      // ... more columns
    ],
  },
};
```

#### Column Definition Format

```typescript
type ColumnDef<T> = {
  key: keyof T | string; // Field name from API response
  label: string; // Display label in table header
  type?: "string" | "number" | "date"; // Data type (for formatting)
  width?: number; // Optional column width in pixels
  sortable?: boolean; // Allow sorting on this column
  filterable?: boolean; // Allow filtering (not yet implemented)
  render?: (
    value: any,
    row: T
  ) => // Custom rendering function
  React.ReactNode;
};
```

### Step 2: Create Frontend Component

Create `frontend/src/pages/report/MyNewReport.tsx`:

```typescript
import { createSimpleReport } from "./createSimpleReport";
import type { ColumnDef } from "../../types/reportingTypes";

type MyReportRow = {
  batch_number: string;
  quantity_kg: number;
  date: string;
};

const columns: ColumnDef<MyReportRow>[] = [
  { key: "batch_number", label: "Batch No", sortable: true },
  {
    key: "quantity_kg",
    label: "Quantity (kg)",
    type: "number",
    sortable: true,
  },
  { key: "date", label: "Date", type: "date", sortable: true },
];

export default createSimpleReport<MyReportRow>({
  title: "My New Report",
  subtitle: "Description of the report",
  endpoint: "/api/v1/reports/my-new-report",
  columns,
  icon: "📊",
  initialPageSize: 10,
  exportFilename: "my_new_report.csv",
});
```

That's it! No need for `useCallback`, `useState`, or `useEffect` boilerplate.

### Step 3: Add Backend Endpoint

Edit `backend/app/controllers/reports_controller.py`:

```python
@router.get("/my-new-report", summary="My New Report")
async def get_my_new_report(
    query: ReportQuery = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """Report description..."""
    logger.info("Fetching my new report")
    try:
        result = await reports_dao.fetch_my_new_report(
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
        logger.error(f"Error fetching my new report: {e}")
        raise
```

### Step 4: Add Backend DAO Query

Edit `backend/app/dao/reports_dao.py`:

```python
async def fetch_my_new_report(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch my new report data.
    """
    return await execute_report_query(
        table_name="batch_summary",  # or your table name
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        select_columns="batch_number,quantity_kg,created_at as date",
    )
```

### Step 5: Register Route in Backend

Edit `backend/app/main.py`:

Already done - just ensure `reports_controller` is imported and registered:

```python
from app.controllers import ... reports_controller

api_v1_router.include_router(reports_controller.router)
```

---

## Query Parameters

All report endpoints support the following query parameters:

| Parameter  | Type   | Example                  | Description                                            |
| ---------- | ------ | ------------------------ | ------------------------------------------------------ |
| `page`     | int    | `?page=1`                | Page number (1-indexed)                                |
| `pageSize` | int    | `?pageSize=25`           | Items per page                                         |
| `sort`     | string | `?sort=batch_number:asc` | Sort by column (format: `column:asc` or `column:desc`) |
| `search`   | string | `?search=batch123`       | Global search across text fields                       |
| `dateFrom` | string | `?dateFrom=2025-01-01`   | Filter from date (ISO format)                          |
| `dateTo`   | string | `?dateTo=2025-01-31`     | Filter to date (ISO format)                            |

### Example Requests

```
GET /api/v1/reports/rcn-closing-stock?page=1&pageSize=25&sort=batch_number:asc

GET /api/v1/reports/outturn?page=1&pageSize=10&search=batch&dateFrom=2025-01-01&dateTo=2025-01-31

GET /api/v1/reports/humidification?page=2&pageSize=50&sort=outturn_percent:desc
```

---

## Advanced Usage

### Custom Report Rendering

If you need custom rendering for specific columns:

```typescript
const columns: ColumnDef<MyRow>[] = [
  {
    key: "batch_number",
    label: "Batch",
    sortable: true,
    render: (value, row) => <Link to={`/batch/${value}`}>{value}</Link>,
  },
  {
    key: "percentage",
    label: "Progress",
    render: (value) => <ProgressBar value={value} />,
  },
];
```

### Using Hook Pattern for Dynamic Reports

If you need more control than `createSimpleReport`:

```typescript
import { useReportConfig } from "./createSimpleReport";
import { ReportView } from "../../components/ReportView";

export function MyDynamicReport() {
  const reportConfig = useReportConfig({
    title: "Dynamic Report",
    subtitle: "...",
    endpoint: "/api/v1/reports/my-report",
    columns: [...],
  });

  // Optionally modify config
  const customColumns = reportConfig.columns.map(col => ({
    ...col,
    // ... modifications
  }));

  return (
    <ReportView
      {...reportConfig}
      columns={customColumns}
    />
  );
}
```

### Getting All Reports Metadata

Use these utility functions from `reportRegistry.ts`:

```typescript
import {
  getAllReportsMetadata,
  getReportsByCategory,
  searchReports,
} from "./reportRegistry";

// Get all reports with metadata
const allReports = getAllReportsMetadata();

// Group reports by category
const byCategory = getReportsByCategory();
// Output: { "Stock": [...], "Production": [...], "Process": [...] }

// Search reports
const results = searchReports("moisture");
// Searches title, description, and tags
```

---

## Backend Implementation Patterns

### Simple Query (Single Table)

For queries that fetch from a single table:

```python
async def fetch_simple_report(
    page: int,
    page_size: int,
    headers: dict,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    return await execute_report_query(
        table_name="batch_summary",
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

### Complex Query (Multiple Tables / Calculations)

For more complex queries, consider creating database views in Supabase:

```sql
-- In Supabase SQL editor
CREATE VIEW outturn_report AS
SELECT
  b.batch_number,
  b.rcn_in_kg,
  SUM(g.kernel_output_kg) as kernel_output_kg,
  ROUND(
    (SUM(g.kernel_output_kg) / b.rcn_in_kg) * 100, 2
  ) as outturn_percent,
  b.created_at as date
FROM batch_summary b
LEFT JOIN grades g ON b.id = g.batch_id
GROUP BY b.id, b.batch_number, b.rcn_in_kg, b.created_at;
```

Then query the view:

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
    return await execute_report_query(
        table_name="outturn_report",  # Use view name
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )
```

### Filtering with Extra Parameters

Add domain-specific filters:

```python
async def fetch_report_by_location(
    page: int,
    page_size: int,
    headers: dict,
    location: Optional[str] = None,  # New parameter
    sort: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    return await execute_report_query(
        table_name="batch_summary",
        page=page,
        page_size=page_size,
        headers=headers,
        sort=sort,
        search=search,
        date_from=date_from,
        date_to=date_to,
        extra_filters={"location": location} if location else None,
    )
```

---

## Existing Reports

The following reports have been created with the new infrastructure:

1. **RCN Closing Stock** (`RCNClosingStock.tsx`)

   - Tracks raw cashew nut inventory by batch
   - Endpoint: `/api/v1/reports/rcn-closing-stock`

2. **Outturn** (`Outturn.tsx`)

   - Yield percentage analysis
   - Endpoint: `/api/v1/reports/outturn`

3. **NW Percent** (`NWPercent.tsx`)

   - Net weight percentage analysis
   - Endpoint: `/api/v1/reports/nw-percent`

4. **Drying Moisture Loss** (`DryingMoistureLoss.tsx`)

   - Moisture reduction during drying
   - Endpoint: `/api/v1/reports/drying-moisture-loss`

5. **Humidification** (`Humidification.tsx`)
   - Moisture rehydration tracking
   - Endpoint: `/api/v1/reports/humidification`

---

## File Structure

```
frontend/
  src/pages/report/
    reportRegistry.ts          ← Central registry of all reports
    createSimpleReport.tsx      ← Report component factory
    RCNClosingStock.tsx        ← Report components (minimal code)
    Outturn.tsx
    NWPercent.tsx
    DryingMoistureLoss.tsx
    Humidification.tsx
    demo/                      ← Demo/reference implementations
      DemoReportPage.tsx
      dummyColumns.ts
      dummyData.ts
      fakeFetch.ts

backend/
  app/controllers/
    reports_controller.py      ← All report endpoints
  app/dao/
    reports_dao.py            ← Generic query builder + specific queries
  app/exceptions/
    exceptions.py             ← ReportError exception
  main.py                      ← Register reports_controller
```

---

## Best Practices

1. **Keep Components Simple**

   - Use `createSimpleReport()` for standard reports
   - Only use the hook pattern if you need custom logic

2. **Organize by Category**

   - Use `category` field in registry to group related reports
   - Makes navigation and search easier

3. **Tag Reports**

   - Add relevant tags for better searchability
   - Users can search reports across the app

4. **Database Views**

   - For complex calculations, create Supabase views
   - Simplifies backend code and improves performance

5. **Error Handling**

   - Both frontend and backend have error handling built-in
   - ReportError is automatically caught and formatted

6. **Pagination**
   - Always paginate large datasets
   - Default page size is 25, adjustable via URL parameter

---

## Troubleshooting

### Report returns empty data

1. Check the endpoint in `reportRegistry.ts`
2. Verify the table/view exists in Supabase
3. Check column names match your database schema
4. Ensure date filters are in ISO format (YYYY-MM-DD)

### Sorting not working

1. Ensure column is marked as `sortable: true`
2. Verify sort parameter format: `column:asc` or `column:desc`
3. Check column name matches database field name

### Search not finding results

- Global search is client-side filtering
- Searches all text values in returned rows
- For server-side search, implement custom filtering in DAO

### Performance issues with large datasets

1. Reduce page size via `initialPageSize` or URL parameter
2. Add indexes to frequently sorted/filtered columns
3. Use database views for complex calculations
4. Consider pagination boundaries (don't fetch all at once)

---

## Summary

The new report infrastructure makes it easy to:

✅ Add new reports with minimal code (~30 lines of frontend + 1 function call on backend)
✅ Maintain consistent UI/UX across all reports
✅ Reuse filtering, sorting, pagination, export functionality
✅ Scale to many reports without complexity
✅ Organize reports by category and tags
✅ Handle errors gracefully

Happy reporting! 📊
