#!/usr/bin/env python3
"""
Build script for Network Discovery Tool
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['pyinstaller', 'scapy', 'customtkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        for package in missing_packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])
    
    print("All dependencies are available.")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Network Discovery Tool executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create single executable
        '--windowed',                   # Hide console window
        '--name=LDM',  # Executable name
        '--icon=icon.ico',              # Icon (if available)
        '--add-data=venv/Lib/site-packages/customtkinter;customtkinter/',  # Include CustomTkinter assets
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=scapy',
        '--hidden-import=scapy.all',
        '--hidden-import=customtkinter',
        'network_discovery_tool.py'
    ]
    
    # Remove icon flag if icon doesn't exist
    if not os.path.exists('icon.ico'):
        cmd.remove('--icon=icon.ico')
    
    # Remove customtkinter data if not in venv
    if not os.path.exists('venv/Lib/site-packages/customtkinter'):
        cmd = [arg for arg in cmd if not arg.startswith('--add-data')]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print("Executable created in: dist/LDM.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_installer():
    """Create a simple installer script"""
    installer_content = '''@echo off
echo Installing Network Discovery Tool...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator - proceeding with installation
) else (
    echo Please run this installer as administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Create installation directory
set INSTALL_DIR=C:\\Program Files\\NetworkDiscoveryTool
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "dist\\LDM.exe" "%INSTALL_DIR%\\"

REM Create desktop shortcut
set DESKTOP=%USERPROFILE%\\Desktop
echo @echo off > "%DESKTOP%\\Network Discovery Tool.bat"
echo cd /d "%INSTALL_DIR%" >> "%DESKTOP%\\Network Discovery Tool.bat"
echo start "" "LDM.exe" >> "%DESKTOP%\\Network Discovery Tool.bat"

echo.
echo Installation completed successfully!
echo A shortcut has been created on your desktop.
echo.
pause
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content)
    
    print("Installer script created: install.bat")

def main():
    """Main build process"""
    print("=== Network Discovery Tool Builder ===")
    print()
    
    # Check dependencies
    check_dependencies()
    print()
    
    # Build executable
    if build_executable():
        print()
        create_installer()
        print()
        print("=== Build Summary ===")
        print("✓ Executable: dist/LDM.exe")
        print("✓ Installer: install.bat")
        print()
        print("To install the tool:")
        print("1. Run install.bat as administrator")
        print("2. Or simply run dist/LDM.exe directly")
        print()
        print("Note: The tool requires administrator privileges to capture network packets.")
    else:
        print("Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 