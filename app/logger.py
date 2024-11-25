import logging
from logging.handlers import RotatingFileHandler

# Create a logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)  # You can switch to DEBUG for more detailed logs

# Create a file handler for logging (rotates when the file reaches 1MB, keeps 5 backups)
file_handler = RotatingFileHandler("app_logs.log", maxBytes=1_000_000, backupCount=5)
file_handler.setLevel(logging.INFO)

# Create a console handler for debugging purposes
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define a logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
