# src/utils/logger.py
import logging
import os
from datetime import datetime

def setup_logging():
    """
    Configures the logging settings for the project.
    Creates a log file in the logs directory with the current timestamp.
    
    Returns:
    --------
    logger : logging.Logger
        Configured logger instance.
    """
    # Create a logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a unique log file with the current timestamp
    log_filename = f'logs/project_log_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

    # Set up logging configuration with filename and line number
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,  # Adjust to DEBUG for more verbose logging
        format='%(asctime)s - %(levelname)s - %(message)s [in %(filename)s:%(lineno)d]',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Return the logger instance
    return logging.getLogger(__name__)
