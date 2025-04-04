#!/usr/bin/env python3
"""
Disk Monitor for Automated Video Workflow

Handles detection of external drives and SD cards.
"""

import os
import platform
import subprocess
import time
from pathlib import Path

class DiskMonitor:
    """Monitors for external drives and SD cards."""
    
    def __init__(self, logger=None):
        """
        Initialize the disk monitor.
        
        Args:
            logger: Logger instance for logging events
        """
        self.logger = logger
        self.system = platform.system()
    
    def is_drive_mounted(self, drive_name):
        """
        Check if a specific drive is mounted.
        
        Args:
            drive_name (str): Name of the drive to check
            
        Returns:
            bool: True if mounted, False otherwise
        """
        if self.system == "Windows":
            return self._is_drive_mounted_windows(drive_name)
        elif self.system == "Darwin":  # macOS
            return self._is_drive_mounted_macos(drive_name)
        else:  # Linux and others
            return self._is_drive_mounted_linux(drive_name)
    
    def _is_drive_mounted_windows(self, drive_name):
        """Check if drive is mounted on Windows."""
        try:
            # List all drives
            drives = [d for d in os.listdir() if os.path.ismount(d)]
            
            # Check if drive_name is in the list of drives
            for drive in drives:
                # Get volume name
                try:
                    volume_name = subprocess.check_output(
                        ["cmd", "/c", f"vol {drive}"],
                        stderr=subprocess.STDOUT,
                        universal_newlines=True
                    )
                    if drive_name.lower() in volume_name.lower():
                        if self.logger:
                            self.logger.info(f"Found drive '{drive_name}' at {drive}")
                        return True
                except subprocess.CalledProcessError:
                    continue
            
            if self.logger:
                self.logger.debug(f"Drive '{drive_name}' not found")
            return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error checking for Windows drive: {e}")
            return False
    
    def _is_drive_mounted_macos(self, drive_name):
        """Check if drive is mounted on macOS."""
        try:
            # Check if /Volumes/drive_name exists
            volumes_path = Path("/Volumes")
            if not volumes_path.exists():
                if self.logger:
                    self.logger.warning("'/Volumes' directory not found")
                return False
            
            # List all volumes
            volumes = [v.name for v in volumes_path.iterdir() if v.is_dir()]
            
            # Check if drive_name is in the list of volumes
            for volume in volumes:
                if drive_name.lower() in volume.lower():
                    if self.logger:
                        self.logger.info(f"Found drive '{drive_name}' at /Volumes/{volume}")
                    return True
            
            if self.logger:
                self.logger.debug(f"Drive '{drive_name}' not found in /Volumes")
            return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error checking for macOS drive: {e}")
            return False
    
    def _is_drive_mounted_linux(self, drive_name):
        """Check if drive is mounted on Linux."""
        try:
            # Run mount command to get all mounted drives
            result = subprocess.check_output(
                ["mount"],
                universal_newlines=True
            )
            
            # Check if drive_name is in the output
            if drive_name.lower() in result.lower():
                if self.logger:
                    self.logger.info(f"Found drive '{drive_name}' in mount list")
                return True
            
            if self.logger:
                self.logger.debug(f"Drive '{drive_name}' not found in mount list")
            return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error checking for Linux drive: {e}")
            return False
    
    def wait_for_drive(self, drive_name, timeout=None, check_interval=5):
        """
        Wait for a drive to be mounted.
        
        Args:
            drive_name (str): Name of the drive to wait for
            timeout (int, optional): Maximum time to wait in seconds. None for no timeout.
            check_interval (int, optional): Interval between checks in seconds. Defaults to 5.
            
        Returns:
            bool: True if drive was mounted, False if timeout was reached
        """
        if self.logger:
            self.logger.info(f"Waiting for drive '{drive_name}' to be mounted...")
        
        start_time = time.time()
        
        while True:
            if self.is_drive_mounted(drive_name):
                if self.logger:
                    self.logger.info(f"Drive '{drive_name}' is now mounted")
                return True
            
            # Check if timeout has been reached
            if timeout and (time.time() - start_time > timeout):
                if self.logger:
                    self.logger.warning(f"Timeout reached waiting for drive '{drive_name}'")
                return False
            
            # Wait before checking again
            time.sleep(check_interval)
    
    def detect_sd_cards(self):
        """
        Detect SD cards that are currently mounted.
        
        Returns:
            list: List of SD card paths that were detected
        """
        # Implementation depends on the platform
        if self.system == "Windows":
            return self._detect_sd_cards_windows()
        elif self.system == "Darwin":  # macOS
            return self._detect_sd_cards_macos()
        else:  # Linux and others
            return self._detect_sd_cards_linux()
    
    def _detect_sd_cards_windows(self):
        """Detect SD cards on Windows."""
        # This is a simplified implementation
        # In a real scenario, would need to check drive types
        sd_cards = []
        
        try:
            import win32api
            
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            
            for drive in drives:
                # Check if drive is removable
                if win32api.GetDriveType(drive) == win32api.DRIVE_REMOVABLE:
                    sd_cards.append(drive)
                    if self.logger:
                        self.logger.info(f"Detected removable drive: {drive}")
        except ImportError:
            if self.logger:
                self.logger.error("win32api module not available for SD card detection")
            # Fallback method
            for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    # This is a very basic check and not reliable
                    sd_cards.append(drive)
                    if self.logger:
                        self.logger.info(f"Detected drive: {drive}")
        
        return sd_cards
    
    def _detect_sd_cards_macos(self):
        """Detect SD cards on macOS."""
        sd_cards = []
        
        try:
            # Run diskutil to list all volumes
            result = subprocess.check_output(
                ["diskutil", "list", "-plist", "external"],
                universal_newlines=True
            )
            
            # Parse the output to find SD cards
            # This is a placeholder - in a real implementation,
            # you would parse the plist output properly
            
            # For now, just check /Volumes for removable media
            volumes_path = Path("/Volumes")
            for volume in volumes_path.iterdir():
                if volume.is_dir() and volume.name not in ["Macintosh HD", "Home"]:
                    sd_cards.append(str(volume))
                    if self.logger:
                        self.logger.info(f"Detected potential SD card: {volume}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error detecting SD cards on macOS: {e}")
        
        return sd_cards
    
    def _detect_sd_cards_linux(self):
        """Detect SD cards on Linux."""
        sd_cards = []
        
        try:
            # Check /dev/disk/by-id for SD cards
            disk_path = Path("/dev/disk/by-id")
            if disk_path.exists():
                for disk in disk_path.iterdir():
                    if "usb" in disk.name.lower() or "sd" in disk.name.lower():
                        # This is a very basic check
                        sd_cards.append(str(disk))
                        if self.logger:
                            self.logger.info(f"Detected potential SD card: {disk}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error detecting SD cards on Linux: {e}")
        
        return sd_cards
