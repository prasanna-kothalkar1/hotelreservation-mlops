import logging
import os
from datetime import datetime

LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

@staticmethod
def get_logger(name):
    """
    Get a logger with the specified name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger