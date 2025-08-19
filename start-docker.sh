#!/bin/bash

# HARSHALADOBE Docker Startup Script
# This script automates the Docker setup and startup process

set -e

echo "🚀 HARSHALADOBE Docker Setup"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if Docker daemon is running
check_docker_daemon() {
    print_status "Checking Docker daemon..."
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    print_success "Docker daemon is running"
}

# Setup credentials directory
setup_credentials() {
    print_status "Setting up credentials directory..."
    
    if [ ! -d "credentials" ]; then
        mkdir -p credentials
        print_warning "Created credentials directory. Please add your adbe-gcp.json file to credentials/"
    else
        print_success "Credentials directory exists"
    fi
    
    if [ ! -f "credentials/adbe-gcp.json" ]; then
        print_warning "adbe-gcp.json not found in credentials directory"
        print_status "Please add your Google Cloud credentials file to credentials/adbe-gcp.json"
    else
        print_success "Google Cloud credentials found"
    fi
}

# Setup environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        if [ -f "env.template" ]; then
            cp env.template .env
            print_warning "Created .env file from template. Please edit .env with your actual values."
        else
            print_error "env.template not found. Please create a .env file manually."
            exit 1
        fi
    else
        print_success "Environment file exists"
    fi
}

# Check if ports are available
check_ports() {
    print_status "Checking port availability..."
    
    local ports=(3000 8000 8080)
    local ports_in_use=()
    
    for port in "${ports[@]}"; do
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            ports_in_use+=($port)
        fi
    done
    
    if [ ${#ports_in_use[@]} -ne 0 ]; then
        print_warning "The following ports are already in use: ${ports_in_use[*]}"
        print_status "Please stop the services using these ports or modify the docker-compose.yml file"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "All required ports are available"
    fi
}

# Build and start containers
start_containers() {
    print_status "Building and starting containers..."
    
    # Stop any existing containers
    docker-compose down 2>/dev/null || true
    
    # Build and start
    docker-compose up --build -d
    
    print_success "Containers started successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        print_status "Attempt $attempt/$max_attempts - Checking services..."
        
        # Check frontend
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend is ready"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            print_warning "Frontend is taking longer than expected to start"
            break
        fi
        
        sleep 2
        ((attempt++))
    done
    
    # Check backends
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        print_success "HARSHALADOBE Backend is ready"
    else
        print_warning "HARSHALADOBE Backend may still be starting"
    fi
    
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        print_success "AdobeV4 Backend is ready"
    else
        print_warning "AdobeV4 Backend may still be starting"
    fi
}

# Show status and URLs
show_status() {
    echo
    echo "🎉 HARSHALADOBE Application is running!"
    echo "========================================"
    echo
    echo "📱 Frontend:        http://localhost:3000"
    echo "🔧 HARSHALADOBE API: http://localhost:8000"
    echo "📚 API Docs:        http://localhost:8000/docs"
    echo "🔧 AdobeV4 API:     http://localhost:8080"
    echo
    echo "📋 Useful Commands:"
    echo "  View logs:        docker-compose logs -f"
    echo "  Stop services:    docker-compose down"
    echo "  Restart:          docker-compose restart"
    echo "  Container shell:  docker exec -it harshaladobe-full-stack bash"
    echo
}

# Main execution
main() {
    echo "Starting HARSHALADOBE Docker setup..."
    echo
    
    check_docker
    check_docker_daemon
    setup_credentials
    setup_environment
    check_ports
    start_containers
    wait_for_services
    show_status
}

# Handle script interruption
trap 'echo -e "\n${RED}Setup interrupted${NC}"; exit 1' INT

# Run main function
main "$@"
