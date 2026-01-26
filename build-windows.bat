@echo off
REM Build script for creating a Windows executable of Drinkingbird
REM Requires Python and pip to be installed

echo ========================================
echo Drinkingbird Windows Build Script
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    exit /b 1
)

REM Create/activate virtual environment (optional but recommended)
if not exist "venv-build" (
    echo Creating virtual environment...
    python -m venv venv-build
)

echo Activating virtual environment...
call venv-build\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install --upgrade pip
pip install pynput>=1.7.6
pip install pyinstaller

REM Build the executable
echo.
echo Building Windows executable...
pyinstaller ^
    --onefile ^
    --name drinkingbird ^
    --console ^
    --clean ^
    --noconfirm ^
    --add-data "README.md;." ^
    drinkingbird.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    exit /b 1
)

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Executable location: dist\drinkingbird.exe
echo.
echo To distribute, copy dist\drinkingbird.exe to the target machine.
echo No Python installation required on the target machine.
echo.

REM Deactivate virtual environment
call venv-build\Scripts\deactivate.bat 2>nul

pause
