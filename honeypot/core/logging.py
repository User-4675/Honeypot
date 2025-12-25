"""
Configures and provides shared logger instances for the honeypot services.

This module sets up file-based, rotating logs to ensure that log files do not
grow indefinitely.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Final

# Define a consistent format for all log entries.
LOG_FORMAT: Final = logging.Formatter("%(asctime)s - %(message)s")
AUDIT_DIR: Final = "audits"


def setup_logger(name: str, log_file: str) -> logging.Logger:
    
    # Ensure the base audit directory exists.
    os.makedirs(AUDIT_DIR, exist_ok=True)
    
    # Construct the full, safe path for the log file.
    log_path = os.path.join(AUDIT_DIR, log_file)
    
    # Ensure the specific log directory exists.
    log_dir = os.path.dirname(log_path)
    os.makedirs(log_dir, exist_ok=True)

    # Get a logger instance.
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent logs from propagating to the root logger.
    logger.propagate = False

    # Add a rotating file handler if one is not already present.
    if not logger.handlers:
        # Rotates logs when they reach 2KB, keeping up to 5 old log files.
        handler = RotatingFileHandler(log_path, maxBytes=2000, backupCount=5)
        handler.setFormatter(LOG_FORMAT)
        logger.addHandler(handler)

    return logger