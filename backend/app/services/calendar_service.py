import asyncio
from app.services import boiling_service
from app.utils.logger import logger


async def get_dates_with_data(headers: dict = None):
    logger.info(f"Fetching all dates with any entry")
    results = await asyncio.gather(
        boiling_service.get_entry_dates(headers),
    )
    # Flatten and deduplicate
    all_dates = set(date for module_dates in results for date in module_dates)
    return sorted(all_dates)

async def get_entries_by_date(self, date: str):
    results = await asyncio.gather(
        self.production.get_entries_by_date(date),
        self.purchase.get_entries_by_date(date),
        self.boiling.get_entries_by_date(date),
        self.humidification.get_entries_by_date(date)
    )
    return {
        "date": date,
        "modules": {
            "production": results[0],
            "purchase": results[1],
            "boiling": results[2],
            "humidification": results[3],
        }
    }
