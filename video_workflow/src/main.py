#!/usr/bin/env python3
"""
Automated Video Workflow - Main Application

This script handles the main workflow for automated video processing.
It can run in either GUI mode or CLI mode.
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path

# Local imports
from config_manager import ConfigManager
from logger import setup_logger
from disk_monitor import DiskMonitor

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Automated Video Workflow")
    parser.add_argument("--gui", action="store_true", help="Run in GUI mode")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--structure-only", action="store_true", help="Only create folder structure")
    args = parser.parse_args()
    
    # Default to GUI mode if no mode is specified
    if not (args.gui or args.cli or args.structure_only):
        args.gui = True
    
    # Run in GUI mode
    if args.gui:
        run_gui_mode()
        return
    
    # Run in CLI mode
    # Initialize logger
    logger = setup_logger()
    logger.info("Starting Automated Video Workflow (CLI Mode)")
    
    # Load configuration
    try:
        config_manager = ConfigManager()
        config = config_manager.get_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    # If structure-only flag is set, just create the folder structure
    if args.structure_only:
        create_folder_structure(config, logger)
        return
    
    # Check if SSD is mounted
    disk_monitor = DiskMonitor(logger)
    if not disk_monitor.is_drive_mounted(config.get('ssd_name')):
        logger.warning(f"External SSD '{config.get('ssd_name')}' not mounted")
        
        # Wait for SSD to be mounted
        logger.info(f"Waiting for SSD '{config.get('ssd_name')}' to be mounted...")
        if disk_monitor.wait_for_drive(config.get('ssd_name'), timeout=60, check_interval=2):
            logger.info(f"SSD '{config.get('ssd_name')}' is now mounted")
        else:
            logger.error(f"Timeout waiting for SSD '{config.get('ssd_name')}'") 
            sys.exit(1)
    
    # TODO: Implement full CLI workflow
    
    logger.info("Workflow completed")

def run_gui_mode():
    """Run the application in GUI mode."""
    try:
        # First check if PyQt6 is properly installed
        try:
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtGui import QAction  # This was causing issues before
            from PyQt6.QtCore import Qt
        except ImportError as e:
            print(f"Error: PyQt6 is not properly installed or has missing components: {e}")
            print("Please reinstall PyQt6: pip install --upgrade --force-reinstall PyQt6")
            sys.exit(1)
            
        # Import GUI modules here to avoid dependencies if running in CLI mode
        try:
            from gui.main_window import run_gui
            run_gui()
        except ImportError as e:
            print(f"Error: Could not load GUI modules: {e}")
            print("There might be an issue with the GUI implementation.")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting GUI: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def create_folder_structure(config, logger):
    """Create the folder structure for a new project."""
    import datetime
    from pathlib import Path
    
    # Get paths from config
    raw_path = config.get('raw_path')
    if not raw_path:
        logger.error("RAW path not configured")
        return False
    
    # Create dated folder
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Prompt for project name
    project_name = input("Enter project name: ")
    if not project_name:
        logger.error("No project name provided")
        return False
    
    # Create project directory using Path for cross-platform compatibility
    project_dir = Path(raw_path) / date_str / project_name
    try:
        project_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created project directory: {project_dir}")
        
        # Create subfolders
        for folder in ['footage', 'proxies', 'exports', 'logs']:
            folder_path = project_dir / folder
            folder_path.mkdir(exist_ok=True)
            logger.info(f"Created folder: {folder_path}")
        
        # Copy DaVinci template if configured
        template_path = config.get('davinci_template_path')
        if template_path and Path(template_path).is_file():
            import shutil
            template_file = Path(template_path)
            dest_path = project_dir / template_file.name
            shutil.copy2(template_file, dest_path)
            logger.info(f"Copied DaVinci template to: {dest_path}")
        
        logger.info("Folder structure created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating folder structure: {e}")
        return False

if __name__ == "__main__":
    main()
