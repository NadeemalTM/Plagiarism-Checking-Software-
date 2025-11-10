@echo off
REM Quick Start Script for PDF Plagiarism Checker
REM This script helps you get started quickly

echo ===============================================
echo   PDF Plagiarism Checker - Quick Start
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

echo Python detected: 
python --version
echo.

REM Check if requirements are installed
echo Checking dependencies...
python -c "import PyPDF2" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Dependencies not found. Installing...
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    
    echo.
    echo Setting up NLTK data...
    python setup_nltk.py
) else (
    echo Dependencies already installed!
)

echo.
echo ===============================================
echo   Installation Complete!
echo ===============================================
echo.
echo Running system tests...
echo.

python test_system.py

if errorlevel 1 (
    echo.
    echo Some tests failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   Ready to Use!
echo ===============================================
echo.
echo Examples:
echo   1. Check a PDF file:
echo      python plagiarism_checker.py --file document.pdf
echo.
echo   2. Generate HTML report:
echo      python plagiarism_checker.py --file document.pdf --format html --output report.html
echo.
echo   3. Compare with references:
echo      python plagiarism_checker.py --file doc.pdf --references ref1.pdf ref2.pdf
echo.
echo For more examples, see EXAMPLES.md
echo.
pause
