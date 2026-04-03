from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def current_timestamp() -> str:
    ist = ZoneInfo("Asia/Kolkata")
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")