# Document Analysis & Podcast Generation System

## 🎯 Overview

This is a comprehensive document analysis and podcast generation system that combines:

- **Backend**: FastAPI server with `app.py` core functionality
- **Frontend**: React + TypeScript + Tailwind CSS interface
- **AI Integration**: Google Gemini AI for analysis and insights
- **Audio Generation**: AWS Polly for text-to-speech podcast creation

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)

**Windows:**
```bash
# Double-click or run in command prompt
start-integrated.bat

# Or PowerShell
.\start-integrated.ps1
```

**Manual Startup:**
```bash
# Terminal 1: Start Backend
cd HARSHALADOBE/backend
pip install -r requirements.txt
python main.py

# Terminal 2: Start Frontend
cd HARSHALADOBE
npm install
npm run dev
```

## 📁 System Architecture

```
HARSHALADOBE/
├── backend/                 # FastAPI Backend
│   ├── main.py             # API endpoints using app.py
│   ├── requirements.txt    # Python dependencies
│   └── documents/          # Uploaded documents
├── src/                    # React Frontend
│   ├── components/         # UI components
│   ├── pages/             # Page components
│   ├── lib/               # API integration
│   └── hooks/             # Custom React hooks
└── start-integrated.bat   # Startup script
```

## 🔧 Backend Features (app.py Integration)

### Document Processing
- **PDF, DOCX, TXT** file support
- **Semantic chunking** for better search
- **FAISS vector indexing** for fast retrieval

### AI-Powered Analysis
- **Google Gemini AI** integration
- **Semantic search** across documents
- **Document categorization** (Agreement/Conflict/Examples)
- **Insight generation** with persona context

### Podcast Generation
- **Conversational scripts** (Alex & Dr. Sharma personas)
- **AWS Polly TTS** for audio generation
- **Multi-speaker audio** with different voices
- **Audio file management** and playback

## 🎨 Frontend Features

### Document Management
- **Drag & drop** file upload
- **Document library** with search
- **PDF viewer** with highlighting
- **Progress tracking** for reading

### AI Analysis Interface
- **Persona selection** (Student, Professional, etc.)
- **Job context** specification
- **Real-time insights** generation
- **Strategic analysis** dashboard

### Podcast Creation
- **Script preview** before generation
- **Audio player** with controls
- **Download options** for generated podcasts
- **Batch processing** for multiple documents

## 🔌 API Endpoints

### Document Management
- `POST /upload-pdfs` - Upload documents
- `GET /documents` - List all documents
- `DELETE /documents/{id}` - Delete document
- `GET /pdf/{id}` - Download PDF

### Analysis & Insights
- `POST /analyze-documents` - Analyze with app.py
- `POST /insights` - Generate AI insights
- `POST /comprehensive-insights` - Detailed analysis
- `POST /strategic-insights` - Strategic recommendations

### Podcast Generation
- `POST /generate-podcast` - Create podcast using app.py
- `POST /podcast` - Generate from text/insights
- `GET /audio/{filename}` - Stream audio files
- `GET /download-podcast/{filename}` - Download podcast

### Search & Discovery
- `POST /search-documents` - Semantic search
- `POST /related-sections` - Find related content
- `GET /cross-connections/{id}` - Document relationships

## 🎯 Usage Examples

### 1. Upload and Analyze Documents

```typescript
// Upload documents
const documents = await apiService.uploadPDFs(files, "Student", "Research Paper");

// Analyze with AI
const analysis = await apiService.analyzeDocuments(
  documentIds, 
  "Student", 
  "Research Paper"
);
```

### 2. Generate Podcast

```typescript
// Generate podcast from query
const podcast = await apiService.generatePodcast(
  "What are the benefits of renewable energy?",
  relatedSections,
  insights
);
```

### 3. Get Strategic Insights

```typescript
// Get strategic analysis
const strategic = await apiService.generateStrategicInsights(
  text,
  "Business Analyst",
  "Market Research"
);
```

## 🔑 Configuration

### Environment Variables

Create `.env` files in both backend and frontend:

**Backend (.env):**
```bash
GOOGLE_API_KEY=your_gemini_api_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
```

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Document Analysis Platform
```

### API Keys Required

1. **Google Gemini AI** - For document analysis and insights
2. **AWS Polly** - For text-to-speech podcast generation
3. **AWS Credentials** - For audio file processing

## 🛠️ Development

### Backend Development
```bash
cd HARSHALADOBE/backend
pip install -r requirements.txt
python main.py
```

### Frontend Development
```bash
cd HARSHALADOBE
npm install
npm run dev
```

### Testing
```bash
# Backend tests
cd HARSHALADOBE/backend
python test_integration.py

# Frontend tests
cd HARSHALADOBE
npm run test
```

## 📊 Performance Features

### Backend Optimizations
- **FAISS indexing** for fast semantic search
- **Document chunking** for efficient processing
- **Caching** for frequently accessed data
- **Async processing** for better concurrency

### Frontend Optimizations
- **Lazy loading** for documents
- **React.memo** for expensive components
- **Virtual scrolling** for large lists
- **Progressive loading** for audio files

## 🔒 Security Considerations

- **CORS configuration** for cross-origin requests
- **File type validation** for uploads
- **Input sanitization** for user data
- **API key management** via environment variables

## 🚀 Deployment

### Production Setup

1. **Backend Deployment:**
   ```bash
   # Use Gunicorn for production
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Frontend Deployment:**
   ```bash
   npm run build
   # Serve dist/ folder with nginx or similar
   ```

3. **Environment Configuration:**
   - Set production API URLs
   - Configure SSL certificates
   - Set up database for persistent storage

## 🐛 Troubleshooting

### Common Issues

1. **Port 8000 already in use:**
   ```bash
   # Find and kill process
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. **Missing dependencies:**
   ```bash
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   npm install
   ```

3. **API key errors:**
   - Verify Google API key is valid
   - Check AWS credentials configuration
   - Ensure API quotas are sufficient

### Debug Mode

Enable debug logging:
```bash
export DEBUG=true
python main.py
```

## 📈 Future Enhancements

1. **Database Integration** - Replace in-memory storage
2. **User Authentication** - Add login/signup system
3. **Real-time Collaboration** - WebSocket support
4. **Advanced Analytics** - Usage statistics and insights
5. **Mobile App** - React Native version
6. **Cloud Storage** - AWS S3 integration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Run integration tests
4. Check server logs for errors

---

**🎉 Ready to analyze documents and create podcasts!**
