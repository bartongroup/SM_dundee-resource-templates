import logging
from logging.handlers import RotatingFileHandler
import os

from config import LOG_PATH

def setup_logging(name='custom'):
    # Ensure the logs directory exists
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    
    log_file = os.path.join(LOG_PATH, 'app.log')
    
    # Set up log formatting
    formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(name)s - %(message)s')

    # Set up log rotation
    log_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    log_handler.setFormatter(formatter)

    # Your custom logger
    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(log_handler)
    
    return custom_logger
