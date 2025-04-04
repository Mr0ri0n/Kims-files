# Automated Video Workflow

> ## ⚠️ WARNING ⚠️
> ### THIS SOFTWARE IS NOT TESTED AND COMES WITH NO GUARANTEES
> ### USE AT YOUR OWN RISK
> ### NO WARRANTY IS PROVIDED OR IMPLIED

A Python-based automation tool for video production workflows, handling everything from SD card import to final delivery. Features a modern, responsive GUI interface built with PyQt6. Designed to work seamlessly across Windows, macOS, and Linux platforms.

## Project Overview

This project automates the video production workflow with the following features:

- SD card detection and automatic file import
- Organized folder structure creation with cross-platform path handling
- Optional proxy file generation with customizable settings
- Export folder monitoring
- Automatic upload to delivery platforms
- Modern GUI interface with dark theme and responsive layout
- Comprehensive logging system
- Full cross-platform compatibility (Windows, macOS, Linux)

## Project Structure

```
📁 video_workflow/
 ┣━━ 📁 config/                  # Configuration directory
 ┃    ┗━━ 📄 config.json        # User configuration settings
 ┣━━ 📁 docs/                    # Documentation
 ┃    ┣━━ 📄 INSTALLATION.md    # Detailed setup instructions
 ┃    ┣━━ 📁 design/            # Design documentation
 ┃    ┃    ┗━━ 📄 template_gui.md  # GUI template specifications
 ┃    ┗━━ 📁 planning/          # Project planning documents
 ┃         ┗━━ 📄 progressplan.md  # Development progress plan
 ┣━━ 📁 logs/                    # Log files directory
 ┣━━ 📁 src/                     # Source code
 ┃    ┣━━ 📄 __init__.py        # Package initialization
 ┃    ┣━━ 📄 main.py            # Main application entry point
 ┃    ┣━━ 📄 config_manager.py  # Configuration handling
 ┃    ┣━━ 📄 logger.py          # Logging system
 ┃    ┣━━ 📄 disk_monitor.py    # SSD/SD card detection
 ┃    ┗━━ 📁 gui/               # GUI components
 ┃         ┣━━ 📄 main_window.py  # Main application window
 ┃         ┣━━ 📄 ui_template.py  # UI styling and components
 ┃         ┗━━ 📁 tabs/           # Tab-specific implementations
 ┃              ┣━━ 📄 config_tab.py         # Configuration tab
 ┃              ┣━━ 📄 sd_detection_tab.py   # SD card detection tab
 ┃              ┣━━ 📄 folder_structure_tab.py # Folder creation tab
 ┃              ┣━━ 📄 proxy_generator_tab.py # Proxy generation tab
 ┃              ┣━━ 📄 export_watcher_tab.py # Export monitoring tab
 ┃              ┣━━ 📄 upload_tab.py         # File upload tab
 ┃              ┗━━ 📄 log_viewer_tab.py     # Log viewing tab
 ┣━━ 📁 templates/               # DaVinci Resolve templates
 ┣━━ 📄 README.md               # Project overview
 ┗━━ 📄 requirements.txt        # Python dependencies
```

## Setup and Installation

1. Install Python 3.13.0 or newer
2. Install required dependencies:
   ```
   pip install PyQt6==6.8.1
   ```
3. Configure the paths in `config/config.json` to match your system
4. Run the application using:
   ```
   python src/main.py
   ```

## Development Progress

This project has been developed in phases as outlined in the progress plan:

- [x] Phase 1: Foundation Setup
- [x] Phase 2: SD Card Detection + Auto-Import
- [x] Phase 3: Folder Structure Generator
- [x] Phase 4: Proxy Generator
- [x] Phase 5: Export Folder Watcher
- [x] Phase 6: Playbook Upload Automation
- [x] Phase 7: GUI Interface Implementation
- [ ] Final Phase: Packaging & Scheduling

## Features

### Modern UI
- Dark theme with purple accents
- Responsive layout with scrollable content areas in all tabs
- Custom-styled scrollbars and tab navigation with hover effects
- Minimum window size (900x900) to ensure proper display of all elements

### SD Card Detection
- Automatic detection of SD cards when connected
- Monitoring of SD card status and available space
- Configurable polling interval

### Folder Structure Generator
- Create organized project folders with customizable structure
- Date-based project organization
- Cross-platform path handling using Python's pathlib
- Optional DaVinci Resolve template integration

### Proxy Generator
- Automatic proxy file generation using ffmpeg
- Customizable resolution, codec, and quality settings
- Progress tracking and status updates

### Export Watcher
- Monitor export folders for new rendered files
- Automatic file organization with date-based folders
- Optional file renaming with timestamps

### Upload Automation
- Upload files to external platforms via API
- Duplicate detection using file hashing
- Progress tracking and status updates

### Configuration
- Save and load configuration settings
- Customizable paths for raw footage, master files, and exports
- Proxy generation settings (resolution, codec, quality)
- Logging preferences with real-time updates

## Requirements

- Python 3.13.0+
- PyQt6 6.8.1+
- ffmpeg (for proxy generation)
- Additional dependencies are specified in requirements.txt

## Usage

### GUI Mode

Run the application with the GUI interface:

```
python src/main.py
```

### CLI Mode

Run specific functions from the command line:

```
python src/main.py --scan-sd      # Scan for SD cards
python src/main.py --create-folders # Create folder structure only
python src/main.py --generate-proxies # Generate proxy files
python src/main.py --watch-exports # Monitor export folder
python src/main.py --upload # Upload files to external platform
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
