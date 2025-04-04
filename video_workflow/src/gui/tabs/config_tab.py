"""
Configuration Tab for the Video Workflow Application
"""

import os
import json
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QSizePolicy,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

# Import UI template components
from ..ui_template import (
    create_group_box, create_directory_selector, create_input_field,
    create_checkbox, create_button, show_info, show_error, create_horizontal_separator
)

class ConfigTab(QWidget):
    """Configuration tab for setting up paths and preferences."""
    
    # Signals
    config_saved = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        
        # Initialize UI
        self.init_ui()
        
        # Load existing configuration if available
        self.load_config()
    
    def init_ui(self):
        """Initialize the UI components."""
        # Set size policy to expand in both directions
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # Create a scrollable area for the entire content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create a widget to hold all content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(15)
        
        # Paths group
        self.paths_group, self.paths_layout = create_group_box("Storage Paths")
        
        # Raw path selector
        self.raw_path_container, self.raw_path_label, self.raw_path_button = create_directory_selector("RAW Path:")
        self.paths_layout.addWidget(self.raw_path_container)
        
        # Master path selector
        self.master_path_container, self.master_path_label, self.master_path_button = create_directory_selector("MASTER Path:")
        self.paths_layout.addWidget(self.master_path_container)
        
        # SSD name input
        self.ssd_name_container, self.ssd_name_input = create_input_field("SSD Name:")
        self.paths_layout.addWidget(self.ssd_name_container)
        
        # Add paths group to content layout
        content_layout.addWidget(self.paths_group)
        
        # Video settings group
        self.video_group, self.video_layout = create_group_box("Video Settings")
        
        # Video extensions input
        self.extensions_container, self.extensions_input = create_input_field("Video Extensions:")
        self.extensions_input.setPlaceholderText(".mp4, .mov (comma separated)")
        self.video_layout.addWidget(self.extensions_container)
        
        # Create proxies checkbox
        self.create_proxies_checkbox = create_checkbox("Create Proxy Files")
        self.video_layout.addWidget(self.create_proxies_checkbox)
        
        # Proxy settings (initially hidden)
        self.proxy_container = QWidget()
        self.proxy_layout = QVBoxLayout(self.proxy_container)
        self.proxy_layout.setContentsMargins(20, 0, 0, 0)
        
        # Proxy resolution
        self.proxy_resolution_container, self.proxy_resolution_input = create_input_field("Resolution:")
        self.proxy_resolution_input.setPlaceholderText("1280x720")
        self.proxy_layout.addWidget(self.proxy_resolution_container)
        
        # Proxy codec
        self.proxy_codec_container, self.proxy_codec_input = create_input_field("Codec:")
        self.proxy_codec_input.setPlaceholderText("h264")
        self.proxy_layout.addWidget(self.proxy_codec_container)
        
        # Proxy CRF
        self.proxy_crf_container, self.proxy_crf_input = create_input_field("CRF Value:")
        self.proxy_crf_input.setPlaceholderText("23")
        self.proxy_layout.addWidget(self.proxy_crf_container)
        
        # Add proxy container to video layout
        self.video_layout.addWidget(self.proxy_container)
        self.proxy_container.setVisible(False)
        
        # Add video group to content layout
        content_layout.addWidget(self.video_group)
        
        # DaVinci Template path
        self.davinci_group, self.davinci_layout = create_group_box("DaVinci Resolve")
        
        # Template path selector
        self.template_path_container, self.template_path_label, self.template_path_button = create_directory_selector("Template Path:")
        self.davinci_layout.addWidget(self.template_path_container)
        
        # Add DaVinci group to content layout
        content_layout.addWidget(self.davinci_group)
        
        # Logging settings group
        self.logging_group, self.logging_layout = create_group_box("Logging")
        
        # Log level input
        self.log_level_container, self.log_level_input = create_input_field("Log Level:")
        self.log_level_input.setPlaceholderText("INFO, DEBUG, WARNING, ERROR")
        self.logging_layout.addWidget(self.log_level_container)
        
        # Log file path
        self.log_path_container, self.log_path_label, self.log_path_button = create_directory_selector("Log Directory:")
        self.logging_layout.addWidget(self.log_path_container)
        
        # Add logging group to content layout
        content_layout.addWidget(self.logging_group)
        
        # Add separator
        content_layout.addWidget(create_horizontal_separator())
        
        # Add save button container
        button_container = QWidget()
        self.button_layout = QHBoxLayout(button_container)
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.addStretch(1)
        
        self.save_button = create_button("Save Configuration")
        self.button_layout.addWidget(self.save_button)
        
        self.reset_button = create_button("Reset", primary=False)
        self.button_layout.addWidget(self.reset_button)
        
        self.button_layout.addStretch(1)
        content_layout.addWidget(button_container)
        
        # Add spacer to content layout
        content_layout.addStretch(1)
        
        # Set the content widget as the scroll area's widget
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to the main layout
        self.layout.addWidget(scroll_area)
        
        # Connect signals
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals and slots."""
        # Connect directory browse buttons
        self.raw_path_button.clicked.connect(lambda: self.browse_directory(self.raw_path_label, "Select RAW Directory"))
        self.master_path_button.clicked.connect(lambda: self.browse_directory(self.master_path_label, "Select MASTER Directory"))
        self.template_path_button.clicked.connect(lambda: self.browse_file(self.template_path_label, "Select DaVinci Template", "DaVinci Resolve Project (*.drp)"))
        self.log_path_button.clicked.connect(lambda: self.browse_directory(self.log_path_label, "Select Log Directory"))
        
        # Connect checkbox
        self.create_proxies_checkbox.stateChanged.connect(self.toggle_proxy_settings)
        
        # Connect buttons
        self.save_button.clicked.connect(self.save_config)
        self.reset_button.clicked.connect(self.load_config)
    
    def browse_directory(self, label, caption):
        """Open directory browser dialog."""
        directory = QFileDialog.getExistingDirectory(self, caption)
        if directory:
            label.setText(directory)
    
    def browse_file(self, label, caption, filter_str):
        """Open file browser dialog."""
        file_path, _ = QFileDialog.getOpenFileName(self, caption, "", filter_str)
        if file_path:
            label.setText(file_path)
    
    def toggle_proxy_settings(self, state):
        """Show or hide proxy settings based on checkbox state."""
        self.proxy_container.setVisible(state == Qt.CheckState.Checked)
    
    def load_config(self):
        """Load configuration from file."""
        try:
            # Get the config file path
            script_dir = Path(__file__).resolve().parent.parent.parent.parent
            config_path = script_dir / 'config' / 'config.json'
            
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Set UI values from config
                self.raw_path_label.setText(config.get('raw_path', 'No directory selected'))
                self.master_path_label.setText(config.get('master_path', 'No directory selected'))
                self.ssd_name_input.setText(config.get('ssd_name', ''))
                
                # Set video extensions
                extensions = config.get('video_extensions', [])
                self.extensions_input.setText(', '.join(extensions))
                
                # Set proxy settings
                create_proxies = config.get('create_proxies', False)
                self.create_proxies_checkbox.setChecked(create_proxies)
                self.proxy_container.setVisible(create_proxies)
                
                proxy_settings = config.get('proxy_settings', {})
                self.proxy_resolution_input.setText(proxy_settings.get('resolution', '1280x720'))
                self.proxy_codec_input.setText(proxy_settings.get('codec', 'h264'))
                self.proxy_crf_input.setText(str(proxy_settings.get('crf', 23)))
                
                # Set DaVinci template path
                self.template_path_label.setText(config.get('davinci_template_path', 'No file selected'))
                
                # Set logging settings
                logging_config = config.get('logging', {})
                self.log_level_input.setText(logging_config.get('level', 'INFO'))
                
                log_path = logging_config.get('file_path', '../logs/workflow.log')
                log_dir = os.path.dirname(log_path)
                self.log_path_label.setText(log_dir if log_dir else 'No directory selected')
        except Exception as e:
            show_error(self, "Error", f"Failed to load configuration: {e}")
    
    def save_config(self):
        """Save configuration to file."""
        try:
            # Create config dictionary
            config = {
                'raw_path': self.raw_path_label.text() if self.raw_path_label.text() != 'No directory selected' else '',
                'master_path': self.master_path_label.text() if self.master_path_label.text() != 'No directory selected' else '',
                'ssd_name': self.ssd_name_input.text(),
                'video_extensions': [ext.strip() for ext in self.extensions_input.text().split(',') if ext.strip()],
                'create_proxies': self.create_proxies_checkbox.isChecked(),
                'proxy_settings': {
                    'resolution': self.proxy_resolution_input.text(),
                    'codec': self.proxy_codec_input.text(),
                    'crf': int(self.proxy_crf_input.text()) if self.proxy_crf_input.text().isdigit() else 23
                },
                'davinci_template_path': self.template_path_label.text() if self.template_path_label.text() != 'No file selected' else '',
                'logging': {
                    'level': self.log_level_input.text(),
                    'file_path': f"{self.log_path_label.text()}/workflow.log" if self.log_path_label.text() != 'No directory selected' else '../logs/workflow.log',
                    'max_size_mb': 10,
                    'backup_count': 5
                }
            }
            
            # Get the config file path
            script_dir = Path(__file__).resolve().parent.parent.parent.parent
            config_path = script_dir / 'config' / 'config.json'
            
            # Create config directory if it doesn't exist
            os.makedirs(config_path.parent, exist_ok=True)
            
            # Write config to file
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            # Emit signal
            self.config_saved.emit(config)
            
            show_info(self, "Success", "Configuration saved successfully")
        except Exception as e:
            show_error(self, "Error", f"Failed to save configuration: {e}")
    
    def run(self):
        """Run the configuration workflow."""
        # Just save the configuration
        self.save_config()
    
    def stop(self):
        """Stop the configuration workflow."""
        # Nothing to stop
        pass
