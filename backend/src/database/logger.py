import logging

# Create a logger instance with a unique name
logger = logging.getLogger("database")

# Set the logger's minimum logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)

# Create a console handler to log messages to the console (optional)
console_handler = logging.StreamHandler()

# Define the logging format
formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s: %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)  # Optional for logging to the console
