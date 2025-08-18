@echo off
echo Running API Tests...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if requests is installed
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing requests...
    pip install requests
)

REM Run the tests
echo.
echo Running tests...
python test_api.py

pause
