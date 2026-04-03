"""
Reports Service Layer

Handles business logic for reports:
- Fetching and aggregating data from multiple tables
- Calculating/transforming data
- Building complex queries
- Post-processing results

This layer sits between controllers and DAOs, providing clean separation
of concerns and enabling complex report logic without cluttering the controller.
"""

from typing import Optional, Any, Dict, List
from datetime import datetime
from asyncio import gather
from app.dao import reports_dao
from app.dao import purchase_dao, boiling_dao, rcn_sales_dao, batch_dao, drying_dao, cashew_kernel_sales_dao, humidifying_dao
from app.utils.logger import logger


class ReportsService:
    """Service layer for reports - handles aggregation and calculations."""

    @staticmethod
    async def get_rcn_closing_stock(
        page: int,
        page_size: int,
        headers: dict,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get RCN closing stock report.
        
        Calculation:
        RCN Closing Stock = Purchase Quantity - RCN Sales Quantity - Boiling Quantity
        
        Aggregates from purchases, boiling, and rcn_sales tables concurrently.
        Uses async.gather() to fetch data from multiple tables concurrently for better performance.
        """
        logger.info("Service: Fetching RCN closing stock data concurrently")
        
        try:
            # Fetch data from purchases, boiling, rcn_sales, and batch tables concurrently
            purchases, boiling, rcn_sales, batches = await gather(
                purchase_dao.fetch_all_purchases(headers),
                boiling_dao.fetch_all_boiling(headers),
                rcn_sales_dao.fetch_all_rcn_sales(headers),
                batch_dao.fetch_all_batches(headers),
                return_exceptions=True  # Don't fail if one table query fails
            )
            
            # Handle potential errors in concurrent calls
            if isinstance(purchases, Exception):
                logger.warning(f"Error fetching purchases: {purchases}")
                purchases = []
            if isinstance(boiling, Exception):
                logger.warning(f"Error fetching boiling: {boiling}")
                boiling = []
            if isinstance(rcn_sales, Exception):
                logger.warning(f"Error fetching rcn_sales: {rcn_sales}")
                rcn_sales = []
            if isinstance(batches, Exception):
                logger.warning(f"Error fetching batches: {batches}")
                batches = []
            
            # Create batch lookup dictionary for quick origin lookup
            batch_lookup = {}
            for batch in batches:
                # Handle both raw batch data and mapped batch data
                batch_num = batch.get("batch_number") or batch.get("batchNumber") or batch.get("id")
                origin = batch.get("origin", "")
                
                if batch_num:
                    batch_lookup[batch_num] = {
                        "origin": origin,
                        "batch_entry_date": batch.get("batch_entry_date", ""),
                    }
            
            logger.info(f"Batch lookup created with {len(batch_lookup)} entries")
            
            # Aggregate data by batch_number
            batch_data = {}
            
            # Helper function to check if date is within filter range
            def is_date_in_range(date_str):
                if not date_str:
                    return True  # Include if no date
                try:
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
                except Exception:
                    return True  # Include if date parsing fails
            
            # Group purchases by batch_number
            for purchase in purchases:
                batch = purchase.get("batch_number")
                purchase_date = purchase.get("purchase_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(purchase_date):
                    if batch not in batch_data:
                        # Get origin from batch_lookup instead of purchase
                        origin = batch_lookup.get(batch, {}).get("origin", "")
                        if batch in batch_lookup:
                            logger.debug(f"Found batch {batch} in lookup with origin: {origin}")
                        else:
                            logger.debug(f"Batch {batch} NOT found in lookup. Available keys: {list(batch_lookup.keys())[:5]}")
                        batch_data[batch] = {
                            "batch_number": batch,
                            "origin": origin,
                            "rcn_in_kg": 0,
                            "rcn_to_boiling_kg": 0,
                            "rcn_sold_kg": 0,
                            "purchase_date": purchase_date,
                            "boiling_date": None,
                            "sale_date": None,
                        }
                    batch_data[batch]["rcn_in_kg"] += float(purchase.get("quantity_kg", 0))
                    # Update purchase_date (keep first/earliest)
                    if purchase_date and (not batch_data[batch]["purchase_date"] or purchase_date < batch_data[batch]["purchase_date"]):
                        batch_data[batch]["purchase_date"] = purchase_date
            
            # Aggregate boiling quantities
            for boil_record in boiling:
                batch = boil_record.get("batch_number")
                boiling_date = boil_record.get("boiling_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(boiling_date):
                    if batch not in batch_data:
                        origin = batch_lookup.get(batch, {}).get("origin", "")
                        batch_data[batch] = {
                            "batch_number": batch,
                            "origin": origin,
                            "rcn_in_kg": 0,
                            "rcn_to_boiling_kg": 0,
                            "rcn_sold_kg": 0,
                            "purchase_date": None,
                            "boiling_date": boiling_date,
                            "sale_date": None,
                        }
                    batch_data[batch]["rcn_to_boiling_kg"] += float(boil_record.get("quantity_kg", 0))
                    # Update boiling_date (keep latest)
                    if boiling_date and (not batch_data[batch]["boiling_date"] or boiling_date > batch_data[batch]["boiling_date"]):
                        batch_data[batch]["boiling_date"] = boiling_date
            
            # Aggregate RCN sales
            for sale_record in rcn_sales:
                batch = sale_record.get("batch_number")
                sale_date = sale_record.get("sale_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(sale_date):
                    if batch not in batch_data:
                        origin = batch_lookup.get(batch, {}).get("origin", "")
                        batch_data[batch] = {
                            "batch_number": batch,
                            "origin": origin,
                            "rcn_in_kg": 0,
                            "rcn_to_boiling_kg": 0,
                            "rcn_sold_kg": 0,
                            "purchase_date": None,
                            "boiling_date": None,
                            "sale_date": sale_date,
                        }
                    batch_data[batch]["rcn_sold_kg"] += float(sale_record.get("quantity_kg", 0))
                    # Update sale_date (keep latest)
                    if sale_date and (not batch_data[batch]["sale_date"] or sale_date > batch_data[batch]["sale_date"]):
                        batch_data[batch]["sale_date"] = sale_date
            
            # Convert to list and calculate closing stock for each batch
            batch_list = []
            for batch_info in batch_data.values():
                rcn_in = batch_info["rcn_in_kg"]
                rcn_boiling = batch_info["rcn_to_boiling_kg"]
                rcn_sold = batch_info["rcn_sold_kg"]
                
                # Closing Stock = Purchase - Sales - Boiling
                closing_stock = rcn_in - rcn_sold - rcn_boiling
                
                # Calculate last_activity_date as the latest among all dates
                dates = [
                    batch_info.get("purchase_date"),
                    batch_info.get("boiling_date"),
                    batch_info.get("sale_date"),
                ]
                last_activity_date = max([d for d in dates if d], default="")
                
                batch_info["closing_stock_kg"] = max(closing_stock, 0)
                batch_info["last_activity_date"] = last_activity_date
                
                batch_list.append(batch_info)
            
            # Apply sorting if needed
            if sort:
                try:
                    col, direction = sort.rsplit(":", 1)
                    reverse = direction.lower() == "desc"
                    batch_list.sort(key=lambda x: float(x.get(col, 0)), reverse=reverse)
                except Exception as e:
                    logger.warning(f"Error applying sort: {e}")
            
            # Apply pagination
            offset = (page - 1) * page_size
            paginated_list = batch_list[offset:offset + page_size]
            total = len(batch_list)
            
            return {
                "rows": paginated_list,
                "total": total
            }
        
        except Exception as e:
            logger.error(f"Error in get_rcn_closing_stock: {e}")
            raise

    @staticmethod
    async def get_outturn(
        page: int,
        page_size: int,
        headers: dict,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get outturn report with calculations.
        
        Outturn = Total NW / (Purchase - NW Sales)
        Outturn (in LBS) = Outturn * 176.409623144943
        
        Aggregates from drying, purchases, and cashew_kernel_sales tables concurrently.
        """
        logger.info("Service: Fetching outturn report data concurrently")
        
        try:
            # Fetch data from drying, purchases, and cashew_kernel_sales tables concurrently
            drying, purchases, kernel_sales = await gather(
                drying_dao.fetch_all_drying(headers),
                purchase_dao.fetch_all_purchases(headers),
                cashew_kernel_sales_dao.fetch_all_cashew_kernel_sales(headers),
                return_exceptions=True  # Don't fail if one table query fails
            )
            
            # Handle potential errors in concurrent calls
            if isinstance(drying, Exception):
                logger.warning(f"Error fetching drying: {drying}")
                drying = []
            if isinstance(purchases, Exception):
                logger.warning(f"Error fetching purchases: {purchases}")
                purchases = []
            if isinstance(kernel_sales, Exception):
                logger.warning(f"Error fetching kernel_sales: {kernel_sales}")
                kernel_sales = []
            
            # Aggregate data by batch_number
            batch_data = {}
            
            # Helper function to check if date is within filter range
            def is_date_in_range(date_str):
                if not date_str:
                    return True  # Include if no date
                try:
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
                except Exception:
                    return True  # Include if date parsing fails
            
            # Group drying data by batch_number (NW wholes and pieces)
            for dry_record in drying:
                batch = dry_record.get("batch_number")
                drying_date = dry_record.get("drying_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(drying_date):
                    if batch not in batch_data:
                        batch_data[batch] = {
                            "batch_number": batch,
                            "nw_wholes_qty_in_kg": 0,
                            "nw_pieces_qty_in_kg": 0,
                            "total_nw_kg": 0,
                            "purchase_qty_kg": 0,
                            "nw_sales_qty_kg": 0,
                            "outturn_percent": 0,
                            "outturn_lbs": 0,
                        }
                    
                    # Aggregate NW quantities from drying
                    batch_data[batch]["nw_wholes_qty_in_kg"] += float(dry_record.get("nw_wholes_in_kg", 0))
                    batch_data[batch]["nw_pieces_qty_in_kg"] += float(dry_record.get("nw_pieces_in_kg", 0))
            
            # Aggregate purchase quantities
            for purchase in purchases:
                batch = purchase.get("batch_number")
                purchase_date = purchase.get("purchase_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(purchase_date):
                    if batch not in batch_data:
                        batch_data[batch] = {
                            "batch_number": batch,
                            "nw_wholes_qty_in_kg": 0,
                            "nw_pieces_qty_in_kg": 0,
                            "total_nw_kg": 0,
                            "purchase_qty_kg": 0,
                            "nw_sales_qty_kg": 0,
                            "outturn_percent": 0,
                            "outturn_lbs": 0,
                        }
                    batch_data[batch]["purchase_qty_kg"] += float(purchase.get("quantity_kg", 0))
            
            # Aggregate NW sales quantities
            for sale_record in kernel_sales:
                batch = sale_record.get("batch_number")
                sale_date = sale_record.get("sale_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(sale_date):
                    if batch not in batch_data:
                        batch_data[batch] = {
                            "batch_number": batch,
                            "nw_wholes_qty_in_kg": 0,
                            "nw_pieces_qty_in_kg": 0,
                            "total_nw_kg": 0,
                            "purchase_qty_kg": 0,
                            "nw_sales_qty_kg": 0,
                            "outturn_percent": 0,
                            "outturn_lbs": 0,
                        }
                    batch_data[batch]["nw_sales_qty_kg"] += float(sale_record.get("quantity_kg", 0))
            
            # Convert to list and calculate outturn for each batch
            batch_list = []
            for batch_info in batch_data.values():
                nw_wholes = batch_info["nw_wholes_qty_in_kg"]
                nw_pieces = batch_info["nw_pieces_qty_in_kg"]
                total_nw = nw_wholes + nw_pieces
                purchase_qty = batch_info["purchase_qty_kg"]
                nw_sales = batch_info["nw_sales_qty_kg"]
                
                # Calculate outturn: Total NW / (Purchase - NW Sales)
                denominator = purchase_qty - nw_sales
                outturn_percent = 0
                if denominator > 0:
                    outturn_percent = (total_nw / denominator) * 100
                
                # Calculate outturn in LBS
                outturn_lbs = outturn_percent * 176.409623144943
                
                batch_info["total_nw_kg"] = total_nw
                batch_info["outturn_percent"] = round(outturn_percent, 2)
                batch_info["outturn_lbs"] = round(outturn_lbs, 2)
                
                batch_list.append(batch_info)
            
            # Apply sorting if needed
            if sort:
                try:
                    col, direction = sort.rsplit(":", 1)
                    reverse = direction.lower() == "desc"
                    batch_list.sort(key=lambda x: float(x.get(col, 0)), reverse=reverse)
                except Exception as e:
                    logger.warning(f"Error applying sort: {e}")
            
            # Apply pagination
            offset = (page - 1) * page_size
            paginated_list = batch_list[offset:offset + page_size]
            total = len(batch_list)
            
            return {
                "rows": paginated_list,
                "total": total
            }
        
        except Exception as e:
            logger.error(f"Error in get_outturn: {e}")
            raise

    @staticmethod
    async def get_nw_percent(
        page: int,
        page_size: int,
        headers: dict,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get NW percent report showing breakdown of wholes vs pieces.
        
        NW Wholes % = NW Wholes Qty IN / Total NW Qty
        NW Pieces % = NW Pieces Qty IN / Total NW Qty
        Total % = NW Wholes % + NW Pieces %
        
        Aggregates from drying table.
        """
        logger.info("Service: Fetching NW percent report")
        
        try:
            # Fetch drying data
            drying = await drying_dao.fetch_all_drying(headers)
            
            # Handle potential errors
            if isinstance(drying, Exception):
                logger.warning(f"Error fetching drying: {drying}")
                drying = []
            
            # Aggregate data by batch_number
            batch_data = {}
            
            # Helper function to check if date is within filter range
            def is_date_in_range(date_str):
                if not date_str:
                    return True  # Include if no date
                try:
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
                except Exception:
                    return True  # Include if date parsing fails
            
            # Group drying data by batch_number
            for dry_record in drying:
                batch = dry_record.get("batch_number")
                drying_date = dry_record.get("drying_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(drying_date):
                    if batch not in batch_data:
                        batch_data[batch] = {
                            "batch_number": batch,
                            "nw_wholes_qty_in_kg": 0,
                            "nw_pieces_qty_in_kg": 0,
                            "drying_date": drying_date,
                        }
                    
                    batch_data[batch]["nw_wholes_qty_in_kg"] += float(dry_record.get("nw_wholes_in_kg", 0))
                    batch_data[batch]["nw_pieces_qty_in_kg"] += float(dry_record.get("nw_pieces_in_kg", 0))
            
            # Convert to list and calculate percentages
            batch_list = []
            for batch_info in batch_data.values():
                nw_wholes = batch_info["nw_wholes_qty_in_kg"]
                nw_pieces = batch_info["nw_pieces_qty_in_kg"]
                total_nw = nw_wholes + nw_pieces
                
                # Calculate percentages
                nw_wholes_percent = 0
                nw_pieces_percent = 0
                total_percent = 0
                
                if total_nw > 0:
                    nw_wholes_percent = round((nw_wholes / total_nw) * 100, 2)
                    nw_pieces_percent = round((nw_pieces / total_nw) * 100, 2)
                    total_percent = round(nw_wholes_percent + nw_pieces_percent, 2)
                
                batch_info["nw_wholes_percent"] = nw_wholes_percent
                batch_info["nw_pieces_percent"] = nw_pieces_percent
                batch_info["total_percent"] = total_percent
                
                batch_list.append(batch_info)
            
            # Apply sorting if needed
            if sort:
                try:
                    sort_field, sort_order = sort.split(':')
                    reverse = sort_order.lower() == 'desc'
                    batch_list.sort(key=lambda x: x.get(sort_field, ''), reverse=reverse)
                except Exception as e:
                    logger.warning(f"Error applying sort {sort}: {e}")
            
            # Apply search if needed
            if search:
                search_term = search.lower()
                batch_list = [
                    batch for batch in batch_list
                    if search_term in str(batch.get("batch_number", "")).lower()
                ]
            
            # Apply pagination
            offset = (page - 1) * page_size
            paginated_list = batch_list[offset:offset + page_size]
            total = len(batch_list)
            
            return {
                "rows": paginated_list,
                "total": total
            }
        
        except Exception as e:
            logger.error(f"Error in get_nw_percent: {e}")
            raise

    @staticmethod
    async def get_drying_moisture_loss(
        page: int,
        page_size: int,
        headers: dict,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get drying moisture loss report based on weight differences.
        
        NW Qty IN = NW Wholes In Qty + NW Pieces Qty IN
        NW Qty OUT = NW Wholes Qty OUT + NW Pieces Qty OUT
        Moisture Loss = NW Qty IN - NW Qty OUT
        Moisture Loss % = (Moisture Loss / NW Qty IN) * 100
        
        Aggregates from drying table.
        """
        logger.info("Service: Fetching drying moisture loss report")
        
        try:
            # Fetch drying data
            drying = await drying_dao.fetch_all_drying(headers)
            
            # Handle potential errors
            if isinstance(drying, Exception):
                logger.warning(f"Error fetching drying: {drying}")
                drying = []
            
            # Aggregate data by batch_number
            batch_data = {}
            
            # Helper function to check if date is within filter range
            def is_date_in_range(date_str):
                if not date_str:
                    return True  # Include if no date
                try:
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
                except Exception:
                    return True  # Include if date parsing fails
            
            # Group drying data by batch_number
            for dry_record in drying:
                batch = dry_record.get("batch_number")
                drying_date = dry_record.get("drying_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(drying_date):
                    if batch not in batch_data:
                        batch_data[batch] = {
                            "batch_number": batch,
                            "nw_qty_in_kg": 0,
                            "nw_qty_out_kg": 0,
                            "drying_date": drying_date,
                        }
                    
                    # Sum NW quantities IN (wholes + pieces)
                    batch_data[batch]["nw_qty_in_kg"] += float(dry_record.get("nw_wholes_in_kg", 0))
                    batch_data[batch]["nw_qty_in_kg"] += float(dry_record.get("nw_pieces_in_kg", 0))
                    
                    # Sum NW quantities OUT (wholes + pieces)
                    batch_data[batch]["nw_qty_out_kg"] += float(dry_record.get("nw_wholes_out_kg", 0))
                    batch_data[batch]["nw_qty_out_kg"] += float(dry_record.get("nw_pieces_out_kg", 0))
            
            # Convert to list and calculate moisture loss
            batch_list = []
            for batch_info in batch_data.values():
                nw_qty_in = batch_info["nw_qty_in_kg"]
                nw_qty_out = batch_info["nw_qty_out_kg"]
                
                # Calculate moisture loss
                moisture_loss_kg = nw_qty_in - nw_qty_out
                moisture_loss_percent = 0
                
                if nw_qty_in > 0:
                    moisture_loss_percent = round((moisture_loss_kg / nw_qty_in) * 100, 2)
                
                batch_info["moisture_loss_kg"] = round(moisture_loss_kg, 2)
                batch_info["moisture_loss_percent"] = moisture_loss_percent
                
                batch_list.append(batch_info)
            
            # Apply sorting if needed
            if sort:
                try:
                    sort_field, sort_order = sort.split(':')
                    reverse = sort_order.lower() == 'desc'
                    batch_list.sort(key=lambda x: x.get(sort_field, ''), reverse=reverse)
                except Exception as e:
                    logger.warning(f"Error applying sort {sort}: {e}")
            
            # Apply search if needed
            if search:
                search_term = search.lower()
                batch_list = [
                    batch for batch in batch_list
                    if search_term in str(batch.get("batch_number", "")).lower()
                ]
            
            # Apply pagination
            offset = (page - 1) * page_size
            paginated_list = batch_list[offset:offset + page_size]
            total = len(batch_list)
            
            return {
                "rows": paginated_list,
                "total": total
            }
        
        except Exception as e:
            logger.error(f"Error in get_drying_moisture_loss: {e}")
            raise

    @staticmethod
    async def get_humidification(
        page: int,
        page_size: int,
        headers: dict,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get humidification moisture increase report based on weight differences.
        
        NW Qty IN = NW Wholes In Qty + NW Pieces Qty IN
        NW Qty OUT = NW Wholes Qty OUT + NW Pieces Qty OUT
        Moisture Increase = NW Qty OUT - NW Qty IN
        Moisture % = (Moisture Increase / NW Qty IN) * 100
        
        Aggregates from humidifying table.
        """
        logger.info("Service: Fetching humidification report")
        
        try:
            # Fetch humidifying data
            humidifying = await humidifying_dao.fetch_all_humidifying(headers)
            
            # Handle potential errors
            if isinstance(humidifying, Exception):
                logger.warning(f"Error fetching humidifying: {humidifying}")
                humidifying = []
            
            # Aggregate data by batch_number
            batch_data = {}
            
            # Helper function to check if date is within filter range
            def is_date_in_range(date_str):
                if not date_str:
                    return True  # Include if no date
                try:
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
                except Exception:
                    return True  # Include if date parsing fails
            
            # Group humidifying data by batch_number
            for humid_record in humidifying:
                batch = humid_record.get("batch_number")
                humid_date = humid_record.get("humidifying_date", "")
                
                # Only include if date is in range
                if batch and is_date_in_range(humid_date):
                    if batch not in batch_data:
                        batch_data[batch] = {
                            "batch_number": batch,
                            "nw_qty_in_kg": 0,
                            "nw_qty_out_kg": 0,
                            "humidifying_date": humid_date,
                        }
                    
                    # Sum NW quantities IN (wholes + pieces, excluding rejections)
                    batch_data[batch]["nw_qty_in_kg"] += float(humid_record.get("nw_wholes_in_kg", 0))
                    batch_data[batch]["nw_qty_in_kg"] += float(humid_record.get("nw_pieces_in_kg", 0))
                    
                    # Sum NW quantities OUT (wholes + pieces, excluding rejections)
                    batch_data[batch]["nw_qty_out_kg"] += float(humid_record.get("nw_wholes_out_kg", 0))
                    batch_data[batch]["nw_qty_out_kg"] += float(humid_record.get("nw_pieces_out_kg", 0))
            
            # Convert to list and calculate moisture increase
            batch_list = []
            for batch_info in batch_data.values():
                nw_qty_in = batch_info["nw_qty_in_kg"]
                nw_qty_out = batch_info["nw_qty_out_kg"]
                
                # Calculate moisture increase
                moisture_increase_kg = nw_qty_out - nw_qty_in
                moisture_increase_percent = 0
                
                if nw_qty_in > 0:
                    moisture_increase_percent = round((moisture_increase_kg / nw_qty_in) * 100, 2)
                
                batch_info["moisture_increase_kg"] = round(moisture_increase_kg, 2)
                batch_info["moisture_increase_percent"] = moisture_increase_percent
                
                batch_list.append(batch_info)
            
            # Apply sorting if needed
            if sort:
                try:
                    sort_field, sort_order = sort.split(':')
                    reverse = sort_order.lower() == 'desc'
                    batch_list.sort(key=lambda x: x.get(sort_field, ''), reverse=reverse)
                except Exception as e:
                    logger.warning(f"Error applying sort {sort}: {e}")
            
            # Apply search if needed
            if search:
                search_term = search.lower()
                batch_list = [
                    batch for batch in batch_list
                    if search_term in str(batch.get("batch_number", "")).lower()
                ]
            
            # Apply pagination
            offset = (page - 1) * page_size
            paginated_list = batch_list[offset:offset + page_size]
            total = len(batch_list)
            
            return {
                "rows": paginated_list,
                "total": total
            }
        
        except Exception as e:
            logger.error(f"Error in get_humidification: {e}")
            raise


# ============================================================================
# Advanced Service Methods for Complex Reports
# ============================================================================

class AdvancedReportsService:
    """
    Advanced service methods for complex multi-table aggregations.
    These methods demonstrate fetching from multiple tables and combining results.
    """

    @staticmethod
    async def get_batch_processing_summary(
        page: int,
        page_size: int,
        headers: dict,
        batch_id: Optional[str] = None,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get comprehensive batch processing summary.
        
        Aggregates data from:
        - batch_summary (main batch info)
        - boiling (boiling data)
        - drying (drying data)
        - humidifying (humidification data)
        - peeling_* (peeling data)
        - grades (quality grades)
        
        Returns: Combined view with all processing steps and calculated metrics.
        """
        logger.info(f"Service: Fetching batch processing summary for batch: {batch_id}")
        
        try:
            # Fetch main batch data
            batches = await reports_dao.fetch_rcn_closing_stock(
                page=page,
                page_size=page_size,
                headers=headers,
                sort=sort,
                search=search,
                date_from=date_from,
                date_to=date_to,
            )
            
            # For each batch, fetch related processing data
            # Note: This is a simplified example - in production, you'd:
            # 1. Create a database VIEW that joins all these tables
            # 2. Query the VIEW instead of making multiple API calls
            
            enriched_rows = []
            for batch in batches.get("rows", []):
                batch_number = batch.get("batch_number")
                
                # In a real scenario, fetch from other tables:
                # boiling_data = await reports_dao.fetch_boiling_by_batch(batch_number, headers)
                # drying_data = await reports_dao.fetch_drying_by_batch(batch_number, headers)
                # grades_data = await reports_dao.fetch_grades_by_batch(batch_number, headers)
                
                # Combine and calculate
                enriched_batch = {
                    **batch,
                    # "boiling_date": boiling_data[0].get("created_at") if boiling_data else None,
                    # "drying_duration_hours": drying_data[0].get("duration_hours") if drying_data else None,
                    # "final_grade": grades_data[0].get("grade") if grades_data else None,
                    # "total_processing_days": calculate_days(...),
                    "processing_status": "Completed",  # Would calculate based on data
                }
                enriched_rows.append(enriched_batch)
            
            return {
                "rows": enriched_rows,
                "total": batches.get("total", 0),
            }
        
        except Exception as e:
            logger.error(f"Error fetching batch processing summary: {e}")
            raise

    @staticmethod
    async def get_production_metrics(
        page: int,
        page_size: int,
        headers: dict,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get aggregated production metrics across multiple batches.
        
        Calculates:
        - Total RCN processed
        - Total kernel output
        - Average outturn %
        - Total processing time
        - Quality distribution
        
        Aggregates from:
        - batch_summary
        - grades
        - drying
        - boiling
        """
        logger.info("Service: Fetching production metrics")
        
        try:
            # Fetch outturn data (which has all batches)
            outturn_data = await reports_dao.fetch_outturn(
                page=1,
                page_size=10000,  # Get all data for aggregation
                headers=headers,
                sort=None,
                search=search,
                date_from=date_from,
                date_to=date_to,
            )
            
            rows = outturn_data.get("rows", [])
            
            if not rows:
                return {"rows": [], "total": 0, "metrics": {}}
            
            # Calculate aggregate metrics
            total_rcn_input = sum(r.get("rcn_input_kg", 0) for r in rows)
            total_kernel_output = sum(r.get("kernel_output_kg", 0) for r in rows)
            avg_outturn = sum(r.get("outturn_percent", 0) for r in rows) / len(rows) if rows else 0
            
            metrics = {
                "total_rcn_input_kg": round(total_rcn_input, 2),
                "total_kernel_output_kg": round(total_kernel_output, 2),
                "average_outturn_percent": round(avg_outturn, 2),
                "total_batches": len(rows),
                "reporting_period": f"{date_from} to {date_to}" if date_from and date_to else "All time",
            }
            
            # Return paginated results
            start = (page - 1) * page_size
            end = start + page_size
            paginated_rows = rows[start:end]
            
            return {
                "rows": paginated_rows,
                "total": len(rows),
                "metrics": metrics,
            }
        
        except Exception as e:
            logger.error(f"Error fetching production metrics: {e}")
            raise

    @staticmethod
    async def get_quality_report(
        page: int,
        page_size: int,
        headers: dict,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get quality report with grade distribution.
        
        Aggregates from:
        - grades (quality grades)
        - batch_summary (batch info)
        - drying (moisture content)
        - peeling_after_drying (peeling quality)
        """
        logger.info("Service: Fetching quality report")
        
        # In a real implementation, you would:
        # 1. Fetch all grades for the date range
        # 2. Group by grade type
        # 3. Calculate percentages
        # 4. Combine with batch and process data
        
        # For now, return example structure
        return {
            "rows": [],
            "total": 0,
            "quality_metrics": {
                "grade_a_percent": 0,
                "grade_b_percent": 0,
                "grade_c_percent": 0,
                "rejections_percent": 0,
            },
        }


# ============================================================================
# Utility Service Methods
# ============================================================================

class ReportUtilsService:
    """
    Utility methods for common report operations.
    """

    @staticmethod
    def calculate_percentage(value: float, total: float) -> float:
        """Calculate percentage safely."""
        if total <= 0:
            return 0.0
        return round((value / total) * 100, 2)

    @staticmethod
    def calculate_percentage_change(start: float, end: float) -> float:
        """Calculate percentage change between two values."""
        if start <= 0:
            return 0.0
        return round(((end - start) / start) * 100, 2)

    @staticmethod
    def format_currency(amount: float, currency: str = "₹") -> str:
        """Format amount as currency."""
        return f"{currency}{amount:,.2f}"

    @staticmethod
    def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
        """Safely divide two numbers."""
        if denominator == 0:
            return default
        return numerator / denominator

    @staticmethod
    def group_by_field(rows: List[Dict], field: str) -> Dict[str, List[Dict]]:
        """Group rows by a specific field."""
        grouped = {}
        for row in rows:
            key = row.get(field)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(row)
        return grouped

    @staticmethod
    def sum_field(rows: List[Dict], field: str) -> float:
        """Sum a numeric field across all rows."""
        return sum(float(r.get(field, 0)) for r in rows)

    @staticmethod
    def average_field(rows: List[Dict], field: str) -> float:
        """Calculate average of a numeric field."""
        if not rows:
            return 0.0
        total = sum(float(r.get(field, 0)) for r in rows)
        return round(total / len(rows), 2)

    @staticmethod
    def enrich_row_with_calculations(
        row: Dict,
        calculations: Dict[str, callable],
    ) -> Dict:
        """
        Enrich a row with calculated fields.
        
        Example:
        ```python
        calculations = {
            "profit_margin": lambda r: (r["revenue"] - r["cost"]) / r["revenue"] * 100,
            "status": lambda r: "Active" if r["amount"] > 0 else "Inactive",
        }
        enriched = enrich_row_with_calculations(row, calculations)
        ```
        """
        enriched = row.copy()
        for field_name, calc_func in calculations.items():
            try:
                enriched[field_name] = calc_func(row)
            except Exception as e:
                logger.warning(f"Error calculating {field_name}: {e}")
                enriched[field_name] = None
        return enriched

    @staticmethod
    def enrich_rows_with_calculations(
        rows: List[Dict],
        calculations: Dict[str, callable],
    ) -> List[Dict]:
        """Enrich multiple rows with calculated fields."""
        return [
            ReportUtilsService.enrich_row_with_calculations(row, calculations)
            for row in rows
        ]
