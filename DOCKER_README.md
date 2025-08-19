# HARSHALADOBE Docker Setup

This document provides instructions for running the complete HARSHALADOBE application using Docker.

## 🏗️ Architecture

The application consists of:
- **Frontend**: React + Vite application (Port 3000)
- **HARSHALADOBE Backend**: FastAPI backend (Port 8000)
- **AdobeV4 Backend**: Additional backend service (Port 8080)

## 📋 Prerequisites

1. **Docker** and **Docker Compose** installed
2. **Credentials directory** with required files
3. **Environment variables** configured

## 🚀 Quick Start

### 1. Setup Credentials Directory

Create a `credentials` directory in the project root and add your credentials:

```bash
mkdir credentials
# Add your adbe-gcp.json file to credentials/
```

### 2. Configure Environment Variables

Copy the environment template and configure your variables:

```bash
cp env.template .env
# Edit .env with your actual values
```

Required environment variables:
- `ADOBE_EMBED_API_KEY`: Your Adobe Embed API key
- `GEMINI_API_KEY`: Your Gemini API key (already configured)
- `AZURE_TTS_KEY`: Your Azure TTS key
- `AZURE_TTS_ENDPOINT`: Your Azure TTS endpoint
- `AZURE_SPEECH_KEY`: Your Azure Speech key (already configured)
- `AZURE_SPEECH_REGION`: Your Azure Speech region (already configured)
- `ADOBE_CLIENT_ID`: Your Adobe Client ID (already configured)

### 3. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Access the Application

Once running, access the application at:
- **Frontend**: http://localhost:3000
- **HARSHALADOBE Backend API**: http://localhost:8000
- **AdobeV4 Backend API**: http://localhost:8080
- **API Documentation**: http://localhost:8000/docs

## 🔧 Manual Docker Commands

### Build the Image

```bash
docker build -t harshaladobe-app .
```

### Run with Custom Configuration

```bash
docker run -d \
  --name harshaladobe-full-stack \
  -v $(pwd)/credentials:/credentials:ro \
  -e ADOBE_EMBED_API_KEY=your_key \
  -e LLM_PROVIDER=gemini \
  -e GOOGLE_APPLICATION_CREDENTIALS=/credentials/adbe-gcp.json \
  -e GEMINI_MODEL=gemini-2.5-flash \
  -e GEMINI_API_KEY=AIzaSyAInqw9seke43AUqjjPA8ftJcJVggRKA6c \
  -e TTS_PROVIDER=azure \
  -e AZURE_TTS_KEY=your_tts_key \
  -e AZURE_TTS_ENDPOINT=your_tts_endpoint \
  -p 3000:3000 \
  -p 8000:8000 \
  -p 8080:8080 \
  harshaladobe-app
```

## 📁 Directory Structure

```
harshaladobe/
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Docker Compose configuration
├── .dockerignore             # Docker build exclusions
├── env.template              # Environment variables template
├── credentials/              # Credentials directory (mounted)
│   └── adbe-gcp.json        # Google Cloud credentials
├── HARSHALADOBE/            # Frontend and HARSHALADOBE backend
│   ├── src/                 # Frontend source
│   ├── backend/             # HARSHALADOBE backend
│   └── package.json         # Frontend dependencies
└── adobev4/                 # AdobeV4 backend
    ├── app.py               # Main application
    └── requirements.txt     # Python dependencies
```

## 🔍 Monitoring and Logs

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs harshaladobe-app

# Follow logs in real-time
docker-compose logs -f
```

### Health Checks

The application includes health checks that monitor:
- Frontend availability (http://localhost:3000)
- Backend services status

### Container Status

```bash
# Check running containers
docker-compose ps

# Check container health
docker inspect harshaladobe-full-stack
```

## 🛠️ Development

### Rebuild After Changes

```bash
# Rebuild and restart
docker-compose up --build

# Rebuild specific service
docker-compose build harshaladobe-app
```

### Access Container Shell

```bash
# Access running container
docker exec -it harshaladobe-full-stack bash

# Run commands in container
docker exec -it harshaladobe-full-stack python --version
```

## 🧹 Cleanup

### Stop and Remove

```bash
# Stop services
docker-compose down

# Remove volumes (data will be lost)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Clean Docker System

```bash
# Remove unused containers, networks, images
docker system prune

# Remove everything (use with caution)
docker system prune -a
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the ports
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :8080
   ```

2. **Permission Issues with Credentials**
   ```bash
   # Ensure credentials directory has correct permissions
   chmod 600 credentials/adbe-gcp.json
   ```

3. **Environment Variables Not Loading**
   ```bash
   # Check if .env file exists and has correct format
   cat .env
   ```

4. **Container Won't Start**
   ```bash
   # Check container logs
   docker-compose logs harshaladobe-app
   
   # Check container status
   docker-compose ps
   ```

### Debug Mode

Run with debug output:

```bash
docker-compose up --build --verbose
```

## 📊 Performance

### Resource Usage

Monitor resource usage:

```bash
# Container resource usage
docker stats harshaladobe-full-stack

# System resource usage
docker system df
```

### Optimization

- Use `.dockerignore` to reduce build context
- Multi-stage builds reduce final image size
- Volume mounts for persistent data
- Health checks for monitoring

## 🔐 Security

### Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Mount credentials as read-only** volumes
4. **Regular security updates** for base images
5. **Scan images** for vulnerabilities

### Credential Management

```bash
# Secure credential storage
chmod 700 credentials/
chmod 600 credentials/adbe-gcp.json
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review container logs
3. Verify environment configuration
4. Ensure all prerequisites are met

## 🚀 Production Deployment

For production deployment:
1. Use proper secrets management
2. Configure reverse proxy (nginx)
3. Set up SSL/TLS certificates
4. Configure monitoring and logging
5. Set up backup strategies
6. Use container orchestration (Kubernetes)
