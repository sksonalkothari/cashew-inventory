# Date Handling Strategy for RCN Closing Stock Report

## Problem Statement

Different transactions have different entry dates:

- **Purchase Date** (`purchase_date`) - When RCN was purchased
- **Boiling Date** (`boiling_date`) - When RCN was sent to boiling
- **Sale Date** (`sale_date`) - When RCN was sold

The question: Which date should we display, and how should date range filters work?

## Solution: Latest Activity Date Approach ✅

### Strategy

**Show the `last_activity_date` for each batch as the maximum of all transaction dates**

```
Batch A:
- Purchase: 2024-01-10
- Boiling: 2024-01-20
- Sales: 2024-02-05
→ Last Activity Date: 2024-02-05 (Latest transaction)
→ Closing Stock as of: 2024-02-05
```

### Benefits

1. **Single date per batch** - Easy to understand
2. **Represents current state** - Shows closing stock as of latest activity
3. **Natural business logic** - "Closing stock as of [date]"
4. **Compatible with date filters** - Filter entire batch if ANY date in range

## Date Range Filtering

### How It Works

When user selects a date range (e.g., Jan 1 - Feb 28):

```python
if date_from and date_to:
    # Include batch only if ANY transaction falls within range
    # Include if:
    # - purchase_date is within range, OR
    # - boiling_date is within range, OR
    # - sale_date is within range

    # Calculate closing stock using ALL transactions in system
    # (Not just those in date range)
```

### Example

**Database:**

- Purchase: 2024-01-10 (100 kg)
- Boiling: 2024-01-20 (30 kg)
- Sales: 2024-03-05 (50 kg) ← Outside range if filtering Jan-Feb

**Filter: Jan 1 - Feb 28**

Result:

- ✅ Include Batch A (purchase & boiling dates in range)
- Closing Stock: 100 - 50 - 30 = 20 kg (uses ALL transactions)
- Last Activity: 2024-03-05 (after filter range, but valid)

### Why Include Transactions Outside Date Range?

The closing stock must account for ALL activity that affected the batch, even if some transactions occurred outside the filter range. Otherwise, the calculation would be incorrect.

## Database Fields Involved

| Table     | Date Field      | Type | Purpose                      |
| --------- | --------------- | ---- | ---------------------------- |
| purchases | `purchase_date` | DATE | When RCN was purchased       |
| boiling   | `boiling_date`  | DATE | When RCN was sent to boiling |
| rcn_sales | `sale_date`     | DATE | When RCN was sold            |

## Implementation Details

### Backend (Python - reports_service.py)

```python
# 1. Date filtering at record level
def is_date_in_range(date_str):
    """Check if a single date falls within filter range"""
    if not date_str:
        return True  # Include records with no date

    record_date = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")

    if date_from:
        from_date = datetime.strptime(date_from, "%Y-%m-%d")
        if record_date < from_date:
            return False

    if date_to:
        to_date = datetime.strptime(date_to, "%Y-%m-%d")
        if record_date > to_date:
            return False

    return True

# 2. Track individual dates while aggregating
batch_data[batch] = {
    "purchase_date": earliest_or_first,  # First purchase date
    "boiling_date": latest,              # Latest boiling date
    "sale_date": latest,                 # Latest sale date
}

# 3. Calculate last_activity_date as maximum
dates = [batch["purchase_date"], batch["boiling_date"], batch["sale_date"]]
last_activity_date = max([d for d in dates if d], default="")
```

### Frontend (React - Report.tsx)

```typescript
// Report.tsx automatically displays columns from reportRegistry
// Column definition in reportRegistry.ts:
{
    key: "last_activity_date",
    label: "Last activity",
    sortable: true,
    type: "date"  // Optional: for date formatting
}

// Date range filter
{
    name: "date_from",
    label: "From Date",
    type: "date"
}
{
    name: "date_to",
    label: "To Date",
    type: "date"
}
```

## Report Output Columns

| Column             | Meaning                        | Example    |
| ------------------ | ------------------------------ | ---------- |
| Batch No           | Batch identifier               | A001       |
| Origin             | Where RCN came from            | Vietnam    |
| RCN in (kg)        | Total purchased                | 100        |
| To boiling (kg)    | Sent to boiling                | 30         |
| Sold (kg)          | Total sold                     | 50         |
| Adjustments (kg)   | System adjustments             | 0          |
| Closing stock (kg) | **Purchase - Sales - Boiling** | 20         |
| **Last activity**  | **Latest transaction date**    | 2024-02-05 |

## Future Enhancements (Optional)

### Option 1: Show All Three Dates (Horizontal Expansion)

```
| Batch | Origin | RCN in | Purchased | Boiled | Sold | Closing Stock |
```

### Option 2: Running Balance Report

```
| Batch | Date | Type | Qty | Running Balance |
| A001 | 2024-01-10 | Purchase | +100 | 100 |
| A001 | 2024-01-20 | Boiling | -30 | 70 |
| A001 | 2024-02-05 | Sales | -50 | 20 |
```

### Option 3: Multiple Rows Per Batch

Show separate rows for each transaction event (more detailed but complex)

---

## Summary

✅ **What's Implemented:**

- Concurrent fetching from 3 tables (purchases, boiling, rcn_sales)
- Date filtering on individual transactions
- Track individual dates per transaction type
- Calculate `last_activity_date` as max of all dates
- Include in report output for visibility

✅ **Date Range Filters Apply To:**

- Only include batch if ANY transaction is in date range
- Calculate closing stock using ALL transactions (entire batch history)
- Show latest activity date (may be outside filter range)

✅ **Closing Stock Formula:**
`Closing Stock = Purchase Quantity - Sales Quantity - Boiling Quantity`
