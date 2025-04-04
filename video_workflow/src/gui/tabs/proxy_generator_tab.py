"""
Proxy Generator Tab for the Video Workflow Application
"""

import os
import sys
import json
import threading
import subprocess
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QComboBox, QSpinBox, QFileDialog, QSizePolicy,
    QScrollArea, QFrame, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal

# Import UI template components
from ..ui_template import (
    create_group_box, create_button, create_directory_selector,
    create_input_field, create_progress_bar, create_combo_box,
    show_info, show_error, create_list_widget, create_text_edit,
    create_horizontal_separator
)

class ProxyGeneratorTab(QWidget):
    """Proxy generator tab for creating proxy video files."""
    
    # Signals for thread-safe UI updates
    log_message_signal = pyqtSignal(str)
    file_found_signal = pyqtSignal(str)
    proxy_progress_signal = pyqtSignal(int, int)  # current, total
    proxy_complete_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Initialize properties
        self.is_running = False
        self.proxy_thread = None
        
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
        
        # Source and destination group
        self.paths_group, self.paths_layout = create_group_box("Source and Destination")
        
        # Source directory selector
        self.source_dir_container, self.source_dir_label, self.source_dir_button = create_directory_selector("Source Directory:")
        self.paths_layout.addWidget(self.source_dir_container)
        
        # Destination directory selector
        self.dest_dir_container, self.dest_dir_label, self.dest_dir_button = create_directory_selector("Proxies Directory:")
        self.paths_layout.addWidget(self.dest_dir_container)
        
        # Add paths group to content layout
        content_layout.addWidget(self.paths_group)
        
        # Proxy settings group
        self.settings_group, self.settings_layout = create_group_box("Proxy Settings")
        
        # Resolution input
        self.resolution_container, self.resolution_input = create_input_field("Resolution:")
        self.resolution_input.setPlaceholderText("1280x720")
        self.settings_layout.addWidget(self.resolution_container)
        
        # Codec selection
        codec_container = QWidget()
        codec_layout = QHBoxLayout(codec_container)
        codec_layout.setContentsMargins(10, 5, 10, 5)
        
        codec_label = QLabel("Codec:")
        codec_label.setStyleSheet("""
            font-size: 12pt;
            font-weight: bold;
            background-color: transparent;
            border: none;
            padding: 5px;
            color: #E0E0E0;
            min-width: 150px;
            max-width: 200px;
        """)
        codec_label.setFixedWidth(150)
        codec_layout.addWidget(codec_label)
        
        self.codec_combo = create_combo_box(["h264", "h265", "prores", "dnxhd"])
        codec_layout.addWidget(self.codec_combo)
        
        self.settings_layout.addWidget(codec_container)
        
        # CRF value - custom implementation with visible controls
        crf_container = QWidget()
        crf_layout = QHBoxLayout(crf_container)
        crf_layout.setContentsMargins(10, 5, 10, 5)
        
        crf_label = QLabel("CRF Value:")
        crf_label.setStyleSheet("""
            font-size: 12pt;
            font-weight: bold;
            background-color: transparent;
            border: none;
            padding: 5px;
            color: #E0E0E0;
            min-width: 150px;
            max-width: 200px;
        """)
        crf_label.setFixedWidth(150)
        crf_layout.addWidget(crf_label)
        
        # Create a custom control with visible buttons
        crf_control = QWidget()
        crf_control_layout = QHBoxLayout(crf_control)
        crf_control_layout.setContentsMargins(0, 0, 0, 0)
        crf_control_layout.setSpacing(0)
        
        # Create the value display
        self.crf_value = QLineEdit("23")
        self.crf_value.setReadOnly(True)
        self.crf_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.crf_value.setFixedWidth(50)
        self.crf_value.setStyleSheet("""
            QLineEdit {
                font-size: 12pt;
                min-height: 30px;
                background-color: #3E3E42;
                border: 1px solid #555555;
                color: #E0E0E0;
                padding: 2px 5px;
            }
        """)
        
        # Create up and down buttons with text
        self.crf_up = QPushButton("+")
        self.crf_up.setFixedSize(30, 30)
        self.crf_up.setStyleSheet("""
            QPushButton {
                font-size: 16pt;
                font-weight: bold;
                background-color: #777777;
                border: 1px solid #555555;
                border-radius: 4px;
                color: white;
            }
            QPushButton:hover {
                background-color: #999999;
            }
        """)
        
        self.crf_down = QPushButton("-")
        self.crf_down.setFixedSize(30, 30)
        self.crf_down.setStyleSheet("""
            QPushButton {
                font-size: 16pt;
                font-weight: bold;
                background-color: #777777;
                border: 1px solid #555555;
                border-radius: 4px;
                color: white;
            }
            QPushButton:hover {
                background-color: #999999;
            }
        """)
        
        # Add components to layout
        crf_control_layout.addWidget(self.crf_down)
        crf_control_layout.addWidget(self.crf_value)
        crf_control_layout.addWidget(self.crf_up)
        
        # Connect signals
        self.crf_value_int = 23  # Store the actual integer value
        self.crf_up.clicked.connect(self.increment_crf)
        self.crf_down.clicked.connect(self.decrement_crf)
        
        crf_layout.addWidget(crf_control)
        
        self.settings_layout.addWidget(crf_container)
        
        # Add settings group to content layout
        content_layout.addWidget(self.settings_group)
        
        # File list group
        self.files_group, self.files_layout = create_group_box("Source Files")
        
        # File list
        self.file_list = create_list_widget()
        self.files_layout.addWidget(self.file_list)
        
        # Scan button
        scan_button_layout = QHBoxLayout()
        scan_button_layout.addStretch()
        
        self.scan_button = create_button("Scan for Video Files")
        scan_button_layout.addWidget(self.scan_button)
        
        scan_button_layout.addStretch()
        self.files_layout.addLayout(scan_button_layout)
        
        # Add files group to content layout
        content_layout.addWidget(self.files_group)
        
        # Progress group
        self.progress_group, self.progress_layout = create_group_box("Conversion Progress")
        
        # Progress bar
        self.progress_container, self.progress_bar = create_progress_bar("Overall Progress")
        self.progress_layout.addWidget(self.progress_container)
        
        # Current file label
        self.current_file_label = QLabel("No conversion in progress")
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
        
        self.generate_button = create_button("Generate Proxies")
        self.generate_button.setEnabled(False)
        self.button_layout.addWidget(self.generate_button)
        
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
        self.dest_dir_button.clicked.connect(lambda: self.browse_directory(self.dest_dir_label, "Select Proxies Directory"))
        self.scan_button.clicked.connect(self.scan_video_files)
        self.generate_button.clicked.connect(self.generate_proxies)
        self.cancel_button.clicked.connect(self.cancel_generation)
        
        # Connect thread signals
        self.log_message_signal.connect(self.log_message)
        self.file_found_signal.connect(self.on_file_found)
        self.proxy_progress_signal.connect(self.update_progress)
        self.proxy_complete_signal.connect(self.on_proxy_complete)
    
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
                
                # Set source directory from raw_path
                raw_path = config.get('raw_path', '')
                if raw_path:
                    self.source_dir_label.setText(raw_path)
                
                # Set proxy settings
                proxy_settings = config.get('proxy_settings', {})
                self.resolution_input.setText(proxy_settings.get('resolution', '1280x720'))
                
                codec = proxy_settings.get('codec', 'h264')
                index = self.codec_combo.findText(codec)
                if index >= 0:
                    self.codec_combo.setCurrentIndex(index)
                
                self.crf_spin.setValue(proxy_settings.get('crf', 23))
        except Exception as e:
            self.log_message(f"Failed to load configuration: {e}")
    
    def scan_video_files(self):
        """Scan for video files in the source directory."""
        try:
            source_dir = self.source_dir_label.text()
            if source_dir == "No directory selected" or not os.path.isdir(source_dir):
                show_error(self, "Error", "Please select a valid source directory")
                return
            
            self.log_message(f"Scanning for video files in {source_dir}...")
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
            self.log_message(f"Error scanning for video files: {e}")
            show_error(self, "Error", f"Failed to scan for video files: {e}")
    
    def scan_directory(self, directory, extensions):
        """Scan directory for video files in a separate thread."""
        try:
            # Show progress message
            self.log_message_signal.emit("Starting file scan (this may take a moment)...")
            
            # Create a set of extensions for faster lookup
            ext_set = set(extensions)
            count = 0
            max_files = 1000  # Limit to prevent excessive scanning
            
            # Use a more efficient approach with a progress indicator
            for root, dirs, files in os.walk(directory):
                # Skip hidden directories (starting with .)
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                # Update progress every 10 directories
                if count % 10 == 0:
                    self.log_message_signal.emit(f"Scanning... found {count} files so far")
                
                # Process files in this directory
                for file in files:
                    # Check extension using set membership for speed
                    if any(file.lower().endswith(ext) for ext in ext_set):
                        file_path = os.path.join(root, file)
                        self.file_found_signal.emit(file_path)
                        count += 1
                        
                        # Limit the number of files to prevent excessive scanning
                        if count >= max_files:
                            self.log_message_signal.emit(f"Reached limit of {max_files} files. Stopping scan.")
                            self.log_message_signal.emit(f"Found {count} video files (limited to first {max_files})")
                            return
            
            if count == 0:
                self.log_message_signal.emit("No video files found")
            else:
                self.log_message_signal.emit(f"Found {count} video files")
        except Exception as e:
            self.log_message_signal.emit(f"Error scanning directory: {e}")
    
    def on_file_found(self, file_path):
        """Handle video file found."""
        self.file_list.addItem(file_path)
        
        # Enable generate button if files are found
        self.generate_button.setEnabled(self.file_list.count() > 0)
    
    def generate_proxies(self):
        """Generate proxy files."""
        try:
            # Validate inputs
            source_dir = self.source_dir_label.text()
            if source_dir == "No directory selected" or not os.path.isdir(source_dir):
                show_error(self, "Error", "Please select a valid source directory")
                return
            
            dest_dir = self.dest_dir_label.text()
            if dest_dir == "No directory selected" or not os.path.isdir(dest_dir):
                show_error(self, "Error", "Please select a valid destination directory")
                return
            
            resolution = self.resolution_input.text().strip()
            if not resolution:
                show_error(self, "Error", "Please enter a valid resolution (e.g. 1280x720)")
                return
            
            # Get files to convert
            files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
            if not files:
                show_error(self, "Error", "No files to convert")
                return
            
            # Update UI
            self.generate_button.setEnabled(False)
            self.cancel_button.setEnabled(True)
            self.progress_bar.setValue(0)
            self.current_file_label.setText("Preparing to convert...")
            
            # Get proxy settings
            codec = self.codec_combo.currentText()
            crf = self.crf_value_int
            
            # Start proxy generation thread
            self.is_running = True
            self.proxy_thread = threading.Thread(
                target=self.convert_files,
                args=(files, dest_dir, resolution, codec, crf),
                daemon=True
            )
            self.proxy_thread.start()
            
            self.log_message(f"Started generating proxies for {len(files)} files")
        except Exception as e:
            self.log_message(f"Error starting proxy generation: {e}")
            show_error(self, "Error", f"Failed to start proxy generation: {e}")
    
    def convert_files(self, files, dest_dir, resolution, codec, crf):
        """Convert files in a separate thread."""
        try:
            total_files = len(files)
            
            for i, file_path in enumerate(files):
                if not self.is_running:
                    self.log_message_signal.emit("Proxy generation cancelled")
                    break
                
                # Get file name
                file_name = os.path.basename(file_path)
                base_name, _ = os.path.splitext(file_name)
                
                # Create destination path
                dest_path = os.path.join(dest_dir, f"{base_name}_proxy.mp4")
                
                # Update UI
                self.log_message_signal.emit(f"Converting {file_name}...")
                self.current_file_label.setText(f"Converting: {file_name}")
                
                # Convert file
                success = self.convert_file(file_path, dest_path, resolution, codec, crf)
                
                if success:
                    self.log_message_signal.emit(f"Successfully converted {file_name}")
                else:
                    self.log_message_signal.emit(f"Failed to convert {file_name}")
                
                # Update progress
                self.proxy_progress_signal.emit(i + 1, total_files)
            
            self.proxy_complete_signal.emit()
        except Exception as e:
            self.log_message_signal.emit(f"Error during proxy generation: {e}")
    
    def convert_file(self, source, destination, resolution, codec, crf):
        """Convert a file using ffmpeg."""
        try:
            # Build ffmpeg command
            cmd = [
                "ffmpeg",
                "-i", source,
                "-vf", f"scale={resolution}",
                "-c:v", codec,
                "-crf", str(crf),
                "-preset", "fast",
                "-c:a", "aac",
                "-b:a", "128k",
                "-y",  # Overwrite output files
                destination
            ]
            
            # Run ffmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Wait for process to complete
            stdout, stderr = process.communicate()
            
            # Check if successful
            if process.returncode != 0:
                self.log_message_signal.emit(f"ffmpeg error: {stderr}")
                return False
            
            return True
        except Exception as e:
            self.log_message_signal.emit(f"Error converting file {source}: {e}")
            return False
    
    def update_progress(self, current, total):
        """Update the progress bar."""
        progress = int((current / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(progress)
    
    def on_proxy_complete(self):
        """Handle proxy generation completion."""
        self.generate_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.current_file_label.setText("Proxy generation completed")
        self.log_message("Proxy generation completed")
        show_info(self, "Success", "Proxy files generated successfully")
    
    def cancel_generation(self):
        """Cancel the proxy generation."""
        self.is_running = False
        self.cancel_button.setEnabled(False)
        self.log_message("Cancelling proxy generation...")
    
    def increment_crf(self):
        """Increment the CRF value."""
        if self.crf_value_int < 51:  # Maximum CRF value
            self.crf_value_int += 1
            self.crf_value.setText(str(self.crf_value_int))
    
    def decrement_crf(self):
        """Decrement the CRF value."""
        if self.crf_value_int > 0:  # Minimum CRF value
            self.crf_value_int -= 1
            self.crf_value.setText(str(self.crf_value_int))
            
    def log_message(self, message):
        """Add a message to the log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def run(self):
        """Run the proxy generation workflow."""
        # Scan for video files if none are in the list
        if self.file_list.count() == 0:
            self.scan_video_files()
        else:
            self.generate_proxies()
    
    def stop(self):
        """Stop the proxy generation workflow."""
        if self.is_running:
            self.cancel_generation()
