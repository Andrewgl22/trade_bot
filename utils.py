from datetime import datetime, time, timedelta
from pytz import timezone

def get_est_now():
    return datetime.now(timezone("US/Eastern"))
