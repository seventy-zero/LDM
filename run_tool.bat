@echo off
echo Network Discovery Tool Launcher
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "network_discovery_tool.py" (
    echo ERROR: network_discovery_tool.py not found
    echo Please ensure you're running this from the correct directory
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import scapy, customtkinter" >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %errorLevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Network Discovery Tool...
echo Note: This tool requires administrator privileges for packet capture
echo.

REM Run the tool
python network_discovery_tool.py

REM Check if the tool ran successfully
if %errorLevel% neq 0 (
    echo.
    echo ERROR: The tool encountered an error
    echo Please check the error messages above
    pause
) 