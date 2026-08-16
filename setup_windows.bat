@echo off
REM Internet Manager - Windows Setup Script
REM This script sets up Internet Manager on Windows

title Internet Manager - Setup

echo.
echo ====================================================
echo Internet Manager - Windows Setup
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Show configuration instructions
echo.
echo ====================================================
echo Setup Complete!
echo ====================================================
echo.
echo Next steps:
echo 1. Edit main.py to configure your connections
echo 2. Run as Administrator:
echo    a. Open Command Prompt as Administrator
echo    b. Navigate to this folder
echo    c. Activate venv: venv\Scripts\activate
echo    d. Run: python main.py
echo.
echo For detailed setup instructions, see WINDOWS_SETUP.md
echo.
pause
