@echo off
setlocal
echo ==========================================
echo      Frai AI Keyboard - Launcher
echo ==========================================

REM 1. Register the IME DLL (Requires Admin usually, but updated per-user in Win8+)
echo [INFO] Registering IME...
if exist "build\Release\FraiIME.dll" (
    regsvr32.exe /s "build\Release\FraiIME.dll"
    echo [INFO] DLL Registered.
) else (
    echo [WARNING] build\Release\FraiIME.dll not found. Did you run build_all.bat?
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
