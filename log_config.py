import os
import logging
from datetime import datetime, timezone

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "trade_logs")
LOG_FILE = os.path.join(LOG_DIR, "trade_bot.log")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | run=%(run_id)s | "
    "%(name)s | %(message)s"
)

def setup_logging(level: int = logging.INFO):
    logging.basicConfig(
        filename=LOG_FILE,
        level=level,
        format=LOG_FORMAT,
    )

    class RunIdFilter(logging.Filter):
        def filter(self, record):
            record.run_id = RUN_ID
            return True

    logging.getLogger().addFilter(RunIdFilter())