@echo off
setlocal
echo ==========================================
echo      Frai AI Keyboard - Build Script
echo ==========================================

REM 1. Find CMake
set CMAKE_EXE=cmake
where cmake >nul 2>nul
if %errorlevel% equ 0 goto CheckCompiler

echo [INFO] CMake not in PATH. Searching...
set "PATHS=C:\Program Files\CMake\bin\cmake.exe;C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe;C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe;C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
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
REM 2. Setup VS Environment (vcvars64.bat) if 'cl.exe' is not found
where cl >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] MSVC Compiler cl.exe already in PATH.
    goto Build
)

echo [INFO] Searching for Visual Studio C++ Tools (vcvars64.bat)...
set "VARS_BATCH="
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if exist "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" set "VARS_BATCH=C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if defined VARS_BATCH (
    echo [INFO] Found tools: %VARS_BATCH%
    echo [INFO] initializing environment...
    call "%VARS_BATCH%" >nul
) else (
    echo [ERROR] Could not auto-detect Visual Studio 2022.
    echo ---------------------------------------------------------------------
    echo SOLUTION: Open "x64 Native Tools Command Prompt for VS 2022"
    echo and run this script from there.
    echo ---------------------------------------------------------------------
    pause
    exit /b
)

:Build
REM 3. Clean and Build using NMake (Reliable with active environment)
if exist "build" rmdir /s /q build
mkdir build
cd build

echo [INFO] Generating NMake Project...
"%CMAKE_EXE%" -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release ..
if %errorlevel% neq 0 (
    echo [ERROR] CMake Configuration failed.
    echo Ensure 'C++ CMake tools for Windows' is installed in VS Installer.
    cd ..
    pause
    exit /b
)

echo [INFO] Compiling...
"%CMAKE_EXE%" --build .
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
