@echo off
REM Internet Manager - Windows Runner (Run as Administrator)
REM This script runs Internet Manager with elevated privileges

title Internet Manager

echo.
echo ====================================================
echo Internet Manager - Windows
echo ====================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo [WARNING] This script should run as Administrator for route switching
    echo.
    echo To run as Administrator:
    echo 1. Right-click this file
    echo 2. Select "Run as administrator"
    echo.
    timeout /t 3
)

REM Activate virtual environment
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_windows.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Run the application
echo Starting Internet Manager...
echo Press Ctrl+C to stop
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] Internet Manager exited with an error
    pause
)
