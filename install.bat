@echo off
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
set INSTALL_DIR=C:\Program Files\NetworkDiscoveryTool
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "dist\LDM.exe" "%INSTALL_DIR%\"

REM Create desktop shortcut
set DESKTOP=%USERPROFILE%\Desktop
echo @echo off > "%DESKTOP%\Network Discovery Tool.bat"
echo cd /d "%INSTALL_DIR%" >> "%DESKTOP%\Network Discovery Tool.bat"
echo start "" "LDM.exe" >> "%DESKTOP%\Network Discovery Tool.bat"

echo.
echo Installation completed successfully!
echo A shortcut has been created on your desktop.
echo.
pause
