@echo off
REM Restaurant Order Management System - Windows Launcher
REM This batch file provides an easy way to start the application on Windows

title Restaurant Order Management System

echo ============================================================
echo Restaurant Order Management System
echo Version 1.0.0
echo ============================================================
echo.

REM Check if Python is installed and accessible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    echo.
    echo Download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Starting Restaurant Management System...
echo Please wait while the application loads...
echo.

REM Run the application
python run_restaurant_system.py

if %errorlevel% neq 0 (
    echo.
    echo Application exited with an error.
    echo Please check the log files for more information.
    pause
)

echo.
echo Thank you for using Restaurant Order Management System!
pause