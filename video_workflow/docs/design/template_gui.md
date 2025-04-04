"""
Modern Dark UI Template with Purple Accents
-------------------------------------------
This template provides a collection of styles and UI components for creating
a modern, dark-themed PyQt6 application with purple accents.

Features:
- Dark theme with purple accents
- Flat, borderless design with rounded corners
- Modern input fields with bottom border highlight
- Gradient-free flat color buttons
- Sleek progress bar
- Organized layout with group boxes

Usage:
1. Import this file in your PyQt6 application
2. Use the style constants for your UI components
3. Follow the example component creation patterns

"""

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QLineEdit, QProgressBar, QMessageBox, QFormLayout, QHBoxLayout, 
    QGroupBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer

# ===== STYLE CONSTANTS =====

# Main window style
WINDOW_STYLE = """
    QWidget {
        background-color: #2D2D30; /* Dark gray background */
        color: #E0E0E0; /* Light gray text */
    }
    QLabel {
        color: #E0E0E0; /* Light gray text */
    }
"""

# Button style
BUTTON_STYLE = """
    QPushButton {
        font-size: 12pt;
        padding: 8px 16px;
        min-width: 120px;
        min-height: 40px;
        background: #6A5ACD; /* Flat color instead of gradient */
        border: none;
        border-radius: 15px; /* Rounded corners */
        color: white;
    }
    QPushButton:hover {
        background: #8A2BE2; /* Flat color on hover */
    }
    QPushButton:pressed {
        background: #9370DB; /* Flat color when pressed */
        padding-top: 9px; /* Subtle movement */
    }
"""

# Success button style (for completed actions)
SUCCESS_BUTTON_STYLE = """
    QPushButton {
        font-size: 12pt;
        padding: 8px 16px;
        min-width: 180px;
        min-height: 40px;
        background-color: #B19CD9; /* Light purple */
        border: none;
        border-radius: 15px; /* Rounded corners */
        color: #FFFFFF;
    }
"""

# Secondary button style
SECONDARY_BUTTON_STYLE = """
    QPushButton {
        font-size: 12pt;
        padding: 8px 16px;
        min-width: 180px;
        min-height: 40px;
        background-color: #9370DB; /* Medium purple */
        border: none;
        border-radius: 15px; /* Rounded corners */
        color: #FFFFFF;
    }
    QPushButton:hover {
        background-color: #8A2BE2; /* Blue violet - darker purple on hover */
    }
"""

# Container style for form fields
CONTAINER_STYLE = """
    QWidget {
        background: #3E3E42; /* Flat dark gray */
        border: none;
        border-radius: 15px; /* Rounded corners */
        padding: 5px 10px;
        margin: 3px 0;
        min-height: 40px;
    }
"""

# Label style for container labels
CONTAINER_LABEL_STYLE = """
    QLabel {
        font-size: 12pt;
        font-weight: bold;
        background-color: transparent;
        border: none;
        padding: 5px;
        color: #E0E0E0; /* Light gray text */
        min-width: 150px; /* Increased width for all labels */
        max-width: 200px; /* Allow more space for longer text */
        qproperty-alignment: 'AlignVCenter'; /* Vertical center alignment */
    }
"""

# File label style
FILE_LABEL_STYLE = """
    QLabel { 
        font-size: 11pt;
        color: #E0E0E0; /* Light gray text */
        padding-left: 5px;
    }
"""

# Input field style
INPUT_STYLE = """
    QLineEdit {
        font-size: 12pt;
        min-height: 30px;
        background-color: #3E3E42; /* Dark gray background */
        border: none;
        border-bottom: 1px solid #6A5ACD; /* Only bottom border for modern look */
        border-radius: 8px; /* Slightly rounded corners for input */
        padding: 2px 5px;
        margin: 0;
        color: #E0E0E0;
    }
    QLineEdit:focus {
        border-bottom: 2px solid #8A2BE2; /* Thicker bottom border when focused */
        background-color: #49494D;
    }
"""

# Header container style
HEADER_STYLE = """
    background: #6A5ACD; /* Flat color instead of gradient */
    border-radius: 15px; /* Rounded corners */
    margin: 5px;
    padding: 5px;
"""

# Header title style
HEADER_TITLE_STYLE = """
    font-size: 20pt; 
    font-weight: bold; 
    color: white;
"""

# Group box style
GROUP_BOX_STYLE = """
    QGroupBox {
        background: #3E3E42; /* Flat dark color */
        border: none;
        border-radius: 15px; /* Rounded corners */
        margin-top: 0.5em;
        padding: 10px;
        color: #E0E0E0;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
        color: #9370DB;
        font-weight: bold;
        font-size: 14pt;
    }
"""

# Progress container style
PROGRESS_CONTAINER_STYLE = """
    background: #3E3E42; /* Flat dark color */
    border: none;
    border-radius: 15px; /* Rounded corners */
    margin: 5px 0;
    padding: 10px;
"""

# Progress label style
PROGRESS_LABEL_STYLE = """
    QLabel {
        font-size: 14pt;
        font-weight: bold;
        color: #9370DB; /* Medium purple */
    }
"""

