import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from src.logger import get_logger

logger = get_logger(__name__)
logger.info("This is a test log message.")
