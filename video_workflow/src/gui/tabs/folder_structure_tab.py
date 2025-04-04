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
    QScrollArea, QFrame, QCheckBox, QPushButton, QRadioButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont

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
        
        # Project settings group with improved description
        self.project_group, self.project_layout = create_group_box("Project Settings")
        
        # Add description of folder structure
        structure_info = QLabel("Your project will be organized as: Base Directory / Date / Project Name / Folders")
        structure_info.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
            margin-bottom: 10px;
            padding: 5px;
            background-color: #444444;
            border-radius: 5px;
        """)
        self.project_layout.addWidget(structure_info)
        
        # Project name input with better description
        self.project_name_container, self.project_name_input = create_input_field("Project Name:")
        self.project_name_input.setPlaceholderText("Enter project name (e.g. Client_ProjectTitle)")
        self.project_layout.addWidget(self.project_name_container)
        
        # Base directory selector with better description
        self.base_dir_container, self.base_dir_label, self.base_dir_button = create_directory_selector("Base Directory:")
        base_dir_info = QLabel("Select the root folder where all projects are stored")
        base_dir_info.setStyleSheet("color: #AAAAAA; margin-left: 160px; font-size: 10pt;")
        self.project_layout.addWidget(self.base_dir_container)
        self.project_layout.addWidget(base_dir_info)
        
        # DaVinci template is always enabled if available
        self.use_davinci_template = True  # Always try to use template if available
        
        # Date selection with improved description
        self.date_group, self.date_layout = create_group_box("Project Date")
        
        # Add date explanation
        date_info = QLabel("The project will be created in a folder with the selected date")
        date_info.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
            margin-bottom: 10px;
        """)
        self.date_layout.addWidget(date_info)
        
        # Current date display
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_date_container = QWidget()
        current_date_layout = QHBoxLayout(current_date_container)
        current_date_layout.setContentsMargins(5, 5, 5, 5)
        
        current_date_label = QLabel("Today's date:")
        current_date_label.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
            font-weight: bold;
        """)
        
        current_date_value = QLabel(current_date)
        current_date_value.setStyleSheet("""
            font-size: 11pt;
            color: #FFFFFF;
            background-color: #555555;
            padding: 3px 8px;
            border-radius: 4px;
        """)
        
        current_date_layout.addWidget(current_date_label)
        current_date_layout.addWidget(current_date_value)
        current_date_layout.addStretch()
        
        self.date_layout.addWidget(current_date_container)
        
        # Use current date checkbox with better styling
        date_options_container = QWidget()
        date_options_layout = QVBoxLayout(date_options_container)
        date_options_layout.setContentsMargins(5, 10, 5, 5)
        date_options_layout.setSpacing(10)
        
        self.use_current_date_checkbox = create_checkbox("Use today's date (recommended)")
        self.use_current_date_checkbox.setChecked(True)
        self.use_current_date_checkbox.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
        """)
        date_options_layout.addWidget(self.use_current_date_checkbox)
        
        # Custom date option
        custom_date_label = QLabel("Or select a custom date:")
        custom_date_label.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
            margin-top: 5px;
        """)
        date_options_layout.addWidget(custom_date_label)
        
        self.date_layout.addWidget(date_options_container)
        
        # Calendar widget with improved styling
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar_widget.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)
        self.calendar_widget.setStyleSheet("""
            QCalendarWidget {
                background-color: #3E3E42;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 5px;
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
            QCalendarWidget QToolButton:hover {
                background-color: #555555;
                border-radius: 4px;
            }
        """)
        self.calendar_widget.setCurrentPage(QDate.currentDate().year(), QDate.currentDate().month())
        self.calendar_widget.setSelectedDate(QDate.currentDate())
        self.date_layout.addWidget(self.calendar_widget)
        self.calendar_widget.setVisible(False)
        
        # Selected date display (initially hidden)
        self.selected_date_container = QWidget()
        selected_date_layout = QHBoxLayout(self.selected_date_container)
        selected_date_layout.setContentsMargins(5, 5, 5, 5)
        
        selected_date_label = QLabel("Selected date:")
        selected_date_label.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
            font-weight: bold;
        """)
        
        self.selected_date_value = QLabel(current_date)
        self.selected_date_value.setStyleSheet("""
            font-size: 11pt;
            color: #FFFFFF;
            background-color: #6A5ACD;
            padding: 3px 8px;
            border-radius: 4px;
        """)
        
        selected_date_layout.addWidget(selected_date_label)
        selected_date_layout.addWidget(self.selected_date_value)
        selected_date_layout.addStretch()
        
        self.date_layout.addWidget(self.selected_date_container)
        self.selected_date_container.setVisible(False)
        
        # Add date group to project layout
        self.project_layout.addWidget(self.date_group)
        
        # Add project group to content layout
        content_layout.addWidget(self.project_group)
        
        # Folder structure group with improved description
        self.structure_group, self.structure_layout = create_group_box("Folder Structure")
        
        # Add description label
        folder_description = QLabel("Select folders to create in your project directory:")
        folder_description.setStyleSheet("""
            font-size: 11pt;
            color: #E0E0E0;
            margin-bottom: 10px;
        """)
        self.structure_layout.addWidget(folder_description)
        
        # Create container for checkboxes with better visual organization
        checkbox_container = QWidget()
        checkbox_layout = QVBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(10, 5, 10, 5)
        checkbox_layout.setSpacing(10)
        
        # Checkboxes for folders to create with descriptions
        self.footage_checkbox = create_checkbox("footage/")
        self.footage_checkbox.setChecked(True)
        footage_description = QLabel("Raw camera footage files")
        footage_description.setStyleSheet("color: #AAAAAA; margin-left: 25px; font-size: 10pt;")
        checkbox_layout.addWidget(self.footage_checkbox)
        checkbox_layout.addWidget(footage_description)
        
        self.proxies_checkbox = create_checkbox("proxies/")
        self.proxies_checkbox.setChecked(True)
        proxies_description = QLabel("Lower resolution proxy files for editing")
        proxies_description.setStyleSheet("color: #AAAAAA; margin-left: 25px; font-size: 10pt;")
        checkbox_layout.addWidget(self.proxies_checkbox)
        checkbox_layout.addWidget(proxies_description)
        
        self.exports_checkbox = create_checkbox("exports/")
        self.exports_checkbox.setChecked(True)
        exports_description = QLabel("Final rendered video files")
        exports_description.setStyleSheet("color: #AAAAAA; margin-left: 25px; font-size: 10pt;")
        checkbox_layout.addWidget(self.exports_checkbox)
        checkbox_layout.addWidget(exports_description)
        
        self.logs_checkbox = create_checkbox("logs/")
        self.logs_checkbox.setChecked(True)
        logs_description = QLabel("Processing and error logs")
        logs_description.setStyleSheet("color: #AAAAAA; margin-left: 25px; font-size: 10pt;")
        checkbox_layout.addWidget(self.logs_checkbox)
        checkbox_layout.addWidget(logs_description)
        
        # Template option moved to project settings section
        
        # Add the checkbox container to the structure layout
        self.structure_layout.addWidget(checkbox_container)
        
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
        
        # Connect checkbox and calendar
        self.use_current_date_checkbox.stateChanged.connect(self.toggle_calendar)
        self.calendar_widget.selectionChanged.connect(self.on_date_selected)
        
        # DaVinci button is already connected in init_ui
        
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
        use_current_date = (state == Qt.CheckState.Checked)
        self.calendar_widget.setVisible(not use_current_date)
        self.selected_date_container.setVisible(not use_current_date)
        
    def on_date_selected(self):
        """Update the selected date display when a date is selected in the calendar."""
        selected_date = self.calendar_widget.selectedDate().toString("yyyy-MM-dd")
        self.selected_date_value.setText(selected_date)
        
    # Template handling is now automatic
    
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
                
                # Set DaVinci template option based on config
                davinci_template_path = config.get('davinci_template_path', '')
                # Template will be used automatically if available
                self.use_davinci_template = bool(davinci_template_path)
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
            
            # Get date - use current date or custom selected date
            if self.use_current_date_checkbox.isChecked():
                date_str = datetime.now().strftime("%Y-%m-%d")
                self.log_message(f"Using today's date: {date_str}")
            else:
                selected_date = self.calendar_widget.selectedDate()
                date_str = f"{selected_date.year()}-{selected_date.month():02d}-{selected_date.day():02d}"
                self.log_message(f"Using custom date: {date_str}")
            
            # Get folders to create
            folders = []
            folder_names = []
            
            if self.footage_checkbox.isChecked():
                folders.append("footage")
                folder_names.append("footage/")
                
            if self.proxies_checkbox.isChecked():
                folders.append("proxies")
                folder_names.append("proxies/")
                
            if self.exports_checkbox.isChecked():
                folders.append("exports")
                folder_names.append("exports/")
                
            if self.logs_checkbox.isChecked():
                folders.append("logs")
                folder_names.append("logs/")
            
            if not folders:
                show_error(self, "Error", "Please select at least one folder to create")
                return
                
            # Log the folders that will be created
            self.log_message(f"Will create folders: {', '.join(folder_names)}")
            
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
            
            # Copy DaVinci template if enabled
            if self.use_davinci_template:
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
