@echo off
echo Starting Integrated Document Analysis System...
echo.

echo [1/3] Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install backend dependencies
    pause
    exit /b 1
)

echo [2/3] Starting backend server...
start "Backend Server" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo [3/3] Starting frontend development server...
cd ..
npm install
if %errorlevel% neq 0 (
    echo Error: Failed to install frontend dependencies
    pause
    exit /b 1
)

start "Frontend Server" cmd /k "npm run dev"

echo.
echo ========================================
echo System started successfully!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to close this window...
pause >nul
