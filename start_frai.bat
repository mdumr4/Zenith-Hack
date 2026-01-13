@echo off
setlocal
echo ==========================================
echo      Frai AI Keyboard - Launcher
echo ==========================================

REM 0. Check for Admin Privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [ERROR] CRITICAL: YOU ARE NOT RUNNING AS ADMINISTRATOR.
    echo.
    echo Windows blocks IME registration without Admin rights.
    echo Error 0x80004005 will happen.
    echo.
    echo PLEASE:
    echo 1. Close this window.
    echo 2. Right-Click your Terminal / Command Prompt.
    echo 3. Select "Run as Administrator".
    echo 4. Run this script again.
    echo.
    pause
    exit /b
)

REM 1. Register the IME DLL (Requires Admin usually, but updated per-user in Win8+)
REM 1. Register the IME DLL (Requires Admin)
echo [INFO] Registering IME...
set "DLL_PATH=build\FraiIME.dll"
if exist "build\Release\FraiIME.dll" set "DLL_PATH=build\Release\FraiIME.dll"
REM Prefer the one in root build if it is newer (simple check: if root exists use it, copy might have failed)
if exist "build\FraiIME.dll" set "DLL_PATH=build\FraiIME.dll"

if exist "%DLL_PATH%" (
    echo [INFO] Found DLL at: %DLL_PATH%
    regsvr32.exe /s "%DLL_PATH%"
    echo [INFO] DLL Registered.
) else (
    echo [WARNING] FraiIME.dll not found in build or build\Release. Run build_all.bat!
)

REM 2. Start Python Brain (Backend)
echo [INFO] Starting AI Backend (Port 18492)...
if exist "venv\Scripts\python.exe" (
    start "FraiBrain" /B venv\Scripts\python.exe src/python_brain/server.py
) else (
    echo [WARNING] venv not found. Using global python...
    start "FraiBrain" /B python src/python_brain/server.py
)

REM 3. Start Python UI (Overlay)
echo [INFO] Starting UI Overlay...
if exist "venv\Scripts\python.exe" (
    start "FraiUI" /B venv\Scripts\python.exe src/python_brain/ui/main.py
) else (
    start "FraiUI" /B python src/python_brain/ui/main.py
)

echo.
echo [SUCCESS] Frai AI Keyboard is running!
echo ------------------------------------------
echo - Backend: http://127.0.0.1:18492
echo - UI: Overlay Active
echo - IME: Registered
echo.
echo Type in any app (Notepad) to test.
echo Close this window to keep running in background, or Ctrl+C to stop script.
pause
