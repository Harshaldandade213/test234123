# 🚀 Integrated Document Analysis System - Usage Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Quick Start](#quick-start)
3. [API Endpoints](#api-endpoints)
4. [Usage Examples](#usage-examples)
5. [Frontend Features](#frontend-features)
6. [Troubleshooting](#troubleshooting)

## 🎯 System Overview

This integrated system combines two powerful backends:

- **🖥️ adobev4 Backend** (Port 8000): Advanced AI analysis and podcast generation
- **🔧 HARSHALADOBE Backend** (Port 8001): Document management and insights
- **🌐 Frontend** (Port 8081): Modern React interface

### Intelligent Routing:
- **Insights/Analysis** → Routes to adobev4's `analyze_and_categorize` function
- **Document Management** → Routes to HARSHALADOBE backend
- **Automatic Fallback** → Seamless switching between backends

## 🚀 Quick Start

### 1. Start All Services
```bash
# Start both backends
cd HARSHALADOBE
.\start-dual-backends.bat

# Start frontend (in new terminal)
cd HARSHALADOBE
npm run dev
```

### 2. Access the System
- **Frontend**: http://localhost:8081/
- **adobev4 API**: http://localhost:8000/docs
- **HARSHALADOBE API**: http://localhost:8001/docs

## 🔌 API Endpoints

### Document Management (HARSHALADOBE Backend)

#### Upload Documents
```bash
curl -X POST "http://localhost:8001/upload-pdfs" \
  -F "files=@document.pdf" \
  -F "persona=Software Developer" \
  -F "job_to_be_done=Code Review"
```

#### Get Documents
```bash
curl "http://localhost:8001/documents"
```

#### Search Documents
```bash
curl -X POST "http://localhost:8001/search-documents" \
  -F "query=testing methodologies" \
  -F "k=5"
```

### AI Analysis (adobev4 Backend via HARSHALADOBE)

#### Analyze Documents
```bash
curl -X POST "http://localhost:8001/analyze-documents" \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": ["doc-id-1", "doc-id-2"],
    "persona": "Software Developer",
    "job_to_be_done": "Code Review"
  }'
```

#### Generate Insights
```bash
curl -X POST "http://localhost:8001/insights" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text content here",
    "persona": "Software Developer",
    "job_to_be_done": "Code Review",
    "document_context": "Optional context"
  }'
```

#### Comprehensive Insights
```bash
curl -X POST "http://localhost:8001/comprehensive-insights" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Advanced content for analysis",
    "persona": "Software Developer",
    "job_to_be_done": "Code Review"
  }'
```

### Text Processing

#### Simplify Text
```bash
curl -X POST "http://localhost:8001/simplify" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Complex technical text to simplify"
  }'
```

#### Define Terms
```bash
curl -X POST "http://localhost:8001/define-term" \
  -H "Content-Type: application/json" \
  -d '{
    "term": "API",
    "context": "Software development context"
  }'
```

### Podcast Generation (adobev4 Backend)

#### Generate Podcast
```bash
curl -X POST "http://localhost:8000/generate-podcast" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Topic for podcast generation",
    "output_filename": "my_podcast.mp3"
  }'
```

## 💡 Usage Examples

### Example 1: Complete Document Analysis Workflow

```python
import requests
import json

# 1. Upload a document
with open('document.pdf', 'rb') as f:
    files = {'files': ('document.pdf', f, 'application/pdf')}
    data = {
        'persona': 'Software Developer',
        'job_to_be_done': 'Code Review'
    }
    response = requests.post('http://localhost:8001/upload-pdfs', files=files, data=data)
    documents = response.json()
    doc_id = documents[0]['id']

# 2. Analyze the document
analysis_data = {
    "document_ids": [doc_id],
    "persona": "Software Developer",
    "job_to_be_done": "Code Review"
}
response = requests.post('http://localhost:8001/analyze-documents', json=analysis_data)
analysis = response.json()

# 3. Generate insights
insights_data = {
    "text": "Your text content",
    "persona": "Software Developer",
    "job_to_be_done": "Code Review"
}
response = requests.post('http://localhost:8001/insights', json=insights_data)
insights = response.json()

# 4. Generate podcast
podcast_data = {
    "query": "Summary of the analysis",
    "output_filename": "analysis_podcast.mp3"
}
response = requests.post('http://localhost:8000/generate-podcast', json=podcast_data)
podcast = response.json()

print("Analysis complete!")
```

### Example 2: Multi-Document Analysis

```python
import requests

# Upload multiple documents
doc_ids = []
for doc_file in ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']:
    with open(doc_file, 'rb') as f:
        files = {'files': (doc_file, f, 'application/pdf')}
        response = requests.post('http://localhost:8001/upload-pdfs', files=files)
        doc_ids.append(response.json()[0]['id'])

# Analyze all documents together
analysis_data = {
    "document_ids": doc_ids,
    "persona": "Project Manager",
    "job_to_be_done": "Project Planning"
}
response = requests.post('http://localhost:8001/analyze-documents', json=analysis_data)
analysis = response.json()

# Get related sections
related_data = {
    "document_ids": json.dumps(doc_ids),
    "current_page": 1,
    "current_section": "Project requirements",
    "persona": "Project Manager",
    "job_to_be_done": "Project Planning"
}
response = requests.post('http://localhost:8001/related-sections', data=related_data)
related = response.json()
```

### Example 3: Text Processing Pipeline

```python
import requests

# 1. Simplify complex text
simplify_data = {
    "text": "The implementation of sophisticated algorithmic paradigms necessitates the utilization of complex computational methodologies."
}
response = requests.post('http://localhost:8001/simplify', json=simplify_data)
simplified_text = response.json()['text']

# 2. Generate insights from simplified text
insights_data = {
    "text": simplified_text,
    "persona": "Student",
    "job_to_be_done": "Learning"
}
response = requests.post('http://localhost:8001/insights', json=insights_data)
insights = response.json()

# 3. Define technical terms
define_data = {
    "term": "Algorithm",
    "context": "Computer science and programming"
}
response = requests.post('http://localhost:8001/define-term', json=define_data)
definition = response.json()['definition']
```

## 🌐 Frontend Features

### 1. Document Upload
- Drag & drop PDF, DOCX, TXT files
- Automatic metadata extraction
- Progress tracking

### 2. Document Library
- Browse uploaded documents
- Search and filter by persona/job
- Document outlines and metadata

### 3. AI Analysis
- One-click document analysis
- Real-time insights generation
- Comprehensive analysis reports

### 4. Text Processing
- Text simplification
- Term definitions
- Context-aware processing

### 5. Podcast Generation
- AI-generated podcast scripts
- Audio file generation
- Download and playback

### 6. Search & Discovery
- Semantic document search
- Related sections discovery
- Cross-document connections

## 🔧 Troubleshooting

### Common Issues

#### 1. Backend Connection Issues
```bash
# Check if backends are running
netstat -ano | findstr ":800"

# Restart backends
cd HARSHALADOBE
.\start-dual-backends.bat
```

#### 2. Frontend Not Loading
```bash
# Check frontend status
netstat -ano | findstr ":8081"

# Restart frontend
cd HARSHALADOBE
npm run dev
```

#### 3. Document Upload Failures
- Ensure file is PDF, DOCX, or TXT
- Check file size (max 50MB)
- Verify backend is running

#### 4. Analysis Failures
- Check Google API key configuration
- Ensure documents are properly indexed
- Verify network connectivity

### Error Codes

- **422**: Validation error - check request format
- **500**: Server error - check backend logs
- **404**: Resource not found - check document IDs
- **503**: Service unavailable - restart backends

### Debug Mode

Enable debug logging in backend:
```python
# In main.py, add debug prints
print(f"Processing request: {request}")
```

## 📊 Performance Tips

1. **Batch Operations**: Upload multiple documents at once
2. **Caching**: Use document IDs for repeated operations
3. **Async Processing**: Large documents are processed asynchronously
4. **Indexing**: Documents are automatically indexed for fast search

## 🔒 Security Considerations

1. **API Keys**: Store Google API keys securely
2. **File Uploads**: Validate file types and sizes
3. **CORS**: Configure CORS for production
4. **Authentication**: Add authentication for production use

## 📈 Monitoring

### Health Checks
```bash
# Check backend health
curl http://localhost:8000/health
curl http://localhost:8001/health

# Check frontend
curl http://localhost:8081/
```

### Logs
- Backend logs: Check terminal output
- Frontend logs: Browser developer tools
- Error logs: Check server.err.log files

## 🎯 Next Steps

1. **Customize Personas**: Add your specific personas
2. **Extend Analysis**: Add custom analysis types
3. **Integrate APIs**: Connect with external services
4. **Scale Up**: Deploy to production environment

---

**🎉 You're now ready to use the integrated document analysis system!**

For more help, check the API documentation at:
- http://localhost:8000/docs (adobev4)
- http://localhost:8001/docs (HARSHALADOBE)
