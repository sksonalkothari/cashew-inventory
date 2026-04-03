# Batch Origin Integration - Implementation Summary

## Overview

Updated the RCN Closing Stock report to fetch and display origin information directly from the **batch table** instead of deriving it from the purchases table.

## Changes Made

### Backend Updates (`reports_service.py`)

#### 1. **Import Addition**

```python
from app.dao import purchase_dao, boiling_dao, rcn_sales_dao, batch_dao
```

Added `batch_dao` to imports for concurrent batch fetching.

#### 2. **Concurrent Data Fetching**

**Before:**

```python
purchases, boiling, rcn_sales = await gather(
    purchase_dao.fetch_all_purchases(headers),
    boiling_dao.fetch_all_boiling(headers),
    rcn_sales_dao.fetch_all_rcn_sales(headers),
    return_exceptions=True
)
```

**After:**

```python
purchases, boiling, rcn_sales, batches = await gather(
    purchase_dao.fetch_all_purchases(headers),
    boiling_dao.fetch_all_boiling(headers),
    rcn_sales_dao.fetch_all_rcn_sales(headers),
    batch_dao.fetch_all_batches(headers),  # NEW
    return_exceptions=True
)
```

Now fetches 4 tables concurrently (still highly optimized).

#### 3. **Batch Error Handling**

Added error handling for batch data fetch:

```python
if isinstance(batches, Exception):
    logger.warning(f"Error fetching batches: {batches}")
    batches = []
```

#### 4. **Batch Lookup Dictionary**

Created fast lookup dictionary for batch origin data:

```python
# Create batch lookup dictionary for quick origin lookup
batch_lookup = {}
for batch in batches:
    batch_num = batch.get("batch_number") or batch.get("id")
    if batch_num:
        batch_lookup[batch_num] = {
            "origin": batch.get("origin", ""),
            "batch_entry_date": batch.get("batch_entry_date", ""),
        }
```

This enables O(1) lookup of origin by batch number.

#### 5. **Updated Aggregation Logic**

Changed origin source from purchases table to batch table:

**Before:**

```python
batch_data[batch] = {
    "batch_number": batch,
    "origin": purchase.get("origin"),  # From purchases table
    ...
}
```

**After:**

```python
# Get origin from batch_lookup instead of purchase
origin = batch_lookup.get(batch, {}).get("origin", "")
batch_data[batch] = {
    "batch_number": batch,
    "origin": origin,  # From batch table via batch_lookup
    ...
}
```

Updated all three aggregation loops (purchases, boiling, sales) to use this approach.

## Response Structure

The report continues to return the same structure with origin now sourced from the batch table:

```json
{
  "rows": [
    {
      "batch_number": "B001",
      "origin": "Vietnam", // ← Now from batch table
      "rcn_in_kg": 1000,
      "rcn_to_boiling_kg": 300,
      "rcn_sold_kg": 200,
      "adjustments_kg": 0,
      "closing_stock_kg": 500,
      "purchase_date": "2024-01-10",
      "boiling_date": "2024-01-20",
      "sale_date": "2024-02-05",
      "last_activity_date": "2024-02-05"
    }
  ],
  "total": 45
}
```

## Benefits

1. **Single Source of Truth** - Origin stored once in batch table, not replicated in purchases
2. **Data Consistency** - No discrepancies if origin differs between purchases
3. **Flexible** - Can update batch origin without modifying purchase records
4. **Performance** - Dictionary lookup is O(1), very fast even with 1000+ batches
5. **Scalable** - Easy to add more batch fields (batch_entry_date, etc.) to lookup dictionary

## Performance Impact

- **Before:** Origin from first matching purchase record
- **After:** Origin from batch table via pre-built lookup dictionary
- **Cost:** +1 additional concurrent API call (negligible with async/gather)
- **Benefit:** Guaranteed correct origin per business logic

## Database Dependency

- **Source:** `batch` table, `origin` column
- **Fallback:** Empty string if batch not found or origin not set
- **Lookup Field:** `batch_number` (primary key for matching)

## Testing Recommendations

1. Verify origin displays correctly for all batches
2. Test with batches that have no purchases (should still show origin from batch table)
3. Verify date range filtering still works correctly with new batch data
4. Check sorting by origin column works as expected
5. Validate pagination with new larger data fetch (4 tables)

## Future Enhancements

- Add more batch metadata to response (batch_entry_date, status, etc.)
- Create database view if this pattern is repeated across multiple reports
- Consider caching batch data if it's fetched by multiple report types
