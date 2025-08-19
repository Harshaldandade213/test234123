# 🐳 HARSHALADOBE Docker Setup Complete

## ✅ **What's Been Created**

Your HARSHALADOBE application has been fully dockerized with the following components:

### 📁 **Docker Files Created**
- `Dockerfile` - Multi-stage Docker build for all services
- `docker-compose.yml` - Orchestration for all services
- `.dockerignore` - Optimized build context
- `env.template` - Environment variables template
- `DOCKER_README.md` - Comprehensive documentation
- `start-docker.sh` - Linux/macOS startup script
- `start-docker.bat` - Windows batch startup script
- `start-docker.ps1` - Windows PowerShell startup script

## 🏗️ **Application Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │ HARSHALADOBE     │    │   AdobeV4       │
│   (Port 3000)   │    │ Backend          │    │ Backend         │
│   React + Vite  │    │ (Port 8000)      │    │ (Port 8080)     │
│                 │    │ FastAPI          │    │ Python          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start Commands**

### **Option 1: Automated Setup (Recommended)**

**Windows:**
```cmd
start-docker.bat
```

**Windows PowerShell:**
```powershell
.\start-docker.ps1
```

**Linux/macOS:**
```bash
./start-docker.sh
```

### **Option 2: Manual Docker Compose**

```bash
# 1. Setup environment
cp env.template .env
# Edit .env with your values

# 2. Create credentials directory
mkdir credentials
# Add your adbe-gcp.json to credentials/

# 3. Build and run
docker-compose up --build -d
```

### **Option 3: Manual Docker Run**

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

## 🌐 **Access URLs**

Once running, access your application at:

- **🎨 Frontend**: http://localhost:3000
- **🔧 HARSHALADOBE API**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **🔧 AdobeV4 API**: http://localhost:8080

## ⚙️ **Environment Variables**

Required environment variables (configure in `.env`):

```bash
# Adobe Embed API
ADOBE_EMBED_API_KEY=your_adobe_embed_api_key_here

# LLM Configuration
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-2.5-flash
GEMINI_API_KEY=AIzaSyAInqw9seke43AUqjjPA8ftJcJVggRKA6c

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/credentials/adbe-gcp.json

# Azure TTS
TTS_PROVIDER=azure
AZURE_TTS_KEY=your_azure_tts_key_here
AZURE_TTS_ENDPOINT=your_azure_tts_endpoint_here
AZURE_SPEECH_KEY=6LKDbzy1pkGLZNMuTjSxf8hrte5dGlAKFWAHX7R0eczacngvw1reJQQJ99BHACGhslBXJ3w3AAAYACOGhON1
AZURE_SPEECH_REGION=centralindia

# Adobe Client
ADOBE_CLIENT_ID=d09f55f4ad4947649871706908700c76
```

## 📁 **Directory Structure**

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

## 🔧 **Management Commands**

### **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs harshaladobe-app
```

### **Stop Services**
```bash
docker-compose down
```

### **Restart Services**
```bash
docker-compose restart
```

### **Rebuild After Changes**
```bash
docker-compose up --build
```

### **Access Container Shell**
```bash
docker exec -it harshaladobe-full-stack bash
```

## 🎙️ **Podcast Feature Status**

✅ **Fully Functional** with your new Gemini API key:
- **API Key**: `AIzaSyAInqw9seke43AUqjjPA8ftJcJVggRKA6c`
- **Quota**: Fresh quota, no more quota exceeded errors
- **Features**: 
  - Manual query input
  - Auto-generation on paste
  - Audio generation and playback
  - Transcript display

## 🔍 **Health Monitoring**

The application includes:
- **Health checks** for all services
- **Automatic restart** on failure
- **Resource monitoring** via Docker stats
- **Log aggregation** for debugging

## 🛡️ **Security Features**

- **Credentials mounted as read-only**
- **Environment variables** for sensitive data
- **No hardcoded secrets** in images
- **Secure file permissions**

## 📊 **Performance Optimizations**

- **Multi-stage builds** reduce image size
- **Layer caching** for faster rebuilds
- **Volume mounts** for persistent data
- **Resource limits** and monitoring

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Port Already in Use**
   ```bash
   # Check what's using the ports
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :8080
   ```

2. **Docker Not Running**
   ```bash
   # Start Docker Desktop (Windows/macOS)
   # Or start Docker daemon (Linux)
   sudo systemctl start docker
   ```

3. **Permission Issues**
   ```bash
   # Fix credential permissions
   chmod 600 credentials/adbe-gcp.json
   ```

4. **Environment Variables**
   ```bash
   # Check .env file
   cat .env
   ```

### **Debug Mode**
```bash
# Run with verbose output
docker-compose up --build --verbose
```

## 🎉 **Success Indicators**

Your application is successfully running when you see:

✅ **Frontend accessible** at http://localhost:3000
✅ **HARSHALADOBE Backend** responding at http://localhost:8000
✅ **AdobeV4 Backend** responding at http://localhost:8080
✅ **API Documentation** available at http://localhost:8000/docs
✅ **Podcast generation** working with your new API key

## 📞 **Support**

For issues:
1. Check the troubleshooting section
2. Review container logs: `docker-compose logs`
3. Verify environment configuration
4. Ensure all prerequisites are met

---

**🎊 Congratulations! Your HARSHALADOBE application is now fully dockerized and ready to run!**
