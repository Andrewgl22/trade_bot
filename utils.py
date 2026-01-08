from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

def get_est_now():
    return datetime.now(timezone.utc).astimezone(ET)
