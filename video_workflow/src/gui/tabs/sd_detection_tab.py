"""
SD Card Detection Tab for the Video Workflow Application
"""

import os
import sys
import time
import threading
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QProgressBar, QSizePolicy, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

# Import UI template components
from ..ui_template import (
    create_group_box, create_button, create_progress_bar, 
    show_info, show_error, create_list_widget, create_text_edit,
    create_horizontal_separator
)

# Import disk monitor
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from disk_monitor import DiskMonitor

class SDDetectionTab(QWidget):
    """SD Card detection and file import tab."""
    
    # Signals for thread-safe UI updates
    sd_detected_signal = pyqtSignal(str)
    file_found_signal = pyqtSignal(str)
    copy_progress_signal = pyqtSignal(int, int)  # current, total
    copy_complete_signal = pyqtSignal()
    log_message_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize properties
        self.disk_monitor = DiskMonitor()
        self.sd_cards = []
        self.is_running = False
        self.copy_thread = None
        
        # Initialize UI
        self.init_ui()
        
        # Connect signals
        self.connect_signals()
    
    def init_ui(self):
        """Initialize the UI components."""
        # Set size policy to expand in both directions
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # Create a scrollable area for the entire content
        # This ensures content is accessible even when window is resized small
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create a widget to hold all content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)
        
        # SD Card detection group
        self.detection_group, self.detection_layout = create_group_box("SD Card Detection")
        
        # Status label
        self.status_label = QLabel("Not monitoring for SD cards")
        self.status_label.setWordWrap(True)  # Enable word wrapping
        self.detection_layout.addWidget(self.status_label)
        
        # SD Card list
        self.sd_list = create_list_widget()
        self.detection_layout.addWidget(self.sd_list)
        
        # Button layout - using a flow layout approach with wrapping
        detection_button_container = QWidget()
        detection_button_layout = QHBoxLayout(detection_button_container)
        detection_button_layout.setSpacing(10)
        detection_button_layout.setContentsMargins(0, 5, 0, 5)
        
        # Create a button container with a flow layout
        button_flow_widget = QWidget()
        button_flow_layout = QHBoxLayout(button_flow_widget)
        button_flow_layout.setSpacing(10)
        button_flow_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scan button
        self.scan_button = create_button("Scan for SD Cards")
        button_flow_layout.addWidget(self.scan_button)
        
        # Monitor button
        self.monitor_button = create_button("Start Monitoring")
        button_flow_layout.addWidget(self.monitor_button)
        
        button_flow_layout.addStretch(1)
        
        # Add the flow layout to the main button container
        detection_button_layout.addWidget(button_flow_widget)
        self.detection_layout.addWidget(detection_button_container)
        
        # Add detection group to content layout
        content_layout.addWidget(self.detection_group)
        
        # File import group
        self.import_group, self.import_layout = create_group_box("File Import")
        
        # File list
        self.file_list = create_list_widget()
        self.import_layout.addWidget(self.file_list)
        
        # Progress bar
        self.progress_container, self.progress_bar = create_progress_bar("Copy Progress")
        self.import_layout.addWidget(self.progress_container)
        
        # Button layout - using a flow layout approach with wrapping
        import_button_container = QWidget()
        import_button_layout = QHBoxLayout(import_button_container)
        import_button_layout.setSpacing(10)
        import_button_layout.setContentsMargins(0, 5, 0, 5)
        
        # Create a button container with a flow layout
        import_button_flow_widget = QWidget()
        import_button_flow_layout = QHBoxLayout(import_button_flow_widget)
        import_button_flow_layout.setSpacing(10)
        import_button_flow_layout.setContentsMargins(0, 0, 0, 0)
        
        # Import button
        self.import_button = create_button("Import Files")
        self.import_button.setEnabled(False)
        import_button_flow_layout.addWidget(self.import_button)
        
        # Cancel button
        self.cancel_button = create_button("Cancel", primary=False)
        self.cancel_button.setEnabled(False)
        import_button_flow_layout.addWidget(self.cancel_button)
        
        import_button_flow_layout.addStretch(1)
        
        # Add the flow layout to the main button container
        import_button_layout.addWidget(import_button_flow_widget)
        self.import_layout.addWidget(import_button_container)
        
        # Add import group to content layout
        content_layout.addWidget(self.import_group)
        
        # Log group
        self.log_group, self.log_layout = create_group_box("Activity Log")
        
        # Log text area
        self.log_text = create_text_edit()
        self.log_layout.addWidget(self.log_text)
        
        # Add log group to content layout
        content_layout.addWidget(self.log_group)
        
        # Add spacer to content layout
        content_layout.addStretch()
        
        # Set the content widget as the scroll area's widget
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to the main layout
        self.layout.addWidget(scroll_area)
    
    def connect_signals(self):
        """Connect signals and slots."""
        # Connect buttons
        self.scan_button.clicked.connect(self.scan_sd_cards)
        self.monitor_button.clicked.connect(self.toggle_monitoring)
        self.import_button.clicked.connect(self.import_files)
        self.cancel_button.clicked.connect(self.cancel_import)
        
        # Connect SD card list
        self.sd_list.itemClicked.connect(self.on_sd_card_selected)
        
        # Connect thread signals
        self.sd_detected_signal.connect(self.on_sd_detected)
        self.file_found_signal.connect(self.on_file_found)
        self.copy_progress_signal.connect(self.update_progress)
        self.copy_complete_signal.connect(self.on_copy_complete)
        self.log_message_signal.connect(self.log_message)
    
    def scan_sd_cards(self):
        """Scan for SD cards."""
        try:
            self.log_message("Scanning for SD cards...")
            self.sd_list.clear()
            self.file_list.clear()
            
            # Get SD cards
            self.sd_cards = self.disk_monitor.detect_sd_cards()
            
            if self.sd_cards:
                for sd_card in self.sd_cards:
                    self.sd_list.addItem(sd_card)
                self.log_message(f"Found {len(self.sd_cards)} SD card(s)")
            else:
                self.log_message("No SD cards found")
        except Exception as e:
            self.log_message(f"Error scanning for SD cards: {e}")
            show_error(self, "Error", f"Failed to scan for SD cards: {e}")
    
    def toggle_monitoring(self):
        """Toggle SD card monitoring."""
        if self.is_running:
            # Stop monitoring
            self.is_running = False
            self.monitor_button.setText("Start Monitoring")
            self.scan_button.setEnabled(True)
            self.status_label.setText("Not monitoring for SD cards")
            self.log_message("Stopped monitoring for SD cards")
        else:
            # Start monitoring
            self.is_running = True
            self.monitor_button.setText("Stop Monitoring")
            self.scan_button.setEnabled(False)
            self.status_label.setText("Monitoring for SD cards...")
            self.log_message("Started monitoring for SD cards")
            
            # Start monitoring thread
            threading.Thread(target=self.monitor_sd_cards, daemon=True).start()
    
    def monitor_sd_cards(self):
        """Monitor for SD cards in a separate thread."""
        initial_cards = set(self.disk_monitor.detect_sd_cards())
        
        while self.is_running:
            try:
                # Get current SD cards
                current_cards = set(self.disk_monitor.detect_sd_cards())
                
                # Check for new cards
                new_cards = current_cards - initial_cards
                if new_cards:
                    for card in new_cards:
                        self.sd_detected_signal.emit(card)
                    initial_cards = current_cards
                
                # Sleep for a bit
                time.sleep(2)
            except Exception as e:
                self.log_message_signal.emit(f"Error monitoring SD cards: {e}")
                time.sleep(5)  # Wait a bit longer if there's an error
    
    def on_sd_detected(self, sd_card):
        """Handle SD card detection."""
        # Add to list if not already there
        items = [self.sd_list.item(i).text() for i in range(self.sd_list.count())]
        if sd_card not in items:
            self.sd_list.addItem(sd_card)
            self.log_message(f"Detected new SD card: {sd_card}")
            
            # Automatically select the new card
            for i in range(self.sd_list.count()):
                if self.sd_list.item(i).text() == sd_card:
                    self.sd_list.setCurrentRow(i)
                    self.on_sd_card_selected(self.sd_list.item(i))
                    break
    
    def on_sd_card_selected(self, item):
        """Handle SD card selection."""
        sd_card = item.text()
        self.log_message(f"Selected SD card: {sd_card}")
        
        # Clear file list
        self.file_list.clear()
        
        # Scan for video files
        threading.Thread(target=self.scan_video_files, args=(sd_card,), daemon=True).start()
    
    def scan_video_files(self, sd_card):
        """Scan for video files on the selected SD card."""
        try:
            self.log_message_signal.emit(f"Scanning for video files on {sd_card}...")
            
            # Get video extensions from config (placeholder)
            video_extensions = [".mp4", ".mov"]
            
            # Walk the SD card directory
            for root, _, files in os.walk(sd_card):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        file_path = os.path.join(root, file)
                        self.file_found_signal.emit(file_path)
        except Exception as e:
            self.log_message_signal.emit(f"Error scanning for video files: {e}")
    
    def on_file_found(self, file_path):
        """Handle video file found."""
        self.file_list.addItem(file_path)
        
        # Enable import button if files are found
        self.import_button.setEnabled(self.file_list.count() > 0)
    
    def import_files(self):
        """Import files from the selected SD card."""
        try:
            # Get selected SD card
            if self.sd_list.currentItem() is None:
                show_error(self, "Error", "No SD card selected")
                return
            
            sd_card = self.sd_list.currentItem().text()
            
            # Get files to import
            files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
            if not files:
                show_error(self, "Error", "No files to import")
                return
            
            # Get destination path (placeholder)
            destination = "D:/RAW"
            
            # Create dated folder
            import datetime
            date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
            destination_folder = os.path.join(destination, date_folder, "footage")
            
            # Create destination folder if it doesn't exist
            os.makedirs(destination_folder, exist_ok=True)
            
            # Update UI
            self.import_button.setEnabled(False)
            self.cancel_button.setEnabled(True)
            self.progress_bar.setValue(0)
            
            # Start copy thread
            self.copy_thread = threading.Thread(
                target=self.copy_files,
                args=(files, destination_folder),
                daemon=True
            )
            self.copy_thread.start()
            
            self.log_message(f"Started importing {len(files)} files to {destination_folder}")
        except Exception as e:
            self.log_message(f"Error starting import: {e}")
            show_error(self, "Error", f"Failed to start import: {e}")
    
    def copy_files(self, files, destination):
        """Copy files in a separate thread."""
        try:
            total_files = len(files)
            
            for i, file_path in enumerate(files):
                if not self.is_running:
                    self.log_message_signal.emit("Import cancelled")
                    break
                
                # Get file name
                file_name = os.path.basename(file_path)
                
                # Create destination path
                dest_path = os.path.join(destination, file_name)
                
                self.log_message_signal.emit(f"Copying {file_name}...")
                
                # Copy file
                self.copy_file(file_path, dest_path)
                
                # Update progress
                self.copy_progress_signal.emit(i + 1, total_files)
            
            self.copy_complete_signal.emit()
        except Exception as e:
            self.log_message_signal.emit(f"Error during import: {e}")
    
    def copy_file(self, source, destination):
        """Copy a file with progress updates."""
        try:
            # Get file size
            file_size = os.path.getsize(source)
            
            # Open source file
            with open(source, 'rb') as src:
                # Open destination file
                with open(destination, 'wb') as dst:
                    copied = 0
                    chunk_size = 1024 * 1024  # 1MB chunks
                    
                    while True:
                        chunk = src.read(chunk_size)
                        if not chunk:
                            break
                        
                        dst.write(chunk)
                        copied += len(chunk)
                        
                        # Update progress occasionally
                        if copied % (10 * chunk_size) == 0:
                            progress = int((copied / file_size) * 100)
                            self.log_message_signal.emit(f"Copying {os.path.basename(source)}: {progress}%")
        except Exception as e:
            self.log_message_signal.emit(f"Error copying file {source}: {e}")
            raise
    
    def update_progress(self, current, total):
        """Update the progress bar."""
        progress = int((current / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(progress)
    
    def on_copy_complete(self):
        """Handle copy completion."""
        self.import_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.log_message("Import completed")
        show_info(self, "Success", "Files imported successfully")
    
    def cancel_import(self):
        """Cancel the import operation."""
        self.is_running = False
        self.cancel_button.setEnabled(False)
        self.log_message("Cancelling import...")
    
    def log_message(self, message):
        """Add a message to the log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def run(self):
        """Run the SD card detection workflow."""
        # Start monitoring
        if not self.is_running:
            self.toggle_monitoring()
    
    def stop(self):
        """Stop the SD card detection workflow."""
        # Stop monitoring
        if self.is_running:
            self.toggle_monitoring()
            
            # Cancel import if in progress
            if self.cancel_button.isEnabled():
                self.cancel_import()
