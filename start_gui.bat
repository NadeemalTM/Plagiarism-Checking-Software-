@echo off
REM Launcher for PDF Plagiarism Checker GUI
REM Double-click this file to start the application

echo ===============================================
echo   PDF Plagiarism Checker - GUI Launcher
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Starting GUI application...
echo.

REM Launch the GUI
python plagiarism_checker_gui.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
