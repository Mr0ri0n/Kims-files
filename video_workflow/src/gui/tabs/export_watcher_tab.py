"""
Export Watcher Tab for the Video Workflow Application
"""

import os
import sys
import json
import time
import shutil
import threading
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QFileDialog, QSizePolicy, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

# Import UI template components
from ..ui_template import (
    create_group_box, create_button, create_directory_selector,
    create_checkbox, show_info, show_error, create_list_widget, 
    create_text_edit, create_horizontal_separator
)

class ExportWatcherTab(QWidget):
    """Export watcher tab for monitoring and moving exported files."""
    
    # Signals for thread-safe UI updates
    log_message_signal = pyqtSignal(str)
    file_detected_signal = pyqtSignal(str)
    file_moved_signal = pyqtSignal(str, str)  # source, destination
    
    def __init__(self):
        super().__init__()
        
        # Initialize properties
        self.is_running = False
        self.watcher_thread = None
        
        # Initialize UI
        self.init_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Load config
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
        
        # Directory settings group
        self.dirs_group, self.dirs_layout = create_group_box("Directory Settings")
        
        # Watch directory selector
        self.watch_dir_container, self.watch_dir_label, self.watch_dir_button = create_directory_selector("Watch Directory:")
        self.dirs_layout.addWidget(self.watch_dir_container)
        
        # Destination directory selector
        self.dest_dir_container, self.dest_dir_label, self.dest_dir_button = create_directory_selector("Destination Directory:")
        self.dirs_layout.addWidget(self.dest_dir_container)
        
        # Add dirs group to content layout
        content_layout.addWidget(self.dirs_group)
        
        # Options group
        self.options_group, self.options_layout = create_group_box("Options")
        
        # Auto-rename checkbox
        self.rename_checkbox = create_checkbox("Auto-rename files with timestamp")
        self.rename_checkbox.setChecked(True)
        self.options_layout.addWidget(self.rename_checkbox)
        
        # Create dated folders checkbox
        self.dated_folders_checkbox = create_checkbox("Create dated folders")
        self.dated_folders_checkbox.setChecked(True)
        self.options_layout.addWidget(self.dated_folders_checkbox)
        
        # Add options group to content layout
        content_layout.addWidget(self.options_group)
        
        # Detected files group
        self.files_group, self.files_layout = create_group_box("Detected Files")
        
        # Files list
        self.file_list = create_list_widget()
        self.files_layout.addWidget(self.file_list)
        
        # Add files group to content layout
        content_layout.addWidget(self.files_group)
        
        # Log group
        self.log_group, self.log_layout = create_group_box("Activity Log")
        
        # Log text area
        self.log_text = create_text_edit()
        self.log_layout.addWidget(self.log_text)
        
        # Add log group to content layout
        content_layout.addWidget(self.log_group)
        
        # Add separator
        content_layout.addWidget(create_horizontal_separator())
        
        # Add buttons container
        button_container = QWidget()
        self.button_layout = QHBoxLayout(button_container)
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.addStretch(1)
        
        self.start_button = create_button("Start Watching")
        self.button_layout.addWidget(self.start_button)
        
        self.stop_button = create_button("Stop Watching", primary=False)
        self.stop_button.setEnabled(False)
        self.button_layout.addWidget(self.stop_button)
        
        self.button_layout.addStretch(1)
        content_layout.addWidget(button_container)
        
        # Add spacer to content layout
        content_layout.addStretch(1)
        
        # Set the content widget as the scroll area's widget
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to the main layout
        self.layout.addWidget(scroll_area)
    
    def connect_signals(self):
        """Connect signals and slots."""
        # Connect buttons
        self.watch_dir_button.clicked.connect(lambda: self.browse_directory(self.watch_dir_label, "Select Watch Directory"))
        self.dest_dir_button.clicked.connect(lambda: self.browse_directory(self.dest_dir_label, "Select Destination Directory"))
        self.start_button.clicked.connect(self.start_watching)
        self.stop_button.clicked.connect(self.stop_watching)
        
        # Connect thread signals
        self.log_message_signal.connect(self.log_message)
        self.file_detected_signal.connect(self.on_file_detected)
        self.file_moved_signal.connect(self.on_file_moved)
    
    def browse_directory(self, label, caption):
        """Open directory browser dialog."""
        directory = QFileDialog.getExistingDirectory(self, caption)
        if directory:
            label.setText(directory)
    
    def load_config(self):
        """Load configuration from file."""
        try:
            # Get the config file path
            script_dir = Path(__file__).resolve().parent.parent.parent.parent
            config_path = script_dir / 'config' / 'config.json'
            
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Set watch directory (this would typically be DaVinci's export folder)
                # For now, we'll use a placeholder
                
                # Set destination directory from master_path
                master_path = config.get('master_path', '')
                if master_path:
                    self.dest_dir_label.setText(master_path)
        except Exception as e:
            self.log_message(f"Failed to load configuration: {e}")
    
    def start_watching(self):
        """Start watching for exported files."""
        try:
            # Validate inputs
            watch_dir = self.watch_dir_label.text()
            if watch_dir == "No directory selected" or not os.path.isdir(watch_dir):
                show_error(self, "Error", "Please select a valid watch directory")
                return
            
            dest_dir = self.dest_dir_label.text()
            if dest_dir == "No directory selected" or not os.path.isdir(dest_dir):
                show_error(self, "Error", "Please select a valid destination directory")
                return
            
            # Update UI
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            
            # Start watcher thread
            self.is_running = True
            self.watcher_thread = threading.Thread(
                target=self.watch_directory,
                args=(watch_dir, dest_dir),
                daemon=True
            )
            self.watcher_thread.start()
            
            self.log_message(f"Started watching {watch_dir} for exported files")
        except Exception as e:
            self.log_message(f"Error starting watcher: {e}")
            show_error(self, "Error", f"Failed to start watcher: {e}")
    
    def watch_directory(self, watch_dir, dest_dir):
        """Watch directory for new files in a separate thread."""
        try:
            # Get initial list of files
            initial_files = set(os.path.join(watch_dir, f) for f in os.listdir(watch_dir) if os.path.isfile(os.path.join(watch_dir, f)))
            
            self.log_message_signal.emit(f"Found {len(initial_files)} existing files in watch directory")
            
            while self.is_running:
                try:
                    # Get current list of files
                    current_files = set(os.path.join(watch_dir, f) for f in os.listdir(watch_dir) if os.path.isfile(os.path.join(watch_dir, f)))
                    
                    # Check for new files
                    new_files = current_files - initial_files
                    if new_files:
                        for file_path in new_files:
                            self.file_detected_signal.emit(file_path)
                            
                            # Move the file
                            self.move_file(file_path, dest_dir)
                        
                        # Update initial files
                        initial_files = current_files
                    
                    # Sleep for a bit
                    time.sleep(2)
                except Exception as e:
                    self.log_message_signal.emit(f"Error watching directory: {e}")
                    time.sleep(5)  # Wait a bit longer if there's an error
        except Exception as e:
            self.log_message_signal.emit(f"Error in watcher thread: {e}")
    
    def move_file(self, source_path, dest_dir):
        """Move a file to the destination directory."""
        try:
            # Get file name
            file_name = os.path.basename(source_path)
            
            # Create destination path
            if self.dated_folders_checkbox.isChecked():
                # Create dated folder
                date_folder = datetime.now().strftime("%Y-%m-%d")
                dest_folder = os.path.join(dest_dir, date_folder)
                os.makedirs(dest_folder, exist_ok=True)
            else:
                dest_folder = dest_dir
            
            # Rename file if needed
            if self.rename_checkbox.isChecked():
                # Add timestamp to file name
                base_name, ext = os.path.splitext(file_name)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_file_name = f"{base_name}_{timestamp}{ext}"
            else:
                new_file_name = file_name
            
            # Create destination path
            dest_path = os.path.join(dest_folder, new_file_name)
            
            # Move file
            shutil.move(source_path, dest_path)
            
            # Signal file moved
            self.file_moved_signal.emit(source_path, dest_path)
        except Exception as e:
            self.log_message_signal.emit(f"Error moving file {source_path}: {e}")
    
    def on_file_detected(self, file_path):
        """Handle file detection."""
        file_name = os.path.basename(file_path)
        self.log_message(f"Detected new file: {file_name}")
        
        # Add to list
        self.file_list.addItem(file_name)
    
    def on_file_moved(self, source_path, dest_path):
        """Handle file moved."""
        source_name = os.path.basename(source_path)
        dest_name = os.path.basename(dest_path)
        
        self.log_message(f"Moved file: {source_name} -> {dest_path}")
    
    def stop_watching(self):
        """Stop watching for exported files."""
        self.is_running = False
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.log_message("Stopped watching for exported files")
    
    def log_message(self, message):
        """Add a message to the log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def run(self):
        """Run the export watcher workflow."""
        self.start_watching()
    
    def stop(self):
        """Stop the export watcher workflow."""
        if self.is_running:
            self.stop_watching()
