"""
Main Window for the Video Workflow Application
"""

import os
import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QStatusBar, QLabel, QPushButton, QMessageBox,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QIcon

# Add parent directory to path to enable imports
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import UI template components
from gui.ui_template import (
    WINDOW_STYLE, create_header, create_status_bar, show_info, 
    show_error, show_question, create_button
)

# Import tab screens for each workflow phase
from gui.tabs.config_tab import ConfigTab
from gui.tabs.sd_detection_tab import SDDetectionTab
from gui.tabs.folder_structure_tab import FolderStructureTab
from gui.tabs.proxy_generator_tab import ProxyGeneratorTab
from gui.tabs.export_watcher_tab import ExportWatcherTab
from gui.tabs.upload_tab import UploadTab
from gui.tabs.log_viewer_tab import LogViewerTab

class MainWindow(QMainWindow):
    """Main application window with tabbed interface for all workflow phases."""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Automated Video Workflow")
        self.setMinimumSize(900, 900)  # Taller minimum height to prevent vertical overlapping
        self.setStyleSheet(WINDOW_STYLE)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        # Set size policy to make the central widget expand in both directions
        self.central_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        
        # Add header
        self.header = create_header("Automated Video Workflow")
        self.main_layout.addWidget(self.header)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setMovable(False)
        self.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.main_layout.addWidget(self.tab_widget, 1)
        
        # Initialize tabs
        self.init_tabs()
        
        # Add bottom button bar
        self.create_button_bar()
        
        # Create status bar
        self.status_bar = create_status_bar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Connect signals
        self.connect_signals()
    
    def init_tabs(self):
        """Initialize all tabs for the workflow phases."""
        # Configuration tab
        self.config_tab = ConfigTab()
        self.tab_widget.addTab(self.config_tab, "Configuration")
        
        # SD Card Detection tab
        self.sd_detection_tab = SDDetectionTab()
        self.tab_widget.addTab(self.sd_detection_tab, "SD Card Detection")
        
        # Folder Structure tab
        self.folder_structure_tab = FolderStructureTab()
        self.tab_widget.addTab(self.folder_structure_tab, "Folder Structure")
        
        # Proxy Generator tab
        self.proxy_generator_tab = ProxyGeneratorTab()
        self.tab_widget.addTab(self.proxy_generator_tab, "Proxy Generator")
        
        # Export Watcher tab
        self.export_watcher_tab = ExportWatcherTab()
        self.tab_widget.addTab(self.export_watcher_tab, "Export Watcher")
        
        # Upload tab
        self.upload_tab = UploadTab()
        self.tab_widget.addTab(self.upload_tab, "Upload")
        
        # Log Viewer tab
        self.log_viewer_tab = LogViewerTab()
        self.tab_widget.addTab(self.log_viewer_tab, "Logs")
    
    def create_button_bar(self):
        """Create the bottom button bar."""
        button_container = QWidget()
        button_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_container.setMinimumHeight(60)  # Ensure enough vertical space
        
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(20)  # Increased spacing between buttons
        
        # Add spacer to push buttons to the right
        button_layout.addStretch(1)
        
        # Run workflow button
        self.run_button = create_button("Run Workflow")
        button_layout.addWidget(self.run_button)
        
        # Stop workflow button
        self.stop_button = create_button("Stop", primary=False)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        # Add spacer to center buttons
        button_layout.addStretch(1)
        
        self.main_layout.addWidget(button_container)
    
    def connect_signals(self):
        """Connect signals and slots."""
        # Connect run button
        self.run_button.clicked.connect(self.run_workflow)
        
        # Connect stop button
        self.stop_button.clicked.connect(self.stop_workflow)
        
        # Connect tab changed signal
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    def run_workflow(self):
        """Run the workflow."""
        # Get current tab
        current_tab = self.tab_widget.currentWidget()
        
        # Run the current tab's workflow
        if hasattr(current_tab, 'run'):
            try:
                current_tab.run()
                self.run_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.status_bar.showMessage(f"Running {self.tab_widget.tabText(self.tab_widget.currentIndex())} workflow...")
            except Exception as e:
                show_error(self, "Error", f"Failed to run workflow: {e}")
    
    def stop_workflow(self):
        """Stop the workflow."""
        # Get current tab
        current_tab = self.tab_widget.currentWidget()
        
        # Stop the current tab's workflow
        if hasattr(current_tab, 'stop'):
            try:
                current_tab.stop()
                self.run_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.status_bar.showMessage("Workflow stopped")
            except Exception as e:
                show_error(self, "Error", f"Failed to stop workflow: {e}")
    
    def on_tab_changed(self, index):
        """Handle tab changed event."""
        # Reset buttons
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Update status bar
        tab_name = self.tab_widget.tabText(index)
        self.status_bar.showMessage(f"Selected {tab_name} tab")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Ask for confirmation if any workflow is running
        if self.stop_button.isEnabled():
            if show_question(self, "Confirm Exit", "A workflow is currently running. Are you sure you want to exit?"):
                # Stop all workflows
                for i in range(self.tab_widget.count()):
                    tab = self.tab_widget.widget(i)
                    if hasattr(tab, 'stop'):
                        try:
                            tab.stop()
                        except:
                            pass
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def run_gui():
    """Run the GUI application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