# Progress bar style
PROGRESS_BAR_STYLE = """
    QProgressBar {
        border: none;
        border-radius: 15px; /* Rounded corners */
        text-align: center;
        background-color: #3E3E42; /* Dark gray to match app background */
        min-height: 35px;
        font-size: 12pt;
        color: #E0E0E0;
        font-weight: bold;
        margin: 0px;
    }
    QProgressBar::chunk {
        background: #6A5ACD; /* Flat color instead of gradient */
        border-radius: 15px; /* Rounded corners */
    }
"""

# ===== COMPONENT CREATION FUNCTIONS =====

def create_header(title):
    """Create a header with the given title"""
    header_container = QWidget()
    header_container.setStyleSheet(HEADER_STYLE)
    header_layout = QHBoxLayout(header_container)
    
    app_title = QLabel(title)
    app_title.setStyleSheet(HEADER_TITLE_STYLE)
    header_layout.addWidget(app_title)
    
    header_layout.addStretch()
    
    return header_container

def create_input_field(label_text, parent=None):
    """Create an input field with label"""
    container = QWidget(parent)
    container.setStyleSheet(CONTAINER_STYLE)
    layout = QHBoxLayout(container)
    layout.setContentsMargins(10, 5, 10, 5)
    
    label = QLabel(label_text)
    label.setStyleSheet(CONTAINER_LABEL_STYLE)
    label.setFixedWidth(150)
    layout.addWidget(label)
    
    input_field = QLineEdit()
    input_field.setStyleSheet(INPUT_STYLE)
    input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    layout.addWidget(input_field, 1)
    
    return container, input_field

def create_file_selector(label_text, parent=None):
    """Create a file selector with browse button"""
    container = QWidget(parent)
    container.setStyleSheet(CONTAINER_STYLE)
    layout = QHBoxLayout(container)
    layout.setContentsMargins(10, 5, 10, 5)
    
    label = QLabel(label_text)
    label.setStyleSheet(CONTAINER_LABEL_STYLE)
    label.setFixedWidth(150)
    layout.addWidget(label)
    
    file_label = QLabel("No file selected")
    file_label.setStyleSheet(FILE_LABEL_STYLE)
    file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    file_label.setWordWrap(True)
    file_label.setMinimumWidth(200)
    layout.addWidget(file_label, 1)
    
    browse_button = QPushButton("Browse...")
    browse_button.setStyleSheet(BUTTON_STYLE)
    browse_button.setFixedWidth(120)
    layout.addWidget(browse_button)
    
    return container, file_label, browse_button

def create_group_box(title):
    """Create a styled group box"""
    group_box = QGroupBox(title)
    group_box.setStyleSheet(GROUP_BOX_STYLE)
    layout = QVBoxLayout(group_box)
    layout.setSpacing(5)
    layout.setContentsMargins(10, 15, 10, 10)
    return group_box

def create_progress_bar(progress_bar=None):
    """Create a progress bar with label"""
    container = QWidget()
    container.setStyleSheet(PROGRESS_CONTAINER_STYLE)
    layout = QVBoxLayout(container)
    
    label = QLabel("Generation Progress")
    label.setStyleSheet(PROGRESS_LABEL_STYLE)
    layout.addWidget(label)
    
    if progress_bar is None:
        progress_bar = QProgressBar()
    
    progress_bar.setStyleSheet(PROGRESS_BAR_STYLE)
    progress_bar.setMinimumHeight(30)
    progress_bar.setMinimumWidth(400)
    layout.addWidget(progress_bar)
    
    return container

def create_button(text):
    """Create a styled button"""
    button = QPushButton(text)
    button.setStyleSheet(BUTTON_STYLE)
    return button

# ===== EXAMPLE USAGE =====

def create_example_window():
    """Create an example window using the template components"""
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Modern Dark UI Template")
    window.setGeometry(200, 200, 650, 500)
    window.setStyleSheet(WINDOW_STYLE)
    
    layout = QVBoxLayout(window)
    layout.setSpacing(5)
    layout.setContentsMargins(10, 10, 10, 10)
    
    # Add header
    header = create_header("Example Application")
    layout.addWidget(header)
    
    # Create file selection group
    file_group = create_group_box("File Selection")
    file_layout = QVBoxLayout(file_group)
    
    # Add file selectors
    input_file_container, input_file_label, input_file_button = create_file_selector("Input File:")
    file_layout.addWidget(input_file_container)
    
    output_file_container, output_file_label, output_file_button = create_file_selector("Output File:")
    file_layout.addWidget(output_file_container)
    
    layout.addWidget(file_group)
    
    # Create settings group
    settings_group = create_group_box("Settings")
    settings_layout = QVBoxLayout(settings_group)
    
    # Add input fields
    name_container, name_input = create_input_field("Name:")
    settings_layout.addWidget(name_container)
    
    email_container, email_input = create_input_field("Email:")
    settings_layout.addWidget(email_container)
    
    layout.addWidget(settings_group)
    
    # Add progress bar
    progress_container = create_progress_bar()
    layout.addWidget(progress_container)
    
    # Add buttons
    button_layout = QHBoxLayout()
    button_layout.addStretch()
    
    process_button = create_button("Process")
    button_layout.addWidget(process_button)
    
    cancel_button = create_button("Cancel")
    button_layout.addWidget(cancel_button)
    
    button_layout.addStretch()
    layout.addLayout(button_layout)
    
    window.show()
    return app, window

if __name__ == "__main__":
    app, window = create_example_window()
    app.exec()