"""
Log Viewer Tab for the Video Workflow Application
"""

import os
import sys
import threading
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QFileDialog, QSplitter, QSizePolicy, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

# Import UI template components
from ..ui_template import (
    create_group_box, create_button, create_directory_selector,
    create_combo_box, create_text_edit, create_horizontal_separator
)

class LogViewerTab(QWidget):
    """Log viewer tab for viewing application logs."""
    
    # Signals for thread-safe UI updates
    log_content_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize properties
        self.log_files = []
        self.current_log = None
        self.auto_refresh = False
        self.refresh_timer = None
        
        # Initialize UI
        self.init_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Find log files
        self.find_log_files()
    
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
        
        # Log selection group
        self.selection_group, self.selection_layout = create_group_box("Log Selection")
        
        # Log directory selector
        self.log_dir_container, self.log_dir_label, self.log_dir_button = create_directory_selector("Log Directory:")
        self.selection_layout.addWidget(self.log_dir_container)
        
        # Log file selector
        log_file_container = QWidget()
        log_file_layout = QHBoxLayout(log_file_container)
        log_file_layout.setContentsMargins(10, 5, 10, 5)
        
        log_file_label = QLabel("Log File:")
        log_file_label.setStyleSheet("""
            font-size: 12pt;
            font-weight: bold;
            background-color: transparent;
            border: none;
            padding: 5px;
            color: #E0E0E0;
            min-width: 150px;
            max-width: 200px;
        """)
        log_file_label.setFixedWidth(150)
        log_file_layout.addWidget(log_file_label)
        
        self.log_file_combo = create_combo_box()
        log_file_layout.addWidget(self.log_file_combo)
        
        self.selection_layout.addWidget(log_file_container)
        
        # Add selection group to content layout
        content_layout.addWidget(self.selection_group)
        
        # Log content group
        self.content_group, self.content_layout = create_group_box("Log Content")
        
        # Log text area
        self.log_text = create_text_edit()
        self.content_layout.addWidget(self.log_text)
        
        # Add content group to content layout
        content_layout.addWidget(self.content_group)
        
        # Add separator
        content_layout.addWidget(create_horizontal_separator())
        
        # Add buttons container
        button_container = QWidget()
        self.button_layout = QHBoxLayout(button_container)
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.addStretch(1)
        
        self.refresh_button = create_button("Refresh")
        self.button_layout.addWidget(self.refresh_button)
        
        self.auto_refresh_button = create_button("Auto Refresh: Off", primary=False)
        self.button_layout.addWidget(self.auto_refresh_button)
        
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
        self.log_dir_button.clicked.connect(lambda: self.browse_directory(self.log_dir_label, "Select Log Directory"))
        self.refresh_button.clicked.connect(self.refresh_log)
        self.auto_refresh_button.clicked.connect(self.toggle_auto_refresh)
        
        # Connect combo box
        self.log_file_combo.currentIndexChanged.connect(self.on_log_file_changed)
        
        # Connect thread signals
        self.log_content_signal.connect(self.update_log_content)
    
    def browse_directory(self, label, caption):
        """Open directory browser dialog."""
        directory = QFileDialog.getExistingDirectory(self, caption)
        if directory:
            label.setText(directory)
            self.find_log_files()
    
    def find_log_files(self):
        """Find log files in the log directory."""
        try:
            log_dir = self.log_dir_label.text()
            if log_dir == "No directory selected" or not os.path.isdir(log_dir):
                # Try to find default log directory
                script_dir = Path(__file__).resolve().parent.parent.parent.parent
                default_log_dir = script_dir / 'logs'
                
                if default_log_dir.exists():
                    log_dir = str(default_log_dir)
                    self.log_dir_label.setText(log_dir)
                else:
                    return
            
            # Clear combo box
            self.log_file_combo.clear()
            self.log_files = []
            
            # Find log files
            for file in os.listdir(log_dir):
                if file.endswith('.log'):
                    self.log_files.append(os.path.join(log_dir, file))
                    self.log_file_combo.addItem(file)
            
            # Select first log file if available
            if self.log_files:
                self.log_file_combo.setCurrentIndex(0)
                self.on_log_file_changed(0)
        except Exception as e:
            self.log_text.setText(f"Error finding log files: {e}")
    
    def on_log_file_changed(self, index):
        """Handle log file selection change."""
        if index >= 0 and index < len(self.log_files):
            self.current_log = self.log_files[index]
            self.refresh_log()
    
    def refresh_log(self):
        """Refresh the log content."""
        if self.current_log and os.path.isfile(self.current_log):
            # Start thread to read log file
            threading.Thread(
                target=self.read_log_file,
                args=(self.current_log,),
                daemon=True
            ).start()
    
    def read_log_file(self, log_file):
        """Read log file in a separate thread."""
        try:
            with open(log_file, 'r') as f:
                content = f.read()
            
            self.log_content_signal.emit(content)
        except Exception as e:
            self.log_content_signal.emit(f"Error reading log file: {e}")
    
    def update_log_content(self, content):
        """Update the log content in the UI."""
        self.log_text.setText(content)
        
        # Scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def toggle_auto_refresh(self):
        """Toggle auto refresh of log content."""
        self.auto_refresh = not self.auto_refresh
        
        if self.auto_refresh:
            self.auto_refresh_button.setText("Auto Refresh: On")
            
            # Start refresh timer
            if not self.refresh_timer:
                self.refresh_timer = QTimer(self)
                self.refresh_timer.timeout.connect(self.refresh_log)
            
            self.refresh_timer.start(2000)  # Refresh every 2 seconds
        else:
            self.auto_refresh_button.setText("Auto Refresh: Off")
            
            # Stop refresh timer
            if self.refresh_timer:
                self.refresh_timer.stop()
    
    def run(self):
        """Run the log viewer workflow."""
        # Just refresh the log
        self.refresh_log()
    
    def stop(self):
        """Stop the log viewer workflow."""
        # Stop auto refresh if enabled
        if self.auto_refresh:
            self.toggle_auto_refresh()
