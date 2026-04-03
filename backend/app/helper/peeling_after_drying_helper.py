from collections import defaultdict
from app.services import batch_summary_service
from app.utils.logger import logger
from app.dao import peeling_after_drying_dao


class PeelingAfterDryingHelper:

    @staticmethod
    def consolidate_batches(data: list[dict]) -> dict:
        """Consolidate multiple peeling_after_drying records into a map by batch_number."""
        batch_map = defaultdict(lambda: {"total_quantity": 0, "created_by": None})

        for item in data:
            batch_number = item.get("batch_number")
            if batch_number is None:
                continue
            batch_map[batch_number]["total_quantity"] += float(item.get("total_quantity_kg", 0) or 0)
            batch_map[batch_number]["created_by"] = batch_map[batch_number].get("created_by") or item.get("created_by") or item.get("updated_by")

        logger.debug(f"Consolidated peeling_after_drying batch map: {batch_map}")
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
                    "peeling_after_drying_qty": 0
                }], headers)
            else:
                logger.debug(f"Batch already exists: {batch_number}")

    @staticmethod
    async def update_batch_quantities(batch_map: dict, headers: dict):
        """Recalculate and update peeling_after_drying quantity in batch_summary for each batch in batch_map."""
        for batch_number, summary in batch_map.items():
            existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
            if existing:
                peel_records = await peeling_after_drying_dao.fetch_all_peeling_after_drying_by_batch_number(batch_number, headers)

                total_wholes = sum(float(r.get('wholes_kg', 0) or 0) for r in peel_records)
                total_pieces = sum(float(r.get('pieces_kg', 0) or 0) for r in peel_records)
                total_unpeeled = sum(float(r.get('unpeeled_kg', 0) or 0) for r in peel_records)
                total_swp = sum(float(r.get('swp_kg', 0) or 0) for r in peel_records)
                total_bb = sum(float(r.get('bb_kg', 0) or 0) for r in peel_records)
                total_rejection = sum(float(r.get('rejection_kg', 0) or 0) for r in peel_records)
                total_cutting = sum(float(r.get('cutting_pieces_kg', 0) or 0) for r in peel_records)

                update_data = {
                    "batch_number": batch_number,
                    "peeling_after_drying_pieces_quantity": total_pieces,
                    "peeling_after_drying_unpeeled_quantity": total_unpeeled,
                    "peeling_after_drying_swp_quantity": total_swp,
                    "peeling_after_drying_bb_quantity": total_bb,
                    "peeling_after_drying_rejection_quantity": total_rejection,
                    "peeling_after_drying_cutting_pieces_quantity": total_cutting,
                    "updated_by": summary.get("created_by")
                }

                logger.info(f"Updating peeling_after_drying quantities for batch ({batch_number}) to wholes={total_wholes}, pieces={total_pieces}, unpeeled={total_unpeeled}, swp={total_swp}, bb={total_bb}, rejection={total_rejection}, cutting={total_cutting}")
                await batch_summary_service.update_batch(update_data, headers)
            else:
                logger.warning(f"No batch_summary found for ({batch_number}) during peeling_after_drying update step.")

    @staticmethod
    async def update_peeling_quantity_for_batch(batch_number: str, updated_by: str, headers: dict, totals: dict):
        update_data = {
            "batch_number": batch_number,
            "peeling_after_drying_wholes_quantity": totals.get('total_wholes_kg'),
            "peeling_after_drying_pieces_quantity": totals.get('total_pieces_kg'),
            "peeling_after_drying_unpeeled_quantity": totals.get('total_unpeeled_kg'),
            "peeling_after_drying_swp_quantity": totals.get('total_swp_kg'),
            "peeling_after_drying_bb_quantity": totals.get('total_bb_kg'),
            "peeling_after_drying_rejection_quantity": totals.get('total_rejection_kg'),
            "peeling_after_drying_cutting_pieces_quantity": totals.get('total_cutting_pieces_kg'),
            "updated_by": updated_by
        }

        await batch_summary_service.update_batch(update_data, headers)
