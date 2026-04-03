import logging
import os
import shutil

# Prefer ProgramData (shared logs), fall back to USERPROFILE if not available
LOG_DIR = os.path.join(
    os.environ.get("ProgramData", os.environ["USERPROFILE"]),
    "CashewInventory",
    "logs"
)

ACTIVE_LOG = os.path.join(LOG_DIR, "backend_0.log")
MAX_LOG_SIZE = 1 * 1024 * 1024  # 1 MB
MAX_ARCHIVES = 10

os.makedirs(LOG_DIR, exist_ok=True)

class MultiArchiveRotatingHandler(logging.FileHandler):
    def emit(self, record):
        if os.path.exists(ACTIVE_LOG) and os.path.getsize(ACTIVE_LOG) >= MAX_LOG_SIZE:
            self.rotate_logs()
        super().emit(record)

    def rotate_logs(self):
        # Close the current file stream
        self.close()

        # Delete the oldest archive if it exists
        oldest = os.path.join(LOG_DIR, f"backend_{MAX_ARCHIVES}.log")
        if os.path.exists(oldest):
            os.remove(oldest)

        # Shift archives: backend_9 → backend_10, ..., backend_1 → backend_2
        for i in reversed(range(1, MAX_ARCHIVES)):
            src = os.path.join(LOG_DIR, f"backend_{i}.log")
            dst = os.path.join(LOG_DIR, f"backend_{i+1}.log")
            if os.path.exists(src):
                shutil.move(src, dst)

        # Move backend_0 → backend_1
        shutil.move(ACTIVE_LOG, os.path.join(LOG_DIR, "backend_1.log"))

        # Reopen backend_0.log for fresh logging
        self.stream = self._open()

logger = logging.getLogger("cashew_erp_backend")
logger.setLevel(logging.DEBUG)

file_handler = MultiArchiveRotatingHandler(ACTIVE_LOG)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)