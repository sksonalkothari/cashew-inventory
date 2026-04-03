from typing import List, Dict
from app.services import batch_summary_service
from app.dao import cashew_shell_sales_dao
from app.utils.logger import logger
from app.exceptions.exceptions import CashewShellSalesError


class CashewShellSalesHelper:

    @staticmethod
    def consolidate_batches(records: List[dict]) -> Dict[str, dict]:
        batch_map = {}
        for rec in records:
            batch_number = rec.get('batch_number')
            qty = rec.get('quantity_kg', 0) or 0
            if not batch_number:
                continue
            if batch_number not in batch_map:
                batch_map[batch_number] = {"cashew_shell_sales_qty": 0, "created_by": rec.get('created_by')}
            batch_map[batch_number]["cashew_shell_sales_qty"] += qty
        return batch_map

    @staticmethod
    async def ensure_batches_exist(batch_map: Dict[str, dict], headers: dict):
        try:
            for batch_number, data in batch_map.items():
                existing = await batch_summary_service.fetch_batch_summary_by_batch_number(batch_number, headers)
                if not existing:
                    await batch_summary_service.insert_batch_summary({"batch_number": batch_number, "created_by": data.get('created_by')}, headers)
        except Exception as e:
            logger.exception("Failed to ensure batch_summary rows exist for cashew shell sales")
            raise CashewShellSalesError(str(e))

    @staticmethod
    async def update_batch_quantities(batch_map: Dict[str, dict], headers: dict):
        try:
            for batch_number in batch_map.keys():
                totals = await cashew_shell_sales_dao.fetch_all_cashew_shell_sales_by_batch_number(batch_number, headers)
                total_qty = sum([item.get('quantity_kg') or 0 for item in totals])
                await batch_summary_service.update_batch(batch_number, {"cashew_shell_sales_qty": total_qty}, headers)
        except Exception as e:
            logger.exception("Failed to update batch_summary cashew_shell_sales_qty")
            raise CashewShellSalesError(str(e))
