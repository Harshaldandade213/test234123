# Document Analysis & Podcast Generation API

A comprehensive FastAPI backend server that provides document management, analysis, and podcast generation capabilities using the existing service layer functions.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS credentials configured (for audio generation)
- Google Gemini API key (already configured in the code)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python run_server.py
```

The server will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## 📚 API Endpoints

### 1. Document Management

#### POST /upload-pdfs
Upload PDF, DOCX, or TXT documents with metadata for analysis.

**Request (FormData):**
```
files: [File1, File2, ...]
persona: string (optional)
job_to_be_done: string (optional)
```

**Response:**
```json
[
  {
    "id": "string",
    "name": "string", 
    "title": "string",
    "outline": [
      {
        "level": "string",
        "text": "string", 
        "page": "number"
      }
    ],
    "language": "string",
    "upload_timestamp": "string"
  }
]
```

#### GET /documents
Retrieve all uploaded documents.

**Response:**
```json
[
  {
    "id": "string",
    "name": "string",
    "title": "string", 
    "outline": [...],
    "language": "string",
    "upload_timestamp": "string"
  }
]
```

#### DELETE /documents/{doc_id}
Delete a specific document.

**Response:** 200 OK (no body)

### 2. Document Analysis

#### POST /analyze-documents
Analyze documents with persona and job context.

**Request:**
```json
{
  "document_ids": ["string"],
  "persona": "string",
  "job_to_be_done": "string"
}
```

**Response:**
```json
{
  "analysis_results": "object",
  "insights": ["string"]
}
```

#### POST /insights
Generate AI insights from text content.

**Request:**
```json
{
  "text": "string",
  "persona": "string", 
  "job_to_be_done": "string",
  "document_context": "string (optional)"
}
```

**Response:**
```json
{
  "insights": [
    {
      "type": "takeaway|fact|contradiction|connection|info|error",
      "content": "string"
    }
  ]
}
```

#### POST /comprehensive-insights
Generate comprehensive insights with web facts and analysis.

**Request:**
```json
{
  "text": "string",
  "persona": "string",
  "job_to_be_done": "string", 
  "document_context": "string (optional)"
}
```

**Response:**
```json
{
  "insights": [...],
  "persona_insights": [
    {
      "type": "relevance|action|skill",
      "content": "string"
    }
  ],
  "topic_analysis": {
    "main_themes": "string",
    "trending_topics": "string",
    "research_opportunities": "string"
  },
  "web_facts": [
    {
      "type": "string",
      "query": "string", 
      "description": "string"
    }
  ],
  "keywords": ["string"],
  "search_queries": ["string"]
}
```

### 3. Content Processing

#### POST /simplify-text
Simplify text difficulty using AI.

**Request:**
```json
{
  "text": "string"
}
```

**Response:**
```json
{
  "text": "string (simplified)",
  "original": "string"
}
```

#### POST /define-term
Define terms in context.

**Request:**
```json
{
  "term": "string",
  "context": "string"
}
```

**Response:**
```json
{
  "definition": "string"
}
```

### 4. Library & Organization

#### GET /library/documents
Get documents filtered by persona/job.

**Query Parameters:**
- `persona`: string (optional)
- `job_to_be_done`: string (optional)

**Response:**
```json
[
  {
    "id": "string",
    "name": "string",
    "title": "string",
    "outline": [...],
    "language": "string", 
    "upload_timestamp": "string"
  }
]
```

#### GET /library/personas
Get available personas.

**Response:**
```json
["string"]
```

### 5. Reading Progress

#### POST /reading-progress
Track reading progress.

**Request (FormData):**
```
doc_id: string
current_page: number
total_pages: number
time_spent: number
```

**Response:**
```json
{
  "progress_percentage": "number",
  "time_spent_minutes": "number",
  "estimated_remaining_minutes": "number",
  "estimated_total_minutes": "number"
}
```

### 6. Media & Files

#### GET /pdf/{doc_id}
Get PDF file for viewing.

**Response:** PDF file (binary)

#### GET /audio/{filename}
Get generated audio files.

**Response:** Audio file (binary)

### 7. Health Check

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "string"
}
```

## 🔧 Configuration

### Environment Variables

The following configurations are hardcoded in the application:

- **Google API Key**: `AIzaSyDGiX4nxOcanzRLZOA5tL6gB90Aidc-jII`
- **AWS Region**: `us-east-1`
- **Server Host**: `0.0.0.0`
- **Server Port**: `8000`

### AWS Setup

For audio generation functionality, ensure you have AWS credentials configured:

1. **AWS CLI**: `aws configure`
2. **Environment Variables**: Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
3. **AWS Credentials File**: `~/.aws/credentials`

## 📁 Project Structure

```
adobev4/
├── main.py                 # FastAPI application
├── app.py                  # Service layer functions
├── run_server.py          # Server startup script
├── requirements.txt       # Python dependencies
├── documents/            # Document storage
├── index/               # Search index storage
├── audio/               # Generated audio files
└── API_README.md        # This file
```

## 🛠️ Development

### Running in Development Mode

```bash
python run_server.py
```

The server runs with auto-reload enabled, so changes to the code will automatically restart the server.

### Running in Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing the API

1. **Interactive Documentation**: Visit http://localhost:8000/docs
2. **Health Check**: `curl http://localhost:8000/health`
3. **Upload Document**: Use the `/docs` interface or curl with FormData

## 🔍 Features

### Document Processing
- **PDF, DOCX, TXT Support**: Automatic parsing and text extraction
- **Chunking**: Intelligent text chunking for better analysis
- **Metadata Extraction**: Automatic outline generation and metadata extraction

### AI Analysis
- **Google Gemini Integration**: Advanced AI analysis and insights generation
- **Semantic Search**: FAISS-based vector search for document retrieval
- **Multi-stage Analysis**: Retrieval + LLM categorization pipeline

### Audio Generation
- **AWS Polly Integration**: High-quality text-to-speech
- **Multi-speaker Support**: Alex (host) and Dr. Sharma (expert) voices
- **Podcast Generation**: Complete podcast script and audio generation

### Data Management
- **In-memory Storage**: Fast access for development (replace with database for production)
- **File Management**: Automatic file organization and cleanup
- **Progress Tracking**: Reading progress and time estimation

## 🚨 Important Notes

1. **In-memory Storage**: The current implementation uses in-memory storage. For production, replace with a proper database (PostgreSQL, MongoDB, etc.).

2. **File Security**: Implement proper file validation and security measures for production use.

3. **CORS Configuration**: The current CORS settings allow all origins. Configure properly for production.

4. **API Key Security**: The Google API key is hardcoded. Use environment variables for production.

5. **Error Handling**: Implement more robust error handling and logging for production.

## 🔮 Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- User authentication and authorization
- Advanced document filtering and search
- Real-time collaboration features
- Enhanced audio processing capabilities
- WebSocket support for real-time updates
- Docker containerization
- Kubernetes deployment support

## 📞 Support

For issues and questions:
1. Check the interactive API documentation at `/docs`
2. Review the service layer functions in `app.py`
3. Check the logs for detailed error information
