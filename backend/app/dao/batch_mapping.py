def map_batch_to_batchlistitem(batch_row, user_lookup=None):
    # user_lookup: dict of {uuid: name} for fast lookup, or None to skip names
    def stage_obj(status, updated_at, updated_by):
        obj = {"status": status or "Not_Started"}
        if updated_at:
            obj["updated_at"] = updated_at.isoformat() if hasattr(updated_at, 'isoformat') else str(updated_at)
        if updated_by and user_lookup:
            obj["updated_by_name"] = user_lookup.get(updated_by)
        return obj

    return {
        "batchNumber": batch_row["batch_number"],
        "origin": batch_row.get("origin", ""),
        "intake_date": str(batch_row.get("batch_entry_date") or batch_row.get("date")),
        "stages": {
            "purchase": stage_obj(batch_row.get("purchase_status"), batch_row.get("purchase_updated_at"), batch_row.get("purchase_updated_by")),
            "boiling": stage_obj(batch_row.get("boiling_status"), batch_row.get("boiling_updated_at"), batch_row.get("boiling_updated_by")),
            "nw_drying": stage_obj(batch_row.get("nw_drying_status"), batch_row.get("nw_drying_updated_at"), batch_row.get("nw_drying_updated_by")),
            "nw_humidification": stage_obj(batch_row.get("nw_humidification_status"), batch_row.get("nw_humidification_updated_at"), batch_row.get("nw_humidification_updated_by")),
            "peeling_before_drying": stage_obj(batch_row.get("peeling_before_drying_status"), batch_row.get("peeling_before_drying_updated_at"), batch_row.get("peeling_before_drying_updated_by")),
            "peeling_after_drying": stage_obj(batch_row.get("peeling_after_drying_status"), batch_row.get("peeling_after_drying_updated_at"), batch_row.get("peeling_after_drying_updated_by")),
            "production": stage_obj(batch_row.get("production_status"), batch_row.get("production_updated_at"), batch_row.get("production_updated_by")),
            "cashew_kernel_sales": stage_obj(batch_row.get("cashew_kernel_sales_status"), batch_row.get("cashew_kernel_sales_updated_at"), batch_row.get("cashew_kernel_sales_updated_by")),
            # Add rcn_sales if needed
        },
    }
