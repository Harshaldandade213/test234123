@echo off
setlocal enabledelayedexpansion

echo 🚀 HARSHALADOBE Docker Setup
echo ================================
echo.

:: Check if Docker is installed
echo [INFO] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [SUCCESS] Docker and Docker Compose are installed

:: Check if Docker daemon is running
echo [INFO] Checking Docker daemon...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker daemon is not running. Please start Docker first.
    pause
    exit /b 1
)
echo [SUCCESS] Docker daemon is running

:: Setup credentials directory
echo [INFO] Setting up credentials directory...
if not exist "credentials" (
    mkdir credentials
    echo [WARNING] Created credentials directory. Please add your adbe-gcp.json file to credentials/
) else (
    echo [SUCCESS] Credentials directory exists
)

if not exist "credentials\adbe-gcp.json" (
    echo [WARNING] adbe-gcp.json not found in credentials directory
    echo [INFO] Please add your Google Cloud credentials file to credentials\adbe-gcp.json
) else (
    echo [SUCCESS] Google Cloud credentials found
)

:: Setup environment file
echo [INFO] Setting up environment configuration...
if not exist ".env" (
    if exist "env.template" (
        copy env.template .env >nul
        echo [WARNING] Created .env file from template. Please edit .env with your actual values.
    ) else (
        echo [ERROR] env.template not found. Please create a .env file manually.
        pause
        exit /b 1
    )
) else (
    echo [SUCCESS] Environment file exists
)

:: Check if ports are available
echo [INFO] Checking port availability...
set ports_in_use=0

netstat -an | findstr ":3000 " >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 3000 is already in use
    set /a ports_in_use+=1
)

netstat -an | findstr ":8000 " >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 8000 is already in use
    set /a ports_in_use+=1
)

netstat -an | findstr ":8080 " >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 8080 is already in use
    set /a ports_in_use+=1
)

if %ports_in_use% gtr 0 (
    echo [WARNING] Some ports are already in use
    echo [INFO] Please stop the services using these ports or modify the docker-compose.yml file
    set /p continue="Continue anyway? (y/N): "
    if /i not "!continue!"=="y" (
        pause
        exit /b 1
    )
) else (
    echo [SUCCESS] All required ports are available
)

:: Build and start containers
echo [INFO] Building and starting containers...

:: Stop any existing containers
docker-compose down >nul 2>&1

:: Build and start
docker-compose up --build -d

if errorlevel 1 (
    echo [ERROR] Failed to start containers
    pause
    exit /b 1
)

echo [SUCCESS] Containers started successfully

:: Wait for services to be ready
echo [INFO] Waiting for services to be ready...
set max_attempts=30
set attempt=1

:wait_loop
echo [INFO] Attempt %attempt%/%max_attempts% - Checking services...

:: Check frontend
curl -s http://localhost:3000 >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Frontend is ready
    goto check_backends
)

if %attempt% equ %max_attempts% (
    echo [WARNING] Frontend is taking longer than expected to start
    goto check_backends
)

timeout /t 2 /nobreak >nul
set /a attempt+=1
goto wait_loop

:check_backends
:: Check HARSHALADOBE backend
curl -s http://localhost:8000/docs >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] HARSHALADOBE Backend is ready
) else (
    echo [WARNING] HARSHALADOBE Backend may still be starting
)

:: Check AdobeV4 backend
curl -s http://localhost:8080 >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] AdobeV4 Backend is ready
) else (
    echo [WARNING] AdobeV4 Backend may still be starting
)

:: Show status and URLs
echo.
echo 🎉 HARSHALADOBE Application is running!
echo ========================================
echo.
echo 📱 Frontend:        http://localhost:3000
echo 🔧 HARSHALADOBE API: http://localhost:8000
echo 📚 API Docs:        http://localhost:8000/docs
echo 🔧 AdobeV4 API:     http://localhost:8080
echo.
echo 📋 Useful Commands:
echo   View logs:        docker-compose logs -f
echo   Stop services:    docker-compose down
echo   Restart:          docker-compose restart
echo   Container shell:  docker exec -it harshaladobe-full-stack bash
echo.

pause
