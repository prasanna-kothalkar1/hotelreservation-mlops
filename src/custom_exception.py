import traceback
import sys

class CustomException(Exception):
    """Base class for custom exceptions."""
    def __init__(self, error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)
        self.error_detail = error_detail
        
    @staticmethod
    def get_detailed_error_message(error_message, error_detail:sys):
        """
        Extracts detailed error message including file name and line number.
        """
        error_message = str(error_message)
        if error_detail is not None:
            _, _, exc_tb = traceback.sys.exc_info()
            error_message = f"Error occurred in script: {exc_tb.tb_frame.f_code.co_filename} at line: {exc_tb.tb_lineno} with error message: {error_message}"
        else:
            error_message = f"Error occurred: {error_message}"
        return error_message

    def __str__(self):
        return self.error_message