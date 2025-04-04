# Installation Guide for Automated Video Workflow

This guide provides detailed instructions for installing and configuring the Automated Video Workflow application on your system. The application is designed to work seamlessly across Windows, macOS, and Linux platforms with consistent path handling.

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **Python**: Version 3.13.0 or newer
- **Disk Space**: At least 500MB for the application and dependencies
- **RAM**: Minimum 4GB recommended
- **External Tools**: ffmpeg (for proxy generation)

## Step 1: Install Python

### Windows
1. Download Python 3.13.0 or newer from the [official Python website](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Complete the installation

### macOS
1. Install Homebrew if not already installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python using Homebrew:
   ```bash
   brew install python@3.13
   ```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.13 python3.13-venv python3.13-dev
```

## Step 2: Install ffmpeg

### Windows
1. Download the ffmpeg build from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the archive to a location on your computer (e.g., `C:\ffmpeg`)
3. Add the `bin` folder to your system PATH:
   - Right-click on "This PC" and select "Properties"
   - Click on "Advanced system settings"
   - Click on "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add the path to the bin folder (e.g., `C:\ffmpeg\bin`)
   - Click "OK" on all dialogs

### macOS
```bash
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

## Step 3: Clone or Download the Repository

### Using Git
```bash
git clone https://github.com/yourusername/video_workflow.git
cd video_workflow
```

### Manual Download
1. Download the ZIP file from the repository
2. Extract it to your desired location
3. Open a terminal/command prompt and navigate to the extracted folder

## Step 4: Set Up a Virtual Environment (Recommended)

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux
```bash
python3.13 -m venv venv
source venv/bin/activate
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available, install the required packages manually:

```bash
pip install PyQt6==6.8.1
pip install watchdog
pip install requests
```

## Step 6: Configure the Application

1. Create a `config` directory in the project root if it doesn't exist:
   ```bash
   mkdir -p config
   ```

2. Create or edit the `config/config.json` file with your specific settings:
   ```json
   {
     "paths": {
       "raw_footage": "/path/to/raw/footage",  /* Use forward slashes even on Windows */
       "proxies": "/path/to/proxies",
       "exports": "/path/to/exports",
       "master": "/path/to/master/files",
       "logs": "/path/to/logs"
     },
     "sd_detection": {
       "polling_interval": 5,
       "auto_import": true
     },
     "proxy_generation": {
       "resolution": "1280x720",
       "codec": "h264",
       "crf": 23,
       "auto_generate": false
     },
     "export_watcher": {
       "auto_rename": true,
       "create_dated_folders": true
     },
     "upload": {
       "api_endpoint": "https://your-api-endpoint.com/upload",
       "avoid_duplicates": true
     }
   }
   ```

3. Adjust the paths and settings to match your workflow and system configuration

## Step 7: Run the Application

### GUI Mode
```bash
# From the project root directory
python src/main.py
```

### CLI Mode
```bash
# Scan for SD cards
python src/main.py --scan-sd

# Create folder structure
python src/main.py --create-folders

# Generate proxy files
python src/main.py --generate-proxies

# Watch export folder
python src/main.py --watch-exports

# Upload files
python src/main.py --upload
```

## Troubleshooting

### Path Handling Issues

If you encounter issues with file paths:

1. Ensure all paths in the configuration use forward slashes (`/`) even on Windows
2. Avoid using backslashes (`\`) as they can cause parsing issues
3. For Windows users, both absolute paths (`C:/Users/...`) and relative paths work correctly
4. For network paths, use the full UNC path format (`//server/share/...`)

### PyQt6 Installation Issues

If you encounter DLL loading errors with PyQt6 on Python 3.13.0:

1. Try reinstalling PyQt6:
   ```bash
   pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
   pip install PyQt6==6.8.1
   ```

2. Ensure you have the Microsoft Visual C++ Redistributable installed (Windows only)

### ffmpeg Not Found

If the application cannot find ffmpeg:

1. Verify ffmpeg is installed by running:
   ```bash
   ffmpeg -version
   ```

2. If installed but not found, ensure it's in your system PATH
3. For Windows, you might need to restart your computer after adding ffmpeg to PATH

### Permission Issues

If you encounter permission issues when accessing directories:

1. Ensure the application has read/write permissions to all configured directories
2. Run the application with elevated privileges if necessary (not recommended for regular use)

## Additional Configuration

### Setting Up Auto-Start (Optional)

#### Windows
1. Create a shortcut to the application
2. Press `Win+R`, type `shell:startup`, and press Enter
3. Move the shortcut to the Startup folder

#### macOS
1. Open System Preferences > Users & Groups
2. Select your user and click on "Login Items"
3. Click the "+" button and select the application or a script that launches it

#### Linux (Systemd)
1. Create a service file in `/etc/systemd/system/video-workflow.service`:
   ```
   [Unit]
   Description=Automated Video Workflow
   After=network.target

   [Service]
   User=yourusername
   WorkingDirectory=/path/to/video_workflow
   ExecStart=/path/to/python /path/to/video_workflow/src/main.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```
2. Enable and start the service:
   ```bash
   sudo systemctl enable video-workflow
   sudo systemctl start video-workflow
   ```

## Updating the Application

To update the application to the latest version:

1. If using Git:
   ```bash
   git pull origin main
   ```

2. If downloaded manually, download the latest version and replace the files

3. Update dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. Run the application as usual

## Support and Resources

If you encounter any issues or need assistance:

1. Check the troubleshooting section above
2. Review the project documentation
3. Submit an issue on the project repository
4. Contact the project maintainers
