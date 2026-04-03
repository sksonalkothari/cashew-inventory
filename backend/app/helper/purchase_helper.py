from collections import defaultdict
from app.services import batch_summary_service
from app.utils.logger import logger

class PurchaseHelper:

    @staticmethod
    def consolidate_batches(data: list[dict]) -> dict:
        batch_map = defaultdict(lambda: {
            "purchase_quantity": 0,
            "origin": None,
            "status": "Purchased",
            "created_by": None
        })

        for item in data:
            batch_number = item["batch_number"]
            batch_map[batch_number]["purchase_quantity"] += float(item["quantity_kg"])
            batch_map[batch_number]["origin"] = item["origin"]
            batch_map[batch_number]["created_by"] = item["created_by"]

        logger.debug(f"Consolidated batch map: {batch_map}")
        return batch_map

    @staticmethod
    async def ensure_batches_exist(batch_map: dict, headers: dict):
        for batch_number, summary in batch_map.items():
            existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
            if not existing:
                logger.debug(f"Batch not found: {batch_number}")
                logger.info(f"Inserting new batch_summary for batch_number: {batch_number}")
                await batch_summary_service.insert_batch([{
                    "batch_number": batch_number,
                    "origin": summary["origin"],
                    "status": summary["status"],
                    "created_by": summary["created_by"],
                    "purchase_quantity": 0
                }], headers)
            else:
                logger.debug(f"Batch already exists: {batch_number}")

    @staticmethod
    async def update_batch_quantities(batch_map: dict, headers: dict):
        for batch_number, summary in batch_map.items():
            existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
            if existing:
                record = existing[0]
                updated_quantity = float(record["purchase_quantity"]) + summary["purchase_quantity"]

                update_data = {
                    "batch_number": batch_number,
                    "origin": record["origin"],
                    "purchase_quantity": updated_quantity,
                    "updated_by": summary["created_by"]
                }

                logger.info(f"Updating purchase_quantity for batch ({batch_number}) to {updated_quantity}")
                await batch_summary_service.update_batch(update_data, headers)
            else:
                logger.warning(f"No batch_summary found for ({batch_number}) during update step.")

    @staticmethod
    async def handle_batch_adjustments(old, new, updated_by, headers):
        new_qty = float(new["quantity_kg"])
        old_qty = float(old["quantity_kg"])

        batch_changed = old["batch_number"] != new["batch_number"]
        quantity_changed = old_qty != new_qty
        origin_changed = old["origin"] != new["origin"]

        if batch_changed or quantity_changed:
            logger.info(f"Adjusting batch summaries due to changes in batch or quantity for purchase ID {old['id']}")
            await PurchaseHelper.adjust_batch_summary_after_removal(
                old["batch_number"], old_qty, updated_by, headers
            )
            await PurchaseHelper.ensure_batch_exists_and_update(
                new["batch_number"], new["origin"], new_qty, updated_by, headers
            )
        elif origin_changed:
            logger.info(f"Updating origin for batch {new['batch_number']} due to change in purchase ID {old['id']}")
            await PurchaseHelper.update_batch_origin_if_changed(
                new["batch_number"], new["origin"], updated_by, headers
            )

    @staticmethod
    async def adjust_batch_summary_after_removal(batch_number: str, quantity_to_remove: float, updated_by: str, headers: dict):
        batch = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
        if not batch:
            logger.warning(f"No batch_summary found for {batch_number}")
            return

        record = batch[0]
        current_qty = float(record["purchase_quantity"])
        new_qty = max(0, current_qty - quantity_to_remove)

        if new_qty == 0 or abs(new_qty - 0.0) < 1e-6:
            logger.info(f"Updating batch_summary for {batch_number} to new quantity: {new_qty}")
            await batch_summary_service.update_batch({
                "batch_number": batch_number,
                "purchase_quantity": new_qty,
                "updated_by": updated_by
            }, headers)
            logger.info(f"Soft-deleting batch_summary for {batch_number} as quantity matches deleted record")
            await batch_summary_service.soft_delete_batch({
                "batch_number": batch_number,
                "updated_by": updated_by
            }, headers)
        else:
            logger.info(f"Updating batch_summary for {batch_number} to new quantity: {new_qty}")
            await batch_summary_service.update_batch({
                "batch_number": batch_number,
                "purchase_quantity": new_qty,
                "updated_by": updated_by
            }, headers)

    @staticmethod
    async def ensure_batch_exists_and_update(batch_number: str, origin: str, quantity: float, updated_by: str, headers: dict):
        existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
        if not existing:
            logger.info(f"Inserting new batch_summary for {batch_number}")
            await batch_summary_service.insert_batch([{
                "batch_number": batch_number,
                "origin": origin,
                "status": "Purchased",
                "created_by": updated_by,
                "purchase_quantity": quantity
            }], headers)
        else:
            record = existing[0]
            new_total = float(record["purchase_quantity"]) + quantity
            logger.info(f"Updating batch_summary for {batch_number} to {new_total}")
            await batch_summary_service.update_batch({
                "batch_number": batch_number,
                "purchase_quantity": new_total,
                "updated_by": updated_by
            }, headers)

    @staticmethod
    async def update_batch_origin_if_changed(batch_number: str, new_origin: str, updated_by: str, headers: dict):
        batch = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
        if not batch:
            logger.warning(f"No batch_summary found for {batch_number}")
            return

        record = batch[0]
        current_origin = record.get("origin")

        if current_origin != new_origin:
            logger.info(f"Updating origin for batch {batch_number} from '{current_origin}' to '{new_origin}'")
            await batch_summary_service.update_batch({
                "batch_number": batch_number,
                "origin": new_origin,
                "updated_by": updated_by
            }, headers)