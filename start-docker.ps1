# HARSHALADOBE Docker Setup PowerShell Script
# This script automates the Docker setup and startup process on Windows

param(
    [switch]$SkipChecks,
    [switch]$Force
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

Write-Host "🚀 HARSHALADOBE Docker Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
function Test-DockerInstallation {
    Write-Status "Checking Docker installation..."
    
    try {
        $dockerVersion = docker --version 2>$null
        if (-not $dockerVersion) {
            throw "Docker not found"
        }
        Write-Success "Docker is installed: $dockerVersion"
    }
    catch {
        Write-Error "Docker is not installed. Please install Docker Desktop first."
        exit 1
    }
    
    try {
        $composeVersion = docker-compose --version 2>$null
        if (-not $composeVersion) {
            throw "Docker Compose not found"
        }
        Write-Success "Docker Compose is installed: $composeVersion"
    }
    catch {
        Write-Error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    }
}

# Check if Docker daemon is running
function Test-DockerDaemon {
    Write-Status "Checking Docker daemon..."
    
    try {
        docker info 2>$null | Out-Null
        Write-Success "Docker daemon is running"
    }
    catch {
        Write-Error "Docker daemon is not running. Please start Docker Desktop first."
        exit 1
    }
}

# Setup credentials directory
function Setup-Credentials {
    Write-Status "Setting up credentials directory..."
    
    if (-not (Test-Path "credentials")) {
        New-Item -ItemType Directory -Path "credentials" | Out-Null
        Write-Warning "Created credentials directory. Please add your adbe-gcp.json file to credentials/"
    }
    else {
        Write-Success "Credentials directory exists"
    }
    
    if (-not (Test-Path "credentials\adbe-gcp.json")) {
        Write-Warning "adbe-gcp.json not found in credentials directory"
        Write-Status "Please add your Google Cloud credentials file to credentials\adbe-gcp.json"
    }
    else {
        Write-Success "Google Cloud credentials found"
    }
}

# Setup environment file
function Setup-Environment {
    Write-Status "Setting up environment configuration..."
    
    if (-not (Test-Path ".env")) {
        if (Test-Path "env.template") {
            Copy-Item "env.template" ".env"
            Write-Warning "Created .env file from template. Please edit .env with your actual values."
        }
        else {
            Write-Error "env.template not found. Please create a .env file manually."
            exit 1
        }
    }
    else {
        Write-Success "Environment file exists"
    }
}

# Check if ports are available
function Test-Ports {
    Write-Status "Checking port availability..."
    
    $ports = @(3000, 8000, 8080)
    $portsInUse = @()
    
    foreach ($port in $ports) {
        $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        if ($connection) {
            $portsInUse += $port
            Write-Warning "Port $port is already in use"
        }
    }
    
    if ($portsInUse.Count -gt 0) {
        Write-Warning "The following ports are already in use: $($portsInUse -join ', ')"
        Write-Status "Please stop the services using these ports or modify the docker-compose.yml file"
        
        if (-not $Force) {
            $continue = Read-Host "Continue anyway? (y/N)"
            if ($continue -ne "y" -and $continue -ne "Y") {
                exit 1
            }
        }
    }
    else {
        Write-Success "All required ports are available"
    }
}

# Build and start containers
function Start-Containers {
    Write-Status "Building and starting containers..."
    
    # Stop any existing containers
    try {
        docker-compose down 2>$null | Out-Null
    }
    catch {
        # Ignore errors if no containers are running
    }
    
    # Build and start
    try {
        docker-compose up --build -d
        Write-Success "Containers started successfully"
    }
    catch {
        Write-Error "Failed to start containers"
        exit 1
    }
}

# Wait for services to be ready
function Wait-ForServices {
    Write-Status "Waiting for services to be ready..."
    
    $maxAttempts = 30
    $attempt = 1
    
    while ($attempt -le $maxAttempts) {
        Write-Status "Attempt $attempt/$maxAttempts - Checking services..."
        
        # Check frontend
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "Frontend is ready"
                break
            }
        }
        catch {
            # Continue waiting
        }
        
        if ($attempt -eq $maxAttempts) {
            Write-Warning "Frontend is taking longer than expected to start"
            break
        }
        
        Start-Sleep -Seconds 2
        $attempt++
    }
    
    # Check backends
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Success "HARSHALADOBE Backend is ready"
        }
    }
    catch {
        Write-Warning "HARSHALADOBE Backend may still be starting"
    }
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Success "AdobeV4 Backend is ready"
        }
    }
    catch {
        Write-Warning "AdobeV4 Backend may still be starting"
    }
}

# Show status and URLs
function Show-Status {
    Write-Host ""
    Write-Host "🎉 HARSHALADOBE Application is running!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Frontend:        http://localhost:3000" -ForegroundColor Cyan
    Write-Host "🔧 HARSHALADOBE API: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "📚 API Docs:        http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "🔧 AdobeV4 API:     http://localhost:8080" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Useful Commands:" -ForegroundColor Yellow
    Write-Host "  View logs:        docker-compose logs -f" -ForegroundColor White
    Write-Host "  Stop services:    docker-compose down" -ForegroundColor White
    Write-Host "  Restart:          docker-compose restart" -ForegroundColor White
    Write-Host "  Container shell:  docker exec -it harshaladobe-full-stack bash" -ForegroundColor White
    Write-Host ""
}

# Main execution
function Main {
    Write-Host "Starting HARSHALADOBE Docker setup..." -ForegroundColor Cyan
    Write-Host ""
    
    if (-not $SkipChecks) {
        Test-DockerInstallation
        Test-DockerDaemon
        Setup-Credentials
        Setup-Environment
        Test-Ports
    }
    
    Start-Containers
    Wait-ForServices
    Show-Status
}

# Run main function
try {
    Main
}
catch {
    Write-Error "Setup failed: $($_.Exception.Message)"
    exit 1
}
