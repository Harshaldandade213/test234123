# Adobe+ PDF Reader & Podcast Generator

A modern, AI-powered PDF reading application with podcast generation capabilities, built with React, FastAPI, and Docker.

## 🚀 Quick Start with Docker

### Prerequisites

- Docker installed on your system
- Git for cloning the repository
- Valid API keys for the services

### 1. Clone the Repository

```bash
# Clone the repository and switch to the harshal branch
git clone <your-repo-url>
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory with your API keys:

```env
# Adobe Embed API Key (Required)
ADOBE_EMBED_API_KEY=a2d7f06cea0c43f09a17bea4c32c9e93

# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# Azure Speech Services
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here

# AWS Credentials (Alternative TTS)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```

### 3. Run with Docker

Use the following command to run the application:

```bash
docker run \
  -v /path/to/credentials:/credentials \
  -e ADOBE_EMBED_API_KEY=a2d7f06cea0c43f09a17bea4c32c9e93 \
  -e LLM_PROVIDER=gemini \
  -e GOOGLE_APPLICATION_CREDENTIALS=/credentials/adbe-gcp.json \
  -e GEMINI_MODEL=gemini-2.5-flash \
  -e TTS_PROVIDER=azure \
  -e AZURE_TTS_KEY=your_azure_tts_key \
  -e AZURE_TTS_ENDPOINT=your_azure_tts_endpoint \
  -p 8080:8080 \
  yourimageidentifier
```

### 4. Alternative: Docker Compose (Recommended)

For easier management, use Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

## 🏗️ Architecture

The application consists of three main components:

### Frontend (React + Vite)
- **Port**: 5173 (dev) / 3000 (Docker)
- **Features**: Modern UI with PDF viewer, tool selection, and podcast generation
- **Tech Stack**: React, TypeScript, Tailwind CSS, Shadcn/ui

### AdobeV4 Backend (FastAPI)
- **Port**: 8080
- **Features**: PDF processing, AI insights, podcast generation
- **Tech Stack**: FastAPI, Python, Gemini AI, Azure TTS

### HARSHALADOBE Backend (FastAPI)
- **Port**: 8001
- **Features**: Document analysis, additional AI services
- **Tech Stack**: FastAPI, Python, Machine Learning

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ADOBE_EMBED_API_KEY` | Adobe Embed API Key | ✅ | `a2d7f06cea0c43f09a17bea4c32c9e93` |
| `GOOGLE_API_KEY` | Google Gemini API Key | ✅ | - |
| `AZURE_SPEECH_KEY` | Azure Speech Services Key | ✅ | - |
| `AZURE_SPEECH_REGION` | Azure Region | ✅ | - |
| `TTS_PROVIDER` | Text-to-Speech Provider | ❌ | `azure` |
| `LLM_PROVIDER` | Language Model Provider | ❌ | `gemini` |
| `GEMINI_MODEL` | Gemini Model Version | ❌ | `gemini-2.5-flash` |

### Volume Mounts

- `/path/to/credentials:/credentials` - Mount credentials directory
- `./adobev4/audio:/app/adobev4-backend/audio` - Audio files storage
- `./adobev4/documents:/app/adobev4-backend/documents` - PDF documents
- `./adobev4/index:/app/adobev4-backend/index` - Search indexes

## 🌐 Access Points

After running the application:

- **Frontend**: http://localhost:3000 (Docker) or http://localhost:5173 (dev)
- **AdobeV4 Backend**: http://localhost:8080
- **HARSHALADOBE Backend**: http://localhost:8001
- **Health Check**: http://localhost:8080/health

## 📚 Features

### PDF Reading
- Upload and view PDF documents
- Intelligent text extraction
- Document search and navigation
- Multiple viewing modes

### AI-Powered Insights
- Custom query analysis
- Document summarization
- Key insights extraction
- Strategic analysis

### Podcast Generation
- Generate podcasts from PDF content
- Custom query-based podcast creation
- Multiple TTS providers (Azure, AWS Polly)
- Audio file export

### Tool Integration
- Floating tool panel
- Quick access to features
- Keyboard shortcuts
- Responsive design

## 🛠️ Development

### Manual Setup (Alternative to Docker)

```bash
# Frontend
cd HARSHALADOBE
npm install
npm run dev

# AdobeV4 Backend
cd adobev4
pip install -r requirements.txt
python run_server.py

# HARSHALADOBE Backend
cd HARSHALADOBE/backend
pip install -r requirements.txt
python main.py
```

### API Endpoints

#### AdobeV4 Backend
- `POST /upload` - Upload PDF documents
- `POST /api/v1/insights` - Generate AI insights
- `POST /podcast/generate` - Generate podcasts
- `GET /health` - Health check

#### HARSHALADOBE Backend
- `POST /analyze-documents` - Document analysis
- `GET /documents` - List documents
- `POST /search-documents` - Search documents

## 🔍 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using the ports
   netstat -an | findstr :8080
   netstat -an | findstr :3000
   
   # Kill processes if needed
   taskkill /f /im python.exe
   taskkill /f /im node.exe
   ```

2. **API Key Issues**
   - Ensure all API keys are valid and have sufficient quota
   - Check environment variables are properly set
   - Verify credentials file path in Docker run command

3. **Docker Build Failures**
   ```bash
   # Clean Docker cache
   docker system prune -f
   docker volume prune -f
   
   # Rebuild without cache
   docker-compose build --no-cache
   ```

4. **Frontend Not Loading**
   - Check if Vite is running on correct port
   - Verify Docker port mappings
   - Check browser console for errors

### Health Checks

```bash
# Test backend health
curl http://localhost:8080/health

# Test frontend
curl http://localhost:3000

# Check Docker containers
docker-compose ps
docker-compose logs
```

## 📝 API Documentation

### Generate Insights
```bash
curl -X POST http://localhost:8080/api/v1/insights \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main points?",
    "passages": [
      {"id": "1", "text": "Sample passage text..."}
    ]
  }'
```

### Generate Podcast
```bash
curl -X POST http://localhost:8080/podcast/generate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Create a podcast about AI trends"
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit: `git commit -m 'Add feature'`
5. Push: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs: `docker-compose logs`
3. Create an issue on GitHub
4. Contact the development team

---

**Note**: Make sure to pull the `harshal` branch from the GitHub repository before running the application:

```bash
git checkout harshal
```

The application requires the Adobe Embed API key: `a2d7f06cea0c43f09a17bea4c32c9e93`
