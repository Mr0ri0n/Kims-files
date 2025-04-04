"""
Upload Tab for the Video Workflow Application
"""

import os
import sys
import json
import time
import threading
import hashlib
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QFileDialog, QLineEdit, QSizePolicy,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

# Import UI template components
from ..ui_template import (
    create_group_box, create_button, create_directory_selector,
    create_input_field, create_checkbox, create_progress_bar,
    show_info, show_error, create_list_widget, create_text_edit,
    create_horizontal_separator
)

class UploadTab(QWidget):
    """Upload tab for uploading files to Playbook or other platforms."""
    
    # Signals for thread-safe UI updates
    log_message_signal = pyqtSignal(str)
    file_found_signal = pyqtSignal(str)
    upload_progress_signal = pyqtSignal(int, int)  # current, total
    upload_complete_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Initialize properties
        self.is_running = False
        self.upload_thread = None
        
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
        
        # API settings group
        self.api_group, self.api_layout = create_group_box("API Settings")
        
        # API key input
        self.api_key_container, self.api_key_input = create_input_field("API Key:")
        self.api_key_input.setPlaceholderText("Enter your API key")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_layout.addWidget(self.api_key_container)
        
        # API endpoint input
        self.api_endpoint_container, self.api_endpoint_input = create_input_field("API Endpoint:")
        self.api_endpoint_input.setPlaceholderText("https://api.example.com/upload")
        self.api_layout.addWidget(self.api_endpoint_container)
        
        # Add API group to content layout
        content_layout.addWidget(self.api_group)
        
        # Source directory group
        self.source_group, self.source_layout = create_group_box("Source Files")
        
        # Source directory selector
        self.source_dir_container, self.source_dir_label, self.source_dir_button = create_directory_selector("Source Directory:")
        self.source_layout.addWidget(self.source_dir_container)
        
        # File list
        self.file_list = create_list_widget()
        self.source_layout.addWidget(self.file_list)
        
        # Scan button
        scan_button_layout = QHBoxLayout()
        scan_button_layout.addStretch()
        
        self.scan_button = create_button("Scan for Files")
        scan_button_layout.addWidget(self.scan_button)
        
        scan_button_layout.addStretch()
        self.source_layout.addLayout(scan_button_layout)
        
        # Add source group to content layout
        content_layout.addWidget(self.source_group)
        
        # Options group
        self.options_group, self.options_layout = create_group_box("Upload Options")
        
        # Avoid duplicates checkbox
        self.avoid_duplicates_checkbox = create_checkbox("Avoid uploading duplicates")
        self.avoid_duplicates_checkbox.setChecked(True)
        self.options_layout.addWidget(self.avoid_duplicates_checkbox)
        
        # Add options group to content layout
        content_layout.addWidget(self.options_group)
        
        # Progress group
        self.progress_group, self.progress_layout = create_group_box("Upload Progress")
        
        # Progress bar
        self.progress_container, self.progress_bar = create_progress_bar("Overall Progress")
        self.progress_layout.addWidget(self.progress_container)
        
        # Current file label
        self.current_file_label = QLabel("No upload in progress")
        self.current_file_label.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
            padding: 5px;
        """)
        self.progress_layout.addWidget(self.current_file_label)
        
        # Add progress group to content layout
        content_layout.addWidget(self.progress_group)
        
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
        
        self.upload_button = create_button("Upload Files")
        self.upload_button.setEnabled(False)
        self.button_layout.addWidget(self.upload_button)
        
        self.cancel_button = create_button("Cancel", primary=False)
        self.cancel_button.setEnabled(False)
        self.button_layout.addWidget(self.cancel_button)
        
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
        self.source_dir_button.clicked.connect(lambda: self.browse_directory(self.source_dir_label, "Select Source Directory"))
        self.scan_button.clicked.connect(self.scan_files)
        self.upload_button.clicked.connect(self.upload_files)
        self.cancel_button.clicked.connect(self.cancel_upload)
        
        # Connect thread signals
        self.log_message_signal.connect(self.log_message)
        self.file_found_signal.connect(self.on_file_found)
        self.upload_progress_signal.connect(self.update_progress)
        self.upload_complete_signal.connect(self.on_upload_complete)
    
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
                
                # Set source directory from master_path
                master_path = config.get('master_path', '')
                if master_path:
                    self.source_dir_label.setText(master_path)
        except Exception as e:
            self.log_message(f"Failed to load configuration: {e}")
    
    def scan_files(self):
        """Scan for files in the source directory."""
        try:
            source_dir = self.source_dir_label.text()
            if source_dir == "No directory selected" or not os.path.isdir(source_dir):
                show_error(self, "Error", "Please select a valid source directory")
                return
            
            self.log_message(f"Scanning for files in {source_dir}...")
            self.file_list.clear()
            
            # Get video extensions from config
            script_dir = Path(__file__).resolve().parent.parent.parent.parent
            config_path = script_dir / 'config' / 'config.json'
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            video_extensions = config.get('video_extensions', [".mp4", ".mov"])
            
            # Start scan thread
            threading.Thread(
                target=self.scan_directory,
                args=(source_dir, video_extensions),
                daemon=True
            ).start()
        except Exception as e:
            self.log_message(f"Error scanning for files: {e}")
            show_error(self, "Error", f"Failed to scan for files: {e}")
    
    def scan_directory(self, directory, extensions):
        """Scan directory for files in a separate thread."""
        try:
            count = 0
            for root, _, files in os.walk(directory):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        file_path = os.path.join(root, file)
                        self.file_found_signal.emit(file_path)
                        count += 1
            
            if count == 0:
                self.log_message_signal.emit("No files found")
            else:
                self.log_message_signal.emit(f"Found {count} files")
        except Exception as e:
            self.log_message_signal.emit(f"Error scanning directory: {e}")
    
    def on_file_found(self, file_path):
        """Handle file found."""
        self.file_list.addItem(file_path)
        
        # Enable upload button if files are found
        self.upload_button.setEnabled(self.file_list.count() > 0)
    
    def upload_files(self):
        """Upload files to the API endpoint."""
        try:
            # Validate inputs
            api_key = self.api_key_input.text().strip()
            if not api_key:
                show_error(self, "Error", "Please enter an API key")
                return
            
            api_endpoint = self.api_endpoint_input.text().strip()
            if not api_endpoint:
                show_error(self, "Error", "Please enter an API endpoint")
                return
            
            # Get files to upload
            files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
            if not files:
                show_error(self, "Error", "No files to upload")
                return
            
            # Update UI
            self.upload_button.setEnabled(False)
            self.cancel_button.setEnabled(True)
            self.progress_bar.setValue(0)
            self.current_file_label.setText("Preparing to upload...")
            
            # Start upload thread
            self.is_running = True
            self.upload_thread = threading.Thread(
                target=self.upload_to_api,
                args=(files, api_endpoint, api_key),
                daemon=True
            )
            self.upload_thread.start()
            
            self.log_message(f"Started uploading {len(files)} files")
        except Exception as e:
            self.log_message(f"Error starting upload: {e}")
            show_error(self, "Error", f"Failed to start upload: {e}")
    
    def upload_to_api(self, files, api_endpoint, api_key):
        """Upload files to API in a separate thread."""
        try:
            total_files = len(files)
            
            for i, file_path in enumerate(files):
                if not self.is_running:
                    self.log_message_signal.emit("Upload cancelled")
                    break
                
                # Get file name
                file_name = os.path.basename(file_path)
                
                # Update UI
                self.log_message_signal.emit(f"Uploading {file_name}...")
                self.current_file_label.setText(f"Uploading: {file_name}")
                
                # Check for duplicates if enabled
                if self.avoid_duplicates_checkbox.isChecked():
                    file_hash = self.calculate_file_hash(file_path)
                    is_duplicate = self.check_duplicate(file_hash, api_endpoint, api_key)
                    
                    if is_duplicate:
                        self.log_message_signal.emit(f"Skipping duplicate file: {file_name}")
                        self.upload_progress_signal.emit(i + 1, total_files)
                        continue
                
                # Upload file
                success = self.upload_file(file_path, api_endpoint, api_key)
                
                if success:
                    self.log_message_signal.emit(f"Successfully uploaded {file_name}")
                else:
                    self.log_message_signal.emit(f"Failed to upload {file_name}")
                
                # Update progress
                self.upload_progress_signal.emit(i + 1, total_files)
            
            self.upload_complete_signal.emit()
        except Exception as e:
            self.log_message_signal.emit(f"Error during upload: {e}")
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file."""
        try:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
            return md5_hash.hexdigest()
        except Exception as e:
            self.log_message_signal.emit(f"Error calculating file hash: {e}")
            return None
    
    def check_duplicate(self, file_hash, api_endpoint, api_key):
        """Check if a file with the same hash already exists."""
        try:
            # This is a placeholder implementation
            # In a real application, you would make an API call to check for duplicates
            
            # Simulate API call
            time.sleep(0.5)
            
            # For demonstration, always return False (no duplicate)
            return False
        except Exception as e:
            self.log_message_signal.emit(f"Error checking for duplicates: {e}")
            return False
    
    def upload_file(self, file_path, api_endpoint, api_key):
        """Upload a file to the API endpoint."""
        try:
            # This is a placeholder implementation
            # In a real application, you would make an API call to upload the file
            
            # Simulate API call with delay based on file size
            file_size = os.path.getsize(file_path)
            # Simulate 1MB/s upload speed
            upload_time = file_size / (1024 * 1024)
            # Cap at 10 seconds for demonstration
            upload_time = min(upload_time, 10)
            
            time.sleep(upload_time)
            
            # For demonstration, always return True (success)
            return True
        except Exception as e:
            self.log_message_signal.emit(f"Error uploading file {file_path}: {e}")
            return False
    
    def update_progress(self, current, total):
        """Update the progress bar."""
        progress = int((current / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(progress)
    
    def on_upload_complete(self):
        """Handle upload completion."""
        self.upload_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.current_file_label.setText("Upload completed")
        self.log_message("Upload completed")
        show_info(self, "Success", "Files uploaded successfully")
    
    def cancel_upload(self):
        """Cancel the upload."""
        self.is_running = False
        self.cancel_button.setEnabled(False)
        self.log_message("Cancelling upload...")
    
    def log_message(self, message):
        """Add a message to the log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def run(self):
        """Run the upload workflow."""
        # Scan for files if none are in the list
        if self.file_list.count() == 0:
            self.scan_files()
        else:
            self.upload_files()
    
    def stop(self):
        """Stop the upload workflow."""
        if self.is_running:
            self.cancel_upload()
