@echo off
echo ==========================================
echo      PROJECT CLEANUP TOOL
echo ==========================================
echo.
echo This will delete:
echo  - build/ folder (C++ artifacts)
echo  - __pycache__ folders (Python bytecode)
echo  - Temporary log files (frai_debug.txt, *.log)
echo  - VS Code .vs folder
echo.
echo [NOTE] It will NOT delete 'venv' or 'FraiIME.dll' (the deployed file).
echo.
set /p "CHOICE=Are you sure you want to clean? (Y/N): "
if /i "%CHOICE%" neq "Y" exit /b

echo.
echo [1/4] Deleting Build Folder...
rmdir /s /q build 2>nul
rmdir /s /q .vs 2>nul

echo.
echo [2/4] Cleaning Python Bytecode...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo.
echo [3/4] Removing logs...
del /F /Q FraiIME.iobj 2>nul
del /F /Q FraiIME.ipdb 2>nul
del /F /Q FraiIME.lib 2>nul
del /F /Q FraiIME.exp 2>nul
del /F /Q FraiIME.pdb 2>nul
del /F /Q frai_debug.txt 2>nul
del /F /Q *.log 2>nul
del /F /Q *.tmp 2>nul

echo.
echo [SUCCESS] Project Cleaned!
pause
