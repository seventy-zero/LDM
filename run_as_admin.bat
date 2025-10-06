@echo off
echo Starting LDM with administrator privileges...
echo This will allow LDM to capture LLDP packets without requiring Npcap.
echo.
powershell -Command "Start-Process 'LDM.exe' -Verb RunAs"
