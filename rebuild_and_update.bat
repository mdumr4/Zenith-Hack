@echo off
echo ==========================================
echo      FORCE REBUILD AND UPDATE
echo ==========================================
echo.
echo [IMPORTANT] Please CLOSE NOTEPAD and any other apps using the keyboard!
echo If you don't close them, the update will FAIL.
echo.
pause

echo.
echo [1/4] Cleaning old build artifacts (including cache)...
rmdir /s /q build
del /F /Q FraiIME.dll 2>nul
del /F /Q Release\FraiIME.dll 2>nul

echo.
echo [2/4] Generating Project...
cmake -B build
if %errorlevel% neq 0 (
    echo [ERROR] CMake Generation Failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [3/4] Building C++ Core...
cmake --build build --config Release
if %errorlevel% neq 0 (
    echo [ERROR] Build Failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [4/4] Deploying new DLL...
copy /Y build\Release\FraiIME.dll FraiIME.dll
if %errorlevel% neq 0 (
    echo [ERROR] Could not overwrite FraiIME.dll. Is Notepad still open?
    pause
    exit /b %errorlevel%
)

echo.
echo [SUCCESS] DLL Updated Successfully!
echo You can now restart start_frai.bat.
pause
