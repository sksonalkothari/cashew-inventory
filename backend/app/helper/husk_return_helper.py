from collections import defaultdict
from app.services import batch_summary_service
from app.utils.logger import logger
from app.dao import husk_return_dao


class HuskReturnHelper:

    @staticmethod
    def consolidate_batches(data: list[dict]) -> dict:
        """Consolidate multiple husk_return records into a map by batch_number."""
        batch_map = defaultdict(lambda: {"total_quantity": 0, "created_by": None})

        for item in data:
            batch_number = item.get("batch_number")
            if batch_number is None:
                continue
            batch_map[batch_number]["total_quantity"] += float(item.get("total_quantity_kg", 0) or 0)
            batch_map[batch_number]["created_by"] = batch_map[batch_number].get("created_by") or item.get("created_by") or item.get("updated_by")

        logger.debug(f"Consolidated husk_return batch map: {batch_map}")
        return batch_map

    @staticmethod
    async def ensure_batches_exist(batch_map: dict, headers: dict):
        for batch_number, summary in batch_map.items():
            existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
            if not existing:
                logger.info(f"Inserting new batch_summary for batch_number: {batch_number}")
                await batch_summary_service.insert_batch([{
                    "batch_number": batch_number,
                    "origin": None,
                    "status": "Purchased",
                    "created_by": summary.get("created_by"),
                    "purchase_quantity": 0,
                    "husk_return_quantity": 0
                }], headers)
            else:
                logger.debug(f"Batch already exists: {batch_number}")

    @staticmethod
    async def update_batch_quantities(batch_map: dict, headers: dict):
        """Recalculate and update husk_return quantity in batch_summary for each batch in batch_map."""
        for batch_number, summary in batch_map.items():
            existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
            if existing:
                husk_records = await husk_return_dao.fetch_all_husk_return_by_batch_number(batch_number, headers)
                total_husk_qty = sum(float(r.get('total_quantity_kg', 0) or 0) for r in husk_records)

                update_data = {
                    "batch_number": batch_number,
                    "husk_return_quantity": total_husk_qty,
                    "updated_by": summary.get("created_by")
                }

                logger.info(f"Updating husk_return quantity for batch ({batch_number}) to {total_husk_qty}")
                await batch_summary_service.update_batch(update_data, headers)
            else:
                logger.warning(f"No batch_summary found for ({batch_number}) during husk_return update step.")

    @staticmethod
    async def update_husk_quantity_for_batch(batch_number: str, updated_by: str, headers: dict, totals: dict):
        update_data = {"batch_number": batch_number,
                       "husk_return_quantity": totals.get('total_quantity_kg'),
                       "updated_by": updated_by}
        await batch_summary_service.update_batch(update_data, headers)
