@echo off
echo Starting Dual Backend System...
echo.

echo [1/4] Installing adobev4 dependencies...
cd ..\adobev4
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install adobev4 dependencies
    pause
    exit /b 1
)

echo [2/4] Starting adobev4 backend (port 8000)...
start "AdobeV4 Backend" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo [3/4] Installing HARSHALADOBE backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install HARSHALADOBE backend dependencies
    pause
    exit /b 1
)

echo [4/4] Starting HARSHALADOBE backend (port 8001)...
start "HARSHALADOBE Backend" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo Dual Backend System started successfully!
echo.
echo AdobeV4 Backend: http://localhost:8000
echo HARSHALADOBE Backend: http://localhost:8001
echo AdobeV4 API Docs: http://localhost:8000/docs
echo HARSHALADOBE API Docs: http://localhost:8001/docs
echo.
echo Press any key to close this window...
pause >nul
