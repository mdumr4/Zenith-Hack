@echo off
setlocal EnableDelayedExpansion
echo ==========================================
echo      Frai AI Keyboard - Build Script
echo ==========================================

REM 1. Find CMake
set CMAKE_EXE=cmake
where cmake >nul 2>nul
if %errorlevel% equ 0 goto CheckCompiler

echo [INFO] CMake not in PATH. Searching...
set "PATHS=C:\Program Files\CMake\bin\cmake.exe;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe;C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"

REM Use simple check loop
for %%p in ("%PATHS:;=" "%") do (
    if exist %%p (
        set CMAKE_EXE=%%p
        echo [INFO] Found CMake at: %%p
        goto CheckCompiler
    )
)
echo [ERROR] CMake not found. Install it first.
pause
exit /b

:CheckCompiler
REM 2. Setup VS Environment (vcvars64.bat)
where cl >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] MSVC Compiler cl.exe already in PATH.
    goto Build
)

echo [INFO] Searching for Visual Studio C++ Tools...
set "VARS_BATCH="

REM Check 64-bit locations first
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

REM Check x86 locations (Build Tools often land here)
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"

if not defined VARS_BATCH (
    echo [ERROR] Could not auto-detect Visual Studio 2022.
    echo Please open "x64 Native Tools Command Prompt" manually.
    pause
    exit /b
)

echo [INFO] Found tools: !VARS_BATCH!
echo [INFO] initializing environment...
call "!VARS_BATCH!" >nul

:Build
REM 3. Clean and Build
if exist "build" rmdir /s /q build
mkdir build
cd build

echo [INFO] Generating NMake Project...
"!CMAKE_EXE!" -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release ..
if %errorlevel% neq 0 (
    echo [ERROR] CMake Configuration failed.
    echo Ensure 'C++ CMake tools for Windows' is installed.
    cd ..
    pause
    exit /b
)

echo [INFO] Compiling...
"!CMAKE_EXE!" --build .
if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed.
    cd ..
    pause
    exit /b
)

echo.
echo [SUCCESS] Build Complete!
if not exist "Release" mkdir Release
copy FraiIME.dll Release\FraiIME.dll >nul
echo DLL Location: %CD%\Release\FraiIME.dll
cd ..
pause
