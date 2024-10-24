import logging

def error_handler(func):
    """
    A wrapper function to handle errors for any given function.
    """
    def wrapper(*args, **kwargs):
        try:
            # Try executing the function with provided arguments
            return func(*args, **kwargs)
        except Exception as e:
            # Handle the exception and print an error message
            logging.error(e)
            return None  # Or some default value
    return wrapper