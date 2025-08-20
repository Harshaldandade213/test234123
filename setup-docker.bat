@echo off
echo 🚀 Setting up Adobe+ Docker Environment
echo ========================================

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.template .env
    echo ✅ .env file created! Please edit it with your API keys:
    echo    - GOOGLE_API_KEY
    echo    - AZURE_SPEECH_KEY
    echo    - AZURE_SPEECH_REGION
    echo.
    echo ⚠️  IMPORTANT: Update the .env file with your actual API keys before running docker-compose!
    echo.
) else (
    echo ✅ .env file already exists
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

echo 🐳 Docker is running

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ docker-compose is not installed. Please install it and try again.
    pause
    exit /b 1
)

echo ✅ docker-compose is available

echo.
echo 🎯 Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: docker-compose up --build
echo 3. Access frontend at: http://localhost:3000
echo 4. Access backend at: http://localhost:8080
echo.
echo 📚 Useful commands:
echo    docker-compose up --build    # Build and start services
echo    docker-compose down          # Stop services
echo    docker-compose logs          # View logs
echo    docker-compose ps            # Check service status
echo.
pause
