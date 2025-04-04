"""
Modern Dark UI Template with Purple Accents for Video Workflow
------------------------------------------------------------
This module provides UI components and styles for the video workflow application.
"""

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QLineEdit, QProgressBar, QMessageBox, QFormLayout, QHBoxLayout, 
    QGroupBox, QSizePolicy, QTabWidget, QListWidget, QTextEdit, QCheckBox,
    QComboBox, QSpinBox, QDoubleSpinBox, QFrame, QScrollArea, QMainWindow,
    QStatusBar, QToolBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont, QPixmap, QAction

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
    
    /* Tab Widget Styling */
    QTabWidget::pane {
        border: 1px solid #3D3D40;
        background-color: #2D2D30;
        border-radius: 3px;
    }
    
    QTabBar::tab {
        background-color: #6A5ACD; /* Purple for unselected tabs */
        color: white;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: #2D2D30; /* Dark gray for selected tab */
        border-bottom: 2px solid #8A2BE2; /* Purple indicator line for selected tab */
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #8A2BE2; /* Brighter purple on hover */
    }
    
    /* Modern Scrollbar Styling */
    QScrollBar:vertical {
        border: none;
        background: #3D3D40;
        width: 10px;
        margin: 0px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background: #6A5ACD;
        min-height: 30px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: #8A2BE2;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
    
    /* Horizontal Scrollbar */
    QScrollBar:horizontal {
        border: none;
        background: #3D3D40;
        height: 10px;
        margin: 0px;
        border-radius: 5px;
    }
    QScrollBar::handle:horizontal {
        background: #6A5ACD;
        min-width: 30px;
        border-radius: 5px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #8A2BE2;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
"""

# Button style
BUTTON_STYLE = """
    QPushButton {
        font-size: 11pt;
        padding: 6px 12px;
        min-width: 120px;
        min-height: 30px;
        background: #6A5ACD; /* Flat color instead of gradient */
        border: none;
        border-radius: 8px; /* Rounded corners */
        color: white;
        margin: 5px;
    }
    QPushButton:hover {
        background: #8A2BE2; /* Flat color on hover */
    }
    QPushButton:pressed {
        background: #9370DB; /* Flat color when pressed */
        padding-top: 7px; /* Subtle movement */
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
        font-size: 11pt;
        padding: 6px 12px;
        min-width: 120px;
        min-height: 30px;
        background-color: #9370DB; /* Medium purple */
        border: none;
        border-radius: 8px; /* Rounded corners */
        color: #FFFFFF;
        margin: 5px;
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
    }
"""

# Header style
HEADER_CONTAINER_STYLE = """
    background-color: #3E3E42; /* Dark gray background */
    border-radius: 15px; /* Rounded corners */
    margin-bottom: 10px;
    padding: 10px;
"""

# Header title style
HEADER_TITLE_STYLE = """
    font-size: 18pt;
    font-weight: bold;
    color: #9370DB; /* Medium purple */
"""

# Group box style
GROUP_BOX_STYLE = """
    QGroupBox {
        font-size: 14pt;
        font-weight: bold;
        border: 1px solid #6A5ACD; /* Purple border */
        border-radius: 15px; /* Rounded corners */
        margin-top: 20px;
        padding-top: 15px;
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
        font-size: 12pt;
        color: #9370DB; /* Medium purple */
        margin-bottom: 5px;
    }
"""

# Progress bar style
PROGRESS_BAR_STYLE = """
    QProgressBar {
        border: none;
        border-radius: 10px;
        background-color: #444444;
        text-align: center;
        color: white;
        font-weight: bold;
    }
    QProgressBar::chunk {
        background-color: #6A5ACD; /* Flat purple */
        border-radius: 10px;
    }
"""

# Tab widget style
TAB_STYLE = """
    QTabWidget::pane {
        border: 1px solid #6A5ACD;
        border-radius: 5px;
        background-color: #2D2D30;
    }
    QTabBar::tab {
        background-color: #3E3E42;
        color: #E0E0E0;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        padding: 8px 16px;
        min-width: 100px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background-color: #6A5ACD;
        color: white;
    }
    QTabBar::tab:hover:!selected {
        background-color: #4E4E52;
    }
"""

# List widget style
LIST_STYLE = """
    QListWidget {
        background-color: #3E3E42;
        border: none;
        border-radius: 10px;
        padding: 5px;
        color: #E0E0E0;
    }
    QListWidget::item {
        padding: 5px;
        border-radius: 5px;
    }
    QListWidget::item:selected {
        background-color: #6A5ACD;
        color: white;
    }
    QListWidget::item:hover:!selected {
        background-color: #4E4E52;
    }
"""

# Text edit style
TEXT_EDIT_STYLE = """
    QTextEdit {
        background-color: #3E3E42;
        border: none;
        border-radius: 10px;
        padding: 5px;
        color: #E0E0E0;
        font-size: 11pt;
    }
"""

# Combo box style
COMBO_BOX_STYLE = """
    QComboBox {
        background-color: #3E3E42;
        border: none;
        border-bottom: 1px solid #6A5ACD;
        border-radius: 8px;
        padding: 5px;
        min-height: 30px;
        color: #E0E0E0;
        font-size: 12pt;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border: none;
    }
    QComboBox QAbstractItemView {
        background-color: #3E3E42;
        border: 1px solid #6A5ACD;
        border-radius: 5px;
        selection-background-color: #6A5ACD;
        color: #E0E0E0;
    }
"""

# Checkbox style
CHECKBOX_STYLE = """
    QCheckBox {
        color: #E0E0E0;
        font-size: 12pt;
        spacing: 10px;
    }
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 5px;
    }
    QCheckBox::indicator:unchecked {
        background-color: #3E3E42;
        border: 1px solid #6A5ACD;
    }
    QCheckBox::indicator:checked {
        background-color: #6A5ACD;
        border: 1px solid #6A5ACD;
    }
"""

# Status bar style
STATUS_BAR_STYLE = """
    QStatusBar {
        background-color: #3E3E42;
        color: #E0E0E0;
        border-top: 1px solid #6A5ACD;
    }
"""

# ===== UI COMPONENT FUNCTIONS =====

def create_header(title):
    """Create a header with title"""
    header_container = QWidget()
    header_container.setStyleSheet(HEADER_CONTAINER_STYLE)
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
    
    # Use horizontal layout for better space usage
    layout = QHBoxLayout(container)
    layout.setContentsMargins(10, 5, 10, 5)
    layout.setSpacing(10)
    
    # Container label
    label = QLabel(label_text)
    label.setStyleSheet(CONTAINER_LABEL_STYLE)
    label.setMinimumWidth(100)
    label.setMaximumWidth(150)
    layout.addWidget(label)
    
    # File label
    file_label = QLabel("No file selected")
    file_label.setStyleSheet(FILE_LABEL_STYLE)
    file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    file_label.setWordWrap(True)
    file_label.setMinimumWidth(200)
    layout.addWidget(file_label, 1)
    
    # Browse button
    browse_button = QPushButton("Browse...")
    browse_button.setStyleSheet(BUTTON_STYLE)
    browse_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    layout.addWidget(browse_button)
    
    return container, file_label, browse_button

def create_directory_selector(label_text, parent=None):
    """Create a directory selector with browse button"""
    container = QWidget(parent)
    container.setStyleSheet(CONTAINER_STYLE)
    
    # Use horizontal layout for better space usage
    layout = QHBoxLayout(container)
    layout.setContentsMargins(10, 5, 10, 5)
    layout.setSpacing(10)
    
    # Container label
    label = QLabel(label_text)
    label.setStyleSheet(CONTAINER_LABEL_STYLE)
    label.setMinimumWidth(100)
    label.setMaximumWidth(150)
    layout.addWidget(label)
    
    # Directory label
    dir_label = QLabel("No directory selected")
    dir_label.setStyleSheet(FILE_LABEL_STYLE)
    dir_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    dir_label.setWordWrap(True)
    dir_label.setMinimumWidth(200)
    layout.addWidget(dir_label, 1)
    
    # Browse button
    browse_button = QPushButton("Browse...")
    browse_button.setStyleSheet(BUTTON_STYLE)
    browse_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    layout.addWidget(browse_button)
    
    return container, dir_label, browse_button

def create_group_box(title):
    """Create a styled group box"""
    group_box = QGroupBox(title)
    group_box.setStyleSheet(GROUP_BOX_STYLE)
    layout = QVBoxLayout(group_box)
    layout.setSpacing(5)
    layout.setContentsMargins(10, 15, 10, 10)
    return group_box, layout

def create_progress_bar(label_text="Progress"):
    """Create a progress bar with label"""
    container = QWidget()
    container.setStyleSheet(PROGRESS_CONTAINER_STYLE)
    layout = QVBoxLayout(container)
    
    label = QLabel(label_text)
    label.setStyleSheet(PROGRESS_LABEL_STYLE)
    layout.addWidget(label)
    
    progress_bar = QProgressBar()
    progress_bar.setStyleSheet(PROGRESS_BAR_STYLE)
    progress_bar.setMinimumHeight(30)
    progress_bar.setMinimumWidth(400)
    layout.addWidget(progress_bar)
    
    return container, progress_bar

def create_button(text, primary=True):
    """Create a styled button"""
    button = QPushButton(text)
    button.setStyleSheet(BUTTON_STYLE if primary else SECONDARY_BUTTON_STYLE)
    
    # Set reasonable size constraints
    button.setMinimumWidth(120)
    button.setMinimumHeight(30)
    button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    
    return button

def create_success_button(text):
    """Create a success-styled button"""
    button = QPushButton(text)
    button.setStyleSheet(SUCCESS_BUTTON_STYLE)
    return button

def create_checkbox(text, parent=None):
    """Create a styled checkbox"""
    checkbox = QCheckBox(text, parent)
    checkbox.setStyleSheet(CHECKBOX_STYLE)
    return checkbox

def create_combo_box(items=None, parent=None):
    """Create a styled combo box"""
    combo = QComboBox(parent)
    combo.setStyleSheet(COMBO_BOX_STYLE)
    
    if items:
        combo.addItems(items)
    
    return combo

def create_tab_widget(parent=None):
    """Create a styled tab widget"""
    tab_widget = QTabWidget(parent)
    tab_widget.setStyleSheet(TAB_STYLE)
    return tab_widget

def create_list_widget(parent=None):
    """Create a styled list widget"""
    list_widget = QListWidget(parent)
    list_widget.setStyleSheet(LIST_STYLE)
    return list_widget

def create_text_edit(parent=None):
    """Create a styled text edit for logs or output"""
    text_edit = QTextEdit(parent)
    text_edit.setStyleSheet(TEXT_EDIT_STYLE)
    text_edit.setReadOnly(True)
    return text_edit

def create_horizontal_separator():
    """Create a horizontal separator line"""
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    line.setStyleSheet("background-color: #6A5ACD;")
    line.setFixedHeight(1)
    return line

def create_status_bar(parent):
    """Create a styled status bar"""
    status_bar = QStatusBar(parent)
    status_bar.setStyleSheet(STATUS_BAR_STYLE)
    return status_bar

def show_message(parent, title, message, icon=QMessageBox.Icon.Information):
    """Show a styled message box"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)
    msg_box.setStyleSheet(WINDOW_STYLE)
    return msg_box.exec()

def show_error(parent, title, message):
    """Show an error message box"""
    return show_message(parent, title, message, QMessageBox.Icon.Critical)

def show_warning(parent, title, message):
    """Show a warning message box"""
    return show_message(parent, title, message, QMessageBox.Icon.Warning)

def show_info(parent, title, message):
    """Show an info message box"""
    return show_message(parent, title, message, QMessageBox.Icon.Information)

def show_question(parent, title, message):
    """Show a question message box"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setStyleSheet(WINDOW_STYLE)
    return msg_box.exec() == QMessageBox.StandardButton.Yes
