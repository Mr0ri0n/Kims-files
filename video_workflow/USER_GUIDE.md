# Video Workflow Application - User Guide

## Overview

The Video Workflow Application is a comprehensive tool designed to streamline the video production process. It provides several key features:

1. **Folder Structure Generator**: Create organized project folders with a consistent structure
2. **SD Card Detection**: Scan and import video files from SD cards
3. **Proxy Generator**: Create proxy files for smoother video editing
4. **File Upload**: Upload video files to cloud storage

This guide will walk you through each feature and how to use them effectively.

## Getting Started

1. Launch the application by running `python src/main.py` from the project directory
2. The application will open with a tabbed interface, each tab representing a different feature
3. Navigate between tabs by clicking on the tab names at the top of the window

## Folder Structure Generator

This feature helps you create a consistent folder structure for your video projects.

### How to Use

1. **Project Settings**:
   - Enter a project name (e.g., "Client_ProjectTitle")
   - Select a base directory where all projects will be stored
   - The DaVinci Resolve template will be included automatically if available

2. **Project Date**:
   - Choose whether to use today's date (recommended) or select a custom date
   - The date will be used as part of the folder structure

3. **Folder Structure**:
   - Select which folders to include in your project structure
   - Standard options include footage, proxies, exports, and logs
   - Each folder has a specific purpose described in the interface

4. **Create Structure**:
   - Click the "Create Folder Structure" button to generate your folders
   - The activity log will show the progress and confirm when folders are created

5. **Result**:
   - Your project will be organized as: Base Directory / Date / Project Name / Selected Folders
   - If a DaVinci Resolve template is available, it will be copied to your project folder

## SD Card Detection

This feature helps you scan SD cards for video files and import them to your project folders.

### How to Use

1. **Detect SD Cards**:
   - Insert your SD card into your computer
   - Click "Scan for SD Cards" to detect available SD cards
   - A progress bar will show the scanning progress
   - Select the SD card from the list once detected

2. **Browse Video Files**:
   - After selecting an SD card, the application will scan for video files
   - A progress bar will show the scanning progress
   - The file list will display all video files found on the SD card

3. **Import Files**:
   - Select a destination folder for the imported files
   - Click "Import Files" to copy the files from the SD card
   - The progress bar will show the copying progress
   - The activity log will confirm when files are successfully imported

4. **Monitoring Mode**:
   - Click "Start Monitoring" to continuously monitor for SD card insertions
   - The application will automatically detect when new SD cards are inserted
   - Click "Stop Monitoring" to turn off this feature

## Proxy Generator

This feature creates lower-resolution proxy files for smoother editing with high-resolution footage.

### How to Use

1. **Select Source Files**:
   - Choose a source directory containing your video files
   - Click "Scan for Video Files" to find all video files in the directory
   - The file list will display all video files found

2. **Configure Proxy Settings**:
   - Select a destination directory for the proxy files
   - Choose the desired proxy resolution (e.g., 720p, 540p)
   - Set the quality level (higher quality results in larger files)
   - Select the encoder to use (H.264 is recommended for compatibility)

3. **Generate Proxies**:
   - Click "Generate Proxies" to start the conversion process
   - The progress bar will show the overall progress
   - The activity log will display detailed information about each file being processed
   - Click "Cancel" to stop the process if needed

4. **Using Proxies in Editing**:
   - Import both original files and proxies into your editing software
   - Link the proxy files to the original high-resolution files
   - Edit with the proxy files for better performance
   - Switch back to the original files for final export

## File Upload

This feature helps you upload video files to cloud storage services.

### How to Use

1. **Select Source Files**:
   - Choose a source directory containing your video files
   - Click "Scan for Files" to find all files in the directory
   - The file list will display all files found

2. **Configure Upload Settings**:
   - Select the destination service (e.g., Google Drive, Dropbox)
   - Enter your account credentials if required
   - Choose upload options such as folder structure and permissions

3. **Upload Files**:
   - Click "Upload Files" to start the upload process
   - The progress bar will show the overall progress
   - The activity log will display detailed information about each file being uploaded
   - Click "Cancel" to stop the process if needed

## Creating an Automated Workflow

You can set up a fully automated video production workflow using this application. Here's how to configure each component for automation:

### 1. Configure Your Environment

1. **Initial Setup**:
   - Ensure Python 3.13.0+ is installed
   - Install all required dependencies: `pip install PyQt6==6.8.1`
   - Configure your paths in `config/config.json` to match your system

### 2. Automated SD Card Detection

1. **Configure SD Card Monitoring**:
   - Go to the SD Detection tab
   - Set your preferred polling interval (how often to check for SD cards)
   - Click "Start Monitoring"
   - The system will now automatically detect SD cards when connected

2. **Configure Auto-Import**:
   - Set a default destination folder for imported files
   - Enable the "Auto-import on detection" option if available
   - When an SD card is detected, files will be automatically imported

### 3. Automated Folder Structure Creation

1. **Standard Project Structure**:
   - In the Folder Structure tab, save your preferred folder structure as a template
   - Configure your base directory for all projects
   - Enable "Create structure on import" if available

2. **DaVinci Resolve Integration**:
   - The application will automatically include DaVinci Resolve templates if available
   - No manual configuration needed for this feature

### 4. Automated Proxy Generation

1. **Configure Proxy Settings**:
   - In the Proxy Generator tab, set your preferred proxy settings:
     - Resolution (e.g., 1280x720)
     - Codec (e.g., H.264)
     - Quality settings
   - Enable "Auto-generate proxies after import" if available

### 5. Automated Export Monitoring

1. **Configure Export Watcher**:
   - In the Export Watcher tab, set the folder to monitor
   - Configure how you want exported files to be processed
   - Enable "Auto-start monitoring on launch" if available

### 6. Automated Upload

1. **Configure Upload Settings**:
   - In the Upload tab, configure your cloud service credentials
   - Set up default upload destinations
   - Enable "Auto-upload after export" if available

### 7. Running the Automated Workflow

1. **Launch at System Startup**:
   - Configure your operating system to launch the application at startup
   - For macOS: Add the application to Login Items
   - For Windows: Add a shortcut to the Startup folder

2. **Command Line Automation**:
   - Use command line arguments for headless operation:
   ```
   python src/main.py --auto-workflow
   ```

3. **Monitoring the Automated Process**:
   - Check the Log Viewer tab for activity logs
   - Configure email or notification alerts if available

## Tips and Best Practices

1. **Consistent Naming**: Use consistent naming conventions for your projects
2. **Regular Backups**: Always back up your project files regularly
3. **Check Space**: Ensure you have enough disk space before generating proxies
4. **SD Card Handling**: Always safely eject SD cards after importing files
5. **Proxy Workflow**: Create proxies immediately after importing footage for the best workflow
6. **Test Your Workflow**: Always test your automated workflow with sample data before using it in production

## Troubleshooting

1. **Application Not Starting**:
   - Ensure Python and all required dependencies are installed
   - Check the console for error messages

2. **SD Cards Not Detected**:
   - Try reinserting the SD card
   - Check if the SD card is properly formatted
   - Try a different SD card reader

3. **Slow File Scanning**:
   - Limit the depth of directories being scanned
   - Exclude system and hidden files from scanning
   - Use faster storage media when possible

4. **Proxy Generation Errors**:
   - Ensure FFmpeg is properly installed and configured
   - Check that source files are not corrupted
   - Verify you have sufficient disk space

5. **Upload Failures**:
   - Check your internet connection
   - Verify your account credentials
   - Ensure you have sufficient storage space in the cloud service
