from collections import defaultdict
from app.services import batch_summary_service
from app.utils.logger import logger
from app.dao import drying_dao


class DryingHelper:

    @staticmethod
    def consolidate_batches(data: list[dict]) -> dict:
        """Consolidate multiple drying records into a map by batch_number.

        Returns a dict: { batch_number: {<sum fields>, "created_by": ...} }
        """
        batch_map = defaultdict(lambda: {
            "nw_wholes_in": 0,
            "nw_pieces_in": 0,
            "nw_rejection_in": 0,
            "nw_wholes_out": 0,
            "nw_pieces_out": 0,
            "nw_rejection_out": 0,
            "created_by": None,
        })

        for item in data:
            batch_number = item.get("batch_number")
            if batch_number is None:
                continue
            batch_map[batch_number]["nw_wholes_in"] += float(item.get("nw_wholes_in_kg", 0) or 0)
            batch_map[batch_number]["nw_pieces_in"] += float(item.get("nw_pieces_in_kg", 0) or 0)
            batch_map[batch_number]["nw_rejection_in"] += float(item.get("nw_rejection_in_kg", 0) or 0)
            batch_map[batch_number]["nw_wholes_out"] += float(item.get("nw_wholes_out_kg", 0) or 0)
            batch_map[batch_number]["nw_pieces_out"] += float(item.get("nw_pieces_out_kg", 0) or 0)
            batch_map[batch_number]["nw_rejection_out"] += float(item.get("nw_rejection_out_kg", 0) or 0)
            batch_map[batch_number]["created_by"] = batch_map[batch_number].get("created_by") or item.get("created_by") or item.get("updated_by")

        logger.debug(f"Consolidated drying batch map: {batch_map}")
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
                    "drying_nw_wholes_in_quantity": 0,
                    "drying_nw_pieces_in_quantity": 0,
                    "drying_nw_rejection_in_quantity": 0,
                    "drying_nw_wholes_out_quantity": 0,
                    "drying_nw_pieces_out_quantity": 0,
                    "drying_nw_rejection_out_quantity": 0
                }], headers)
            else:
                logger.debug(f"Batch already exists: {batch_number}")

    @staticmethod
    async def update_batch_quantities(batch_map: dict, headers: dict):
        """Recalculate and update drying-related quantities in batch_summary for each batch in batch_map."""
        for batch_number, summary in batch_map.items():
            existing = await batch_summary_service.fetch_batch_by_number(batch_number, headers)
            if existing:
                # fetch all drying records for this batch and sum quantities
                drying_records = await drying_dao.fetch_all_drying_by_batch_number(batch_number, headers)
                total_nw_wholes_in = sum(float(r.get('nw_wholes_in_kg', 0) or 0) for r in drying_records)
                total_nw_pieces_in = sum(float(r.get('nw_pieces_in_kg', 0) or 0) for r in drying_records)
                total_nw_rejection_in = sum(float(r.get('nw_rejection_in_kg', 0) or 0) for r in drying_records)
                total_nw_wholes_out = sum(float(r.get('nw_wholes_out_kg', 0) or 0) for r in drying_records)
                total_nw_pieces_out = sum(float(r.get('nw_pieces_out_kg', 0) or 0) for r in drying_records)
                total_nw_rejection_out = sum(float(r.get('nw_rejection_out_kg', 0) or 0) for r in drying_records)

                update_data = {
                    "batch_number": batch_number,
                    "drying_nw_wholes_in_quantity": total_nw_wholes_in,
                    "drying_nw_pieces_in_quantity": total_nw_pieces_in,
                    "drying_nw_rejection_in_quantity": total_nw_rejection_in,
                    "drying_nw_wholes_out_quantity": total_nw_wholes_out,
                    "drying_nw_pieces_out_quantity": total_nw_pieces_out,
                    "drying_nw_rejection_out_quantity": total_nw_rejection_out,
                    "updated_by": summary.get("created_by")
                }

                logger.info(f"Updating drying quantities for batch ({batch_number}) to {update_data}")
                await batch_summary_service.update_batch(update_data, headers)
            else:
                logger.warning(f"No batch_summary found for ({batch_number}) during drying update step.")

    @staticmethod
    async def update_drying_quantity_for_batch(batch_number: str, updated_by: str, headers: dict, totals: dict):
        update_data = {"batch_number": batch_number,
                       "drying_nw_wholes_in_quantity": totals.get('total_nw_wholes_in_quantity'),
                       "drying_nw_pieces_in_quantity": totals.get('total_nw_pieces_in_quantity'),
                       "drying_nw_rejection_in_quantity": totals.get('total_nw_rejection_in_quantity'),
                       "drying_nw_wholes_out_quantity": totals.get('total_nw_wholes_out_quantity'),
                       "drying_nw_pieces_out_quantity": totals.get('total_nw_pieces_out_quantity'),
                       "drying_nw_rejection_out_quantity": totals.get('total_nw_rejection_out_quantity'),
                       "updated_by": updated_by}
        await batch_summary_service.update_batch(update_data, headers)
