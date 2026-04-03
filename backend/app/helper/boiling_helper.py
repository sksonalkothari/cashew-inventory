from collections import defaultdict
from app.services import batch_summary_service
from app.utils.logger import logger
from app.dao import boiling_dao


class BoilingHelper:

    @staticmethod
    def consolidate_batches(data: list[dict]) -> dict:
        """Consolidate multiple boiling records into a map by batch_number.

        Returns a dict: { batch_number: {"boiling_quantity": float, "created_by": ...} }
        """
        batch_map = defaultdict(lambda: {
            "boiling_quantity": 0,
            "created_by": None,
        })

        for item in data:
            batch_number = item.get("batch_number")
            if batch_number is None:
                continue
            batch_map[batch_number]["boiling_quantity"] += float(item.get("quantity_kg", 0))
            # prefer created_by, fall back to updated_by
            batch_map[batch_number]["created_by"] = batch_map[batch_number].get("created_by") or item.get("created_by") or item.get("updated_by")

        logger.debug(f"Consolidated boiling batch map: {batch_map}")
        return batch_map

    @staticmethod
    async def ensure_batches_exist(batch_map: dict, headers: dict):
        """Ensure a batch_summary entry exists for each batch_number in the map.

        If missing, insert a batch_summary with zero purchase_quantity and boiling_quantity.
        """
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
                    "boiling_quantity": 0
                }], headers)
            else:
                logger.debug(f"Batch already exists: {batch_number}")

    @staticmethod
    async def update_batch_quantities(batch_map: dict, headers: dict):
        """Recalculate and update boiling_quantity in batch_summary for each batch in batch_map.

        This recalculates the total boiling quantity from DB (to avoid incremental drift) and
        writes it to the batch_summary.boiling_quantity field.
        """
        for batch_number, summary in batch_map.items():
            existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
            if existing:
                # fetch all boiling records for this batch and sum quantities
                boiling_records = await boiling_dao.fetch_all_boilings_by_batch_number(batch_number, headers)
                total_quantity = sum(float(r.get('quantity_kg', 0)) for r in boiling_records)

                update_data = {
                    "batch_number": batch_number,
                    "boiling_quantity": total_quantity,
                    "updated_by": summary.get("created_by")
                }

                logger.info(f"Updating boiling_quantity for batch ({batch_number}) to {total_quantity}")
                await batch_summary_service.update_batch(update_data, headers)
            else:
                logger.warning(f"No batch_summary found for ({batch_number}) during boiling update step.")

    @staticmethod
    async def update_boiling_quantity_for_batch(batch_number: str, updated_by: str, headers: dict, total_quantity: float):
        update_data = {"batch_number": batch_number,
                    "boiling_quantity": total_quantity,
                    "updated_by": updated_by}
        await batch_summary_service.update_batch(update_data, headers)