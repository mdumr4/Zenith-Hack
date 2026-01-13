@echo off
echo ==========================================
echo      Frai AI Keyboard - Stop Script
echo ==========================================

echo [INFO] Stopping Frai Python processes...

REM Use PowerShell to find and kill only our specific python scripts
REM This avoids killing other random Python stuff on the user's machine.
powershell -Command "Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -like '*src/python_brain/*' } | ForEach-Object { Write-Host 'Killing PID:' $_.ProcessId; Stop-Process $_.ProcessId -Force }"

echo.
echo [SUCCESS] Cleanup Complete.
pause
