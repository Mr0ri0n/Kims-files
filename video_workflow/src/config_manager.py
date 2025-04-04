#!/usr/bin/env python3
"""
Configuration Manager for Automated Video Workflow

Handles loading, validating, and providing access to configuration settings.
"""

import os
import json
from pathlib import Path

class ConfigManager:
    """Manages configuration for the video workflow application."""
    
    def __init__(self, config_path=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path (str, optional): Path to the config file. 
                                         Defaults to '../config/config.json'.
        """
        self.config = {}
        
        # Set default config path if not provided
        if config_path is None:
            # Get the directory where this script is located
            script_dir = Path(__file__).resolve().parent
            # Config is in the config directory at the project root
            self.config_path = script_dir.parent / 'config' / 'config.json'
        else:
            self.config_path = Path(config_path).resolve()
        
        # Load the configuration
        self._load_config()
    
    def _load_config(self):
        """Load configuration from the JSON file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                # Create default config if file doesn't exist
                self._create_default_config()
        except Exception as e:
            raise Exception(f"Failed to load configuration: {e}")
    
    def _create_default_config(self):
        """Create a default configuration file."""
        default_config = {
            "raw_path": "",
            "master_path": "",
            "ssd_name": "",
            "video_extensions": [".mp4", ".mov"],
            "create_proxies": False,
            "proxy_settings": {
                "resolution": "1280x720",
                "codec": "h264",
                "crf": 23
            },
            "davinci_template_path": "",
            "logging": {
                "level": "INFO",
                "file_path": "../logs/workflow.log",
                "max_size_mb": 10,
                "backup_count": 5
            }
        }
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_path.parent, exist_ok=True)
        
        # Write default config to file
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        self.config = default_config
    
    def get_config(self):
        """
        Get the current configuration.
        
        Returns:
            dict: The configuration dictionary
        """
        return self.config
    
    def update_config(self, new_config):
        """
        Update the configuration and save to file.
        
        Args:
            new_config (dict): New configuration values
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Update config dictionary
            self.config.update(new_config)
            
            # Save to file
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            return True
        except Exception:
            return False
