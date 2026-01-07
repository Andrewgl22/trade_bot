import os
import logging
from datetime import datetime, timezone

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "trade_logs")
LOG_FILE = os.path.join(LOG_DIR, "trade_bot.log")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s | %(levelname)s | run=%(run_id)s | %(name)s | %(message)s"

def setup_logging(level: int = logging.INFO):
    # 1) Inject run_id into every LogRecord globally
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.run_id = RUN_ID
        return record

    logging.setLogRecordFactory(record_factory)

    # 2) Configure logging (force=True ensures it actually applies)
    logging.basicConfig(
        filename=LOG_FILE,
        level=level,
        format=LOG_FORMAT,
        force=True,
    )
