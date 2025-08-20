# Adobe+ Docker Setup

This Docker Compose setup provides a complete containerized environment for the Adobe+ application with frontend and backend services.

## 🏗️ Architecture

- **Frontend**: React application running on port 3000
- **Backend**: AdobeV4 Python FastAPI service running on port 8080
- **Network**: Custom bridge network for service communication
- **Volumes**: Persistent storage for audio, documents, and index files

## 📋 Prerequisites

- Docker Desktop installed and running
- Docker Compose installed
- API keys for Google and Azure services

## 🚀 Quick Start

### 1. Setup Environment

**Windows:**
```bash
setup-docker.bat
```

**Linux/Mac:**
```bash
chmod +x setup-docker.sh
./setup-docker.sh
```

### 2. Configure API Keys

Edit the `.env` file and add your API keys:

```env
# Google API Configuration
GOOGLE_API_KEY=your_actual_google_api_key

# Azure Speech Services Configuration
AZURE_SPEECH_KEY=your_actual_azure_speech_key
AZURE_SPEECH_REGION=your_azure_region

# Optional: AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```

### 3. Build and Run

```bash
docker-compose up --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8080
- **Health Check**: http://localhost:8080/health

## 📁 Project Structure

```
.
├── docker-compose.yml          # Main Docker Compose configuration
├── .dockerignore              # Files to exclude from Docker builds
├── env.template               # Environment variables template
├── setup-docker.sh            # Linux/Mac setup script
├── setup-docker.bat           # Windows setup script
├── HARSHALADOBE/
│   ├── Dockerfile             # Frontend Docker configuration
│   └── ...                    # React application files
└── adobev4/
    ├── Dockerfile             # Backend Docker configuration
    ├── requirements.txt       # Python dependencies
    └── ...                    # Python backend files
```

## 🔧 Services

### Frontend Service
- **Port**: 3000
- **Technology**: React + Vite
- **Health Check**: HTTP GET http://localhost:3000
- **Dependencies**: Waits for backend to be healthy

### AdobeV4 Backend Service
- **Port**: 8080
- **Technology**: Python FastAPI
- **Health Check**: HTTP GET http://localhost:8080/health
- **Volumes**:
  - `./adobev4/audio` → `/app/adobev4-backend/audio`
  - `./adobev4/documents` → `/app/adobev4-backend/documents`
  - `./adobev4/index` → `/app/adobev4-backend/index`

## 🌐 Network Configuration

- **Network Name**: `adobe-network`
- **Type**: Bridge network
- **Services**: frontend, adobev4-backend

## 📊 Health Checks

Both services include health checks that verify:
- Service is responding on the correct port
- Application is healthy and ready to serve requests
- Automatic restart on failure

## 🔄 Environment Variables

### Frontend
- `VITE_ADOBEV4_URL`: Backend API URL (http://localhost:8080)

### Backend
- `GOOGLE_API_KEY`: Google API key for AI services
- `AZURE_SPEECH_KEY`: Azure Speech Services key
- `AZURE_SPEECH_REGION`: Azure region
- `TTS_PROVIDER`: Text-to-speech provider (azure)
- `HOST`: Server host (0.0.0.0)
- `PORT`: Server port (8080)
- `DEBUG`: Debug mode (true)
- `DEVELOPMENT_MODE`: Development mode (true)
- `VERBOSE_LOGGING`: Verbose logging (false)

## 🛠️ Useful Commands

### Basic Operations
```bash
# Build and start services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs frontend
docker-compose logs adobev4-backend

# Check service status
docker-compose ps

# Restart services
docker-compose restart
```

### Development
```bash
# Rebuild specific service
docker-compose build frontend
docker-compose build adobev4-backend

# Execute commands in running containers
docker-compose exec frontend sh
docker-compose exec adobev4-backend bash

# View resource usage
docker-compose top
```

### Troubleshooting
```bash
# Remove all containers and volumes
docker-compose down -v

# Remove all images and rebuild
docker-compose down --rmi all
docker-compose up --build

# Check Docker system info
docker system df
docker system prune
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the ports
   netstat -an | grep :3000
   netstat -an | grep :8080
   
   # Stop conflicting services
   docker-compose down
   ```

2. **API Key Issues**
   - Verify `.env` file exists and contains valid API keys
   - Check backend logs: `docker-compose logs adobev4-backend`

3. **Build Failures**
   ```bash
   # Clean build
   docker-compose down --rmi all
   docker-compose up --build --force-recreate
   ```

4. **Health Check Failures**
   - Check if services are starting correctly
   - Verify ports are accessible
   - Check application logs

### Log Analysis
```bash
# Follow logs in real-time
docker-compose logs -f

# Filter logs by service
docker-compose logs -f adobev4-backend

# Search for errors
docker-compose logs | grep -i error
```

## 📈 Monitoring

### Health Status
```bash
# Check health status
docker-compose ps

# Manual health check
curl http://localhost:3000
curl http://localhost:8080/health
```

### Resource Usage
```bash
# View resource usage
docker stats

# View container details
docker-compose top
```

## 🔒 Security Considerations

- API keys are stored in `.env` file (keep this secure)
- Services run in isolated containers
- Network communication is restricted to the custom bridge network
- Health checks help ensure service availability

## 📝 Notes

- The HARSHALADOBE backend (port 8000) is **NOT** included in this setup
- All persistent data is stored in mounted volumes
- Services automatically restart on failure
- Health checks ensure service availability before marking as ready

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs`
3. Verify environment configuration
4. Ensure Docker Desktop is running
5. Check API key validity and permissions
