import sys
from Housing.src.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    exception_block_line_number = exc_tb.tb_frame.f_lineno
    try_block_line_number = exc_tb.tb_lineno

    error_message = "Error occured in python script name [{0}] line number [{1}] \
        at try block line number :[{3}] ,exception block line number [{4}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno , str(error),
        exception_block_line_number ,try_block_line_number
    )

    return error_message

class HousingException(Exception):
    def __init__(self, error_message:Exception, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        """
        This function will print class 
        If we use print(HousingException) ---> You will get return statement from __str__ method
        """
        return self.error_message    
    
    def __repr__(self) -> str:
        return 

