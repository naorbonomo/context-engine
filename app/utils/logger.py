import logging
from colorama import Fore, Style, init
import os
from dotenv import load_dotenv

load_dotenv()
init()  # Initialize colorama

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        # Add color to the message
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        record.msg = f"[{Fore.MAGENTA}{record.name}{Style.RESET_ALL}] {color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

def get_logger(name):
    """Get a logger instance with colored output"""
    logger = logging.getLogger(name)
    
    # Only add handler if logger doesn't have handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter('%(message)s'))
        logger.addHandler(handler)
        
        # Set level based on DEBUG_MODE in .env
        debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
        logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    return logger 