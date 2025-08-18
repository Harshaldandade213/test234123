# Manual API Testing Guide

This guide provides curl commands and examples for manually testing each endpoint of your FastAPI server.

## 🚀 Quick Start

Make sure your server is running:
```bash
python run_server.py
```

Server will be available at: http://localhost:8000

## 📋 Test Results Summary

From the automated tests:
- ✅ **10/11 tests passed** (91% success rate)
- ✅ All core functionality working
- ⚠️ Reading progress tracking needs a valid document ID

## 🧪 Manual Testing Commands

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-17T19:11:02.125530"
}
```

### 2. Get All Documents
```bash
curl http://localhost:8000/documents
```

**Expected Response:**
```json
[]
```

### 3. Get Personas
```bash
curl http://localhost:8000/library/personas
```

**Expected Response:**
```json
[]
```

### 4. Generate AI Insights
```bash
curl -X POST http://localhost:8000/insights \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is transforming the way we work and live. Machine learning algorithms are becoming more sophisticated and accessible.",
    "persona": "Technology Professional",
    "job_to_be_done": "Understanding AI trends and applications"
  }'
```

**Expected Response:**
```json
{
  "insights": [
    {
      "type": "fact",
      "content": "AI and machine learning are rapidly advancing..."
    },
    {
      "type": "takeaway",
      "content": "Technology professionals should stay updated..."
    }
  ]
}
```

### 5. Generate Comprehensive Insights
```bash
curl -X POST http://localhost:8000/comprehensive-insights \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The rapid advancement of artificial intelligence technologies is reshaping industries across the globe.",
    "persona": "Business Executive",
    "job_to_be_done": "Evaluating AI adoption strategies"
  }'
```

**Expected Response:**
```json
{
  "insights": [...],
  "persona_insights": [...],
  "topic_analysis": {
    "main_themes": "...",
    "trending_topics": "...",
    "research_opportunities": "..."
  },
  "web_facts": [...],
  "keywords": ["AI", "Business Transformation", ...],
  "search_queries": [...]
}
```

### 6. Simplify Text
```bash
curl -X POST http://localhost:8000/simplify-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The implementation of artificial intelligence algorithms necessitates comprehensive understanding of machine learning paradigms and neural network architectures."
  }'
```

**Expected Response:**
```json
{
  "text": "Using AI requires understanding machine learning and neural networks.",
  "original": "The implementation of artificial intelligence algorithms necessitates comprehensive understanding of machine learning paradigms and neural network architectures."
}
```

### 7. Define Term
```bash
curl -X POST http://localhost:8000/define-term \
  -H "Content-Type: application/json" \
  -d '{
    "term": "machine learning",
    "context": "In the context of artificial intelligence and data science"
  }'
```

**Expected Response:**
```json
{
  "definition": "In the context of artificial intelligence and data science, machine learning is a type of artificial intelligence that allows computer systems to learn and improve from experience without being explicitly programmed..."
}
```

### 8. Upload Document (using a test file)
```bash
curl -X POST http://localhost:8000/upload-pdfs \
  -F "files=@documents/test2.docx" \
  -F "persona=Test User" \
  -F "job_to_be_done=Testing API functionality"
```

**Expected Response:**
```json
[
  {
    "id": "aa7a2143-16a8-4adb-adbd-286513f484d2",
    "name": "test2.docx",
    "title": "test2",
    "outline": [...],
    "language": "en",
    "upload_timestamp": "2025-08-17T19:11:00.000000"
  }
]
```

### 9. Analyze Documents (after uploading)
```bash
curl -X POST http://localhost:8000/analyze-documents \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": ["aa7a2143-16a8-4adb-adbd-286513f484d2"],
    "persona": "Test Analyst",
    "job_to_be_done": "Testing document analysis functionality"
  }'
```

**Expected Response:**
```json
{
  "analysis_results": {
    "query": "...",
    "analysis": [...],
    "summary": "..."
  },
  "insights": [...]
}
```

### 10. Track Reading Progress
```bash
curl -X POST http://localhost:8000/reading-progress \
  -F "doc_id=aa7a2143-16a8-4adb-adbd-286513f484d2" \
  -F "current_page=5" \
  -F "total_pages=20" \
  -F "time_spent=300"
```

**Expected Response:**
```json
{
  "progress_percentage": 25.0,
  "time_spent_minutes": 5.0,
  "estimated_remaining_minutes": 15.0,
  "estimated_total_minutes": 20.0
}
```

### 11. Get Library Documents (with filters)
```bash
# Without filters
curl http://localhost:8000/library/documents

# With persona filter
curl "http://localhost:8000/library/documents?persona=technology"

# With job filter
curl "http://localhost:8000/library/documents?job_to_be_done=analysis"
```

### 12. Get PDF File
```bash
curl http://localhost:8000/pdf/aa7a2143-16a8-4adb-adbd-286513f484d2
```

### 13. Get Audio File
```bash
curl http://localhost:8000/audio/podcast_output.mp3
```

## 🌐 Interactive Testing

### Using the Web Interface

1. **Open your browser** and go to: http://localhost:8000/docs
2. **Explore all endpoints** with the interactive Swagger UI
3. **Test endpoints directly** in the browser
4. **View request/response examples** for each endpoint

### Alternative Documentation

- **ReDoc**: http://localhost:8000/redoc (Alternative documentation format)

## 🔧 Testing Tips

### 1. Check Server Status
Always start by testing the health endpoint to ensure the server is running.

### 2. Test in Order
Some endpoints depend on others:
- Upload documents first
- Then analyze them
- Then track reading progress

### 3. Use Real Data
The AI endpoints work best with real, meaningful text content.

### 4. Check Response Headers
Look for proper content types and status codes.

### 5. Test Error Cases
Try invalid data to test error handling:
```bash
# Test with invalid JSON
curl -X POST http://localhost:8000/insights \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
```

## 📊 Performance Testing

### Load Testing (Optional)
```bash
# Install Apache Bench (ab) or use a similar tool
ab -n 100 -c 10 http://localhost:8000/health
```

### Memory Usage
Monitor the server's memory usage during testing, especially for document processing.

## 🐛 Troubleshooting

### Common Issues

1. **Server not responding**
   - Check if server is running: `python run_server.py`
   - Check port 8000 is not in use

2. **CORS errors**
   - The server is configured to allow all origins
   - Check browser console for CORS issues

3. **File upload issues**
   - Ensure files are in supported formats (PDF, DOCX, TXT)
   - Check file size limits

4. **AI generation errors**
   - Verify Google API key is working
   - Check internet connection for API calls

### Debug Mode

Run the server with debug logging:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## ✅ Success Criteria

Your API is working correctly if:

- ✅ Health check returns 200 OK
- ✅ All endpoints respond with appropriate status codes
- ✅ AI endpoints generate meaningful insights
- ✅ Document upload and analysis work
- ✅ File serving works correctly
- ✅ Error handling works for invalid requests

## 🎉 Next Steps

Once testing is complete:

1. **Build a frontend** to consume these APIs
2. **Add authentication** for production use
3. **Implement database storage** instead of in-memory
4. **Add more comprehensive error handling**
5. **Deploy to production environment**
