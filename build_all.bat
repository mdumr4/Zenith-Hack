@echo off
echo ==========================================
echo      Frai AI Keyboard - Build Script
echo ==========================================

REM 1. Check for CMake
where cmake >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] CMake is not installed or not in PATH.
    echo Please install CMake from https://cmake.org/download/
    pause
    exit /b
)

REM 2. Create Build Directory
if not exist "build" (
    echo [INFO] Creating build directory...
    mkdir build
)

REM 3. Run CMake Generation
cd build
echo [INFO] Generating Visual Studio Project files...
cmake .. -A x64
if %errorlevel% neq 0 (
    echo [ERROR] CMake generation failed.
    cd ..
    pause
    exit /b
)

REM 4. Build Release Configuration
echo [INFO] Compiling FraiIME.dll (Release)...
cmake --build . --config Release
if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    cd ..
    pause
    exit /b
)

echo.
echo [SUCCESS] Build Complete!
echo DLL Location: %CD%\Release\FraiIME.dll
cd ..
pause
