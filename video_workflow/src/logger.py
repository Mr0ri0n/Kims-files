#!/usr/bin/env python3
"""
Logger for Automated Video Workflow

Sets up logging for the application with configurable options.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(config=None):
    """
    Set up and configure the application logger.
    
    Args:
        config (dict, optional): Configuration dictionary with logging settings.
                                If None, default settings are used.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Default configuration
    default_config = {
        "level": "INFO",
        "file_path": "../logs/workflow.log",
        "max_size_mb": 10,
        "backup_count": 5
    }
    
    # Use provided config or default
    log_config = config.get("logging", default_config) if config else default_config
    
    # Create logger
    logger = logging.getLogger("video_workflow")
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Set log level
    log_level = getattr(logging, log_config.get("level", "INFO"))
    logger.setLevel(log_level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if file path is provided
    if log_config.get("file_path"):
        # Get absolute path for log file
        script_dir = Path(__file__).resolve().parent
        log_file_path = Path(log_config["file_path"])
        
        # Handle relative paths properly across platforms
        if log_file_path.is_absolute():
            log_path = log_file_path
        else:
            # Handle paths starting with '..' relative to script directory
            if str(log_file_path).startswith('..'):
                # Navigate from script directory to project root then to the logs folder
                parts = str(log_file_path).replace('\\', '/').split('/')
                current_dir = script_dir
                for part in parts:
                    if part == '..':
                        current_dir = current_dir.parent
                    elif part not in ('', '.'):
                        current_dir = current_dir / part
                log_path = current_dir
            else:
                # Treat as relative to project root
                log_path = script_dir.parent / log_file_path
        
        # Create directory if it doesn't exist
        os.makedirs(log_path.parent, exist_ok=True)
        
        # Set up rotating file handler
        max_bytes = log_config.get("max_size_mb", 10) * 1024 * 1024  # Convert MB to bytes
        backup_count = log_config.get("backup_count", 5)
        
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    logger.info("Logger initialized")
    return logger
