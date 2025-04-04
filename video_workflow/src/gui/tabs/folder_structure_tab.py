"""
Folder Structure Generator Tab for the Video Workflow Application
"""

import os
import sys
import json
import threading
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCalendarWidget, QFileDialog, QSizePolicy,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate

# Import UI template components
from ..ui_template import (
    create_group_box, create_button, create_directory_selector,
    create_checkbox, show_info, show_error, create_text_edit,
    create_horizontal_separator, create_input_field
)

class FolderStructureTab(QWidget):
    """Folder structure generator tab for creating project directories."""
    
    # Signals for thread-safe UI updates
    log_message_signal = pyqtSignal(str)
    structure_created_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Initialize properties
        self.is_running = False
        self.structure_thread = None
        
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
        
        # Project settings group
        self.project_group, self.project_layout = create_group_box("Project Settings")
        
        # Project name input
        self.project_name_container, self.project_name_input = create_input_field("Project Name:")
        self.project_name_input.setPlaceholderText("Enter project name")
        self.project_layout.addWidget(self.project_name_container)
        
        # Base directory selector
        self.base_dir_container, self.base_dir_label, self.base_dir_button = create_directory_selector("Base Directory:")
        self.project_layout.addWidget(self.base_dir_container)
        
        # Date selection
        self.date_group, self.date_layout = create_group_box("Project Date")
        
        # Use current date checkbox
        self.use_current_date_checkbox = create_checkbox("Use current date")
        self.use_current_date_checkbox.setChecked(True)
        self.date_layout.addWidget(self.use_current_date_checkbox)
        
        # Calendar widget (initially hidden)
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar_widget.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)
        self.calendar_widget.setStyleSheet("""
            QCalendarWidget {
                background-color: #3E3E42;
                color: #E0E0E0;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #2D2D30;
                selection-background-color: #6A5ACD;
                selection-color: white;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #3E3E42;
            }
            QCalendarWidget QToolButton {
                color: #E0E0E0;
                background-color: #3E3E42;
            }
        """)
        self.calendar_widget.setCurrentPage(QDate.currentDate().year(), QDate.currentDate().month())
        self.calendar_widget.setSelectedDate(QDate.currentDate())
        self.date_layout.addWidget(self.calendar_widget)
        self.calendar_widget.setVisible(False)
        
        # Add date group to project layout
        self.project_layout.addWidget(self.date_group)
        
        # Add project group to content layout
        content_layout.addWidget(self.project_group)
        
        # Folder structure group
        self.structure_group, self.structure_layout = create_group_box("Folder Structure")
        
        # Checkboxes for folders to create
        self.footage_checkbox = create_checkbox("footage/")
        self.footage_checkbox.setChecked(True)
        self.structure_layout.addWidget(self.footage_checkbox)
        
        self.proxies_checkbox = create_checkbox("proxies/")
        self.proxies_checkbox.setChecked(True)
        self.structure_layout.addWidget(self.proxies_checkbox)
        
        self.exports_checkbox = create_checkbox("exports/")
        self.exports_checkbox.setChecked(True)
        self.structure_layout.addWidget(self.exports_checkbox)
        
        self.logs_checkbox = create_checkbox("logs/")
        self.logs_checkbox.setChecked(True)
        self.structure_layout.addWidget(self.logs_checkbox)
        
        # DaVinci template checkbox
        self.davinci_checkbox = create_checkbox("Copy DaVinci template")
        self.structure_layout.addWidget(self.davinci_checkbox)
        
        # Add structure group to content layout
        content_layout.addWidget(self.structure_group)
        
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
        
        self.create_button = create_button("Create Folder Structure")
        self.button_layout.addWidget(self.create_button)
        
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
        self.base_dir_button.clicked.connect(lambda: self.browse_directory(self.base_dir_label, "Select Base Directory"))
        self.create_button.clicked.connect(self.create_folder_structure)
        self.cancel_button.clicked.connect(self.cancel_creation)
        
        # Connect checkbox
        self.use_current_date_checkbox.stateChanged.connect(self.toggle_calendar)
        
        # Connect thread signals
        self.log_message_signal.connect(self.log_message)
        self.structure_created_signal.connect(self.on_structure_created)
    
    def browse_directory(self, label, caption):
        """Open directory browser dialog."""
        directory = QFileDialog.getExistingDirectory(self, caption)
        if directory:
            label.setText(directory)
    
    def toggle_calendar(self, state):
        """Show or hide calendar based on checkbox state."""
        self.calendar_widget.setVisible(state != Qt.CheckState.Checked)
    
    def load_config(self):
        """Load configuration from file."""
        try:
            # Get the config file path
            script_dir = Path(__file__).resolve().parent.parent.parent.parent
            config_path = script_dir / 'config' / 'config.json'
            
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Set base directory from raw_path
                raw_path = config.get('raw_path', '')
                if raw_path:
                    self.base_dir_label.setText(raw_path)
                
                # Set DaVinci template checkbox based on config
                davinci_template_path = config.get('davinci_template_path', '')
                self.davinci_checkbox.setChecked(bool(davinci_template_path))
                self.davinci_checkbox.setEnabled(bool(davinci_template_path))
        except Exception as e:
            self.log_message(f"Failed to load configuration: {e}")
    
    def create_folder_structure(self):
        """Create the folder structure."""
        try:
            # Validate inputs
            project_name = self.project_name_input.text().strip()
            if not project_name:
                show_error(self, "Error", "Please enter a project name")
                return
            
            base_dir = self.base_dir_label.text()
            if base_dir == "No directory selected" or not os.path.isdir(base_dir):
                show_error(self, "Error", "Please select a valid base directory")
                return
            
            # Get date
            if self.use_current_date_checkbox.isChecked():
                date_str = datetime.now().strftime("%Y-%m-%d")
            else:
                selected_date = self.calendar_widget.selectedDate()
                date_str = f"{selected_date.year()}-{selected_date.month():02d}-{selected_date.day():02d}"
            
            # Get folders to create
            folders = []
            if self.footage_checkbox.isChecked():
                folders.append("footage")
            if self.proxies_checkbox.isChecked():
                folders.append("proxies")
            if self.exports_checkbox.isChecked():
                folders.append("exports")
            if self.logs_checkbox.isChecked():
                folders.append("logs")
            
            if not folders:
                show_error(self, "Error", "Please select at least one folder to create")
                return
            
            # Update UI
            self.create_button.setEnabled(False)
            self.cancel_button.setEnabled(True)
            
            # Start structure creation thread
            self.is_running = True
            self.structure_thread = threading.Thread(
                target=self.create_structure,
                args=(base_dir, date_str, project_name, folders),
                daemon=True
            )
            self.structure_thread.start()
            
            self.log_message(f"Creating folder structure for project '{project_name}' in {base_dir}/{date_str}")
        except Exception as e:
            self.log_message(f"Error starting folder creation: {e}")
            show_error(self, "Error", f"Failed to start folder creation: {e}")
    
    def create_structure(self, base_dir, date_str, project_name, folders):
        """Create the folder structure in a separate thread."""
        try:
            # Create project directory
            project_dir = os.path.join(base_dir, date_str, project_name)
            os.makedirs(project_dir, exist_ok=True)
            self.log_message_signal.emit(f"Created project directory: {project_dir}")
            
            # Create subfolders
            for folder in folders:
                if not self.is_running:
                    self.log_message_signal.emit("Folder creation cancelled")
                    return
                
                folder_path = os.path.join(project_dir, folder)
                os.makedirs(folder_path, exist_ok=True)
                self.log_message_signal.emit(f"Created folder: {folder_path}")
            
            # Copy DaVinci template if selected
            if self.davinci_checkbox.isChecked():
                try:
                    # Get template path from config
                    script_dir = Path(__file__).resolve().parent.parent.parent.parent
                    config_path = script_dir / 'config' / 'config.json'
                    
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    
                    template_path = config.get('davinci_template_path', '')
                    
                    if template_path and Path(template_path).is_file():
                        import shutil
                        # Use Path objects for cross-platform compatibility
                        template_file = Path(template_path)
                        dest_path = Path(project_dir) / template_file.name
                        shutil.copy2(template_file, dest_path)
                        self.log_message_signal.emit(f"Copied DaVinci template to: {dest_path}")
                    else:
                        self.log_message_signal.emit("DaVinci template not found or not configured")
                except Exception as e:
                    self.log_message_signal.emit(f"Error copying DaVinci template: {e}")
            
            # Signal completion
            self.structure_created_signal.emit()
        except Exception as e:
            self.log_message_signal.emit(f"Error creating folder structure: {e}")
    
    def cancel_creation(self):
        """Cancel the folder structure creation."""
        self.is_running = False
        self.cancel_button.setEnabled(False)
        self.log_message("Cancelling folder creation...")
    
    def on_structure_created(self):
        """Handle structure creation completion."""
        self.create_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.log_message("Folder structure created successfully")
        show_info(self, "Success", "Folder structure created successfully")
    
    def log_message(self, message):
        """Add a message to the log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def run(self):
        """Run the folder structure creation workflow."""
        self.create_folder_structure()
    
    def stop(self):
        """Stop the folder structure creation workflow."""
        if self.is_running:
            self.cancel_creation()
