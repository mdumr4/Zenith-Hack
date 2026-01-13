@echo off
echo ==========================================
echo      Frai AI Keyboard - Environment Setup
echo ==========================================

REM 1. Check if Python is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org
    pause
    exit /b
)

REM 2. Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment 'venv'...
    python -m venv venv
) else (
    echo [INFO] Virtual environment 'venv' already exists.
)

REM 3. Activate and Install
echo [INFO] Installing dependencies from requirements.txt...
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo [SUCCESS] Environment Setup Complete!
echo You can now run 'build_all.bat' (if not done) and 'start_frai.bat'.
pause
