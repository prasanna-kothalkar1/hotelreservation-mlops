from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)
def test_logger():
    try:
        logger.info("This is a test log message.")
        raise ValueError("This is a test exception")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise CustomException("Custom test logger error", sys) 
    finally:
        logger.info("Test completed.")

def divide_number(a,b):
    try:
        result = a / b
        logger.info(f"Division result: {result}")
    except ZeroDivisionError as e:
        logger.error(f"Division by zero error: {e}")
        raise CustomException("Custom zero division error", sys) 
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise CustomException("Custom unexpected error", sys) 
    
if __name__ == "__main__":
    try:
        logger.info("Starting main program.")
        #test_logger()
        #divide_number(10, 0)
        divide_number(10, 2)
        divide_number(10, "a")
        divide_number(10, None)
    except CustomException as e:
        logger.error(f"Custom exception caught: {e}")
        logger.info("Test completed.")