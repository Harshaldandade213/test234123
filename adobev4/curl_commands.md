# FastAPI Endpoint Testing - Curl Commands

## 🚀 **Server Information**
- **Base URL**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 📋 **1. Health Check**
```bash
curl -X GET http://localhost:8000/health
```

## 📄 **2. Document Management**

### Upload PDF Documents
```bash
curl -X POST http://localhost:8000/upload-pdfs \
  -F "files=@documents/Abhishek 4302 G-A (1).pdf" \
  -F "persona=UX Researcher" \
  -F "job_to_be_done=Analyzing design documents for research insights"
```

### Get All Documents
```bash
curl -X GET http://localhost:8000/documents
```

### Delete Document
```bash
curl -X DELETE http://localhost:8000/documents/{doc_id}
```

## 🔍 **3. App.py Integration Endpoints**

### Index Documents (Using app.py logic)
```bash
curl -X POST http://localhost:8000/index-documents
```

### Search Documents (Using app.py logic)
```bash
curl -X POST http://localhost:8000/search-documents \
  -F "query=design principles" \
  -F "k=5"
```

### Analyze Query (Using app.py logic)
```bash
curl -X POST http://localhost:8000/analyze-query \
  -F "query=What are the key design principles discussed in the documents?"
```

## 📊 **4. Document Analysis**

### Analyze Documents with Persona and Job Context
```bash
curl -X POST http://localhost:8000/analyze-documents \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": ["your-doc-id-here"],
    "persona": "UX Researcher",
    "job_to_be_done": "Analyzing design principles and usability guidelines"
  }'
```

### Generate AI Insights
```bash
curl -X POST http://localhost:8000/insights \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Design principles and usability guidelines for creating user-centered interfaces",
    "persona": "UX Designer",
    "job_to_be_done": "Understanding design principles and usability guidelines",
    "document_context": "Analyzing design documents for research"
  }'
```

### Generate Comprehensive Insights
```bash
curl -X POST http://localhost:8000/comprehensive-insights \
  -H "Content-Type: application/json" \
  -d '{
    "text": "User-centered design methodology and implementation strategies for modern applications",
    "persona": "UX Research Manager",
    "job_to_be_done": "Comprehensive analysis of design methodologies",
    "document_context": "Researching design principles and user experience"
  }'
```

## 📝 **5. Content Processing**

### Simplify Text
```bash
curl -X POST http://localhost:8000/simplify-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The implementation of user-centered design methodologies necessitates a comprehensive understanding of cognitive psychology principles and human-computer interaction paradigms."
  }'
```

### Define Term
```bash
curl -X POST http://localhost:8000/define-term \
  -H "Content-Type: application/json" \
  -d '{
    "term": "usability",
    "context": "User interface design and user experience"
  }'
```

## 📚 **6. Library & Organization**

### Get Documents Filtered by Persona/Job
```bash
curl -X GET "http://localhost:8000/library/documents?persona=UX%20Researcher&job_to_be_done=Document%20analysis"
```

### Get Available Personas
```bash
curl -X GET http://localhost:8000/library/personas
```

## 📖 **7. Reading Progress**

### Track Reading Progress
```bash
curl -X POST http://localhost:8000/reading-progress \
  -F "doc_id=your-doc-id-here" \
  -F "current_page=5" \
  -F "total_pages=20" \
  -F "time_spent=300"
```

## 📄 **8. Media & Files**

### Get PDF File
```bash
curl -X GET http://localhost:8000/pdf/{doc_id} \
  -o downloaded_document.pdf
```

### Get Audio File
```bash
curl -X GET http://localhost:8000/audio/{filename} \
  -o downloaded_audio.mp3
```

## 🔄 **9. Complete Workflow Example**

### Step 1: Upload and Index Documents
```bash
# Upload a PDF
curl -X POST http://localhost:8000/upload-pdfs \
  -F "files=@documents/Abhishek 4302 G-A (1).pdf" \
  -F "persona=UX Researcher" \
  -F "job_to_be_done=Document analysis"

# Index documents
curl -X POST http://localhost:8000/index-documents
```

### Step 2: Search Documents
```bash
curl -X POST http://localhost:8000/search-documents \
  -F "query=design principles usability" \
  -F "k=3"
```

### Step 3: Analyze Documents
```bash
curl -X POST http://localhost:8000/analyze-query \
  -F "query=What are the key insights about usability and user experience?"
```

### Step 4: Generate Insights
```bash
curl -X POST http://localhost:8000/insights \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The documents discuss various design principles including usability guidelines, user-centered design, and accessibility considerations.",
    "persona": "UX Designer",
    "job_to_be_done": "Understanding design principles",
    "document_context": "Design documentation analysis"
  }'
```

## 🛠️ **10. PowerShell Commands (Windows)**

For Windows PowerShell users, use these commands instead:

### Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
```

### Upload Documents
```powershell
$form = @{
    files = Get-Item "documents\Abhishek 4302 G-A (1).pdf"
    persona = "UX Researcher"
    job_to_be_done = "Document analysis"
}
Invoke-WebRequest -Uri "http://localhost:8000/upload-pdfs" -Method POST -Form $form
```

### Search Documents
```powershell
$form = @{
    query = "design principles"
    k = 5
}
Invoke-WebRequest -Uri "http://localhost:8000/search-documents" -Method POST -Form $form
```

### Generate Insights
```powershell
$body = @{
    text = "Design principles and usability guidelines"
    persona = "UX Designer"
    job_to_be_done = "Understanding design principles"
    document_context = "Design documentation"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/insights" -Method POST -Body $body -ContentType "application/json"
```

## 📝 **11. Testing Notes**

### Expected Responses:
- **Success**: HTTP 200 with JSON response
- **Error**: HTTP 4xx/5xx with error details
- **File Upload**: Returns document metadata with ID
- **Search**: Returns relevant passages with similarity scores
- **Analysis**: Returns categorized insights with justifications

### Common Issues:
1. **Server not running**: Ensure `python main.py` is running
2. **File not found**: Check file paths in documents directory
3. **API key issues**: Verify Google Gemini API key is configured
4. **CORS issues**: Server allows all origins for development

### Tips:
- Use `-v` flag for verbose output: `curl -v -X GET http://localhost:8000/health`
- Save responses to file: `curl -X GET http://localhost:8000/documents > response.json`
- Test with Swagger UI: Visit `http://localhost:8000/docs` for interactive testing

## 🎯 **12. Quick Test Sequence**

Run these commands in sequence to test the complete system:

```bash
# 1. Check server health
curl -X GET http://localhost:8000/health

# 2. Upload a document
curl -X POST http://localhost:8000/upload-pdfs -F "files=@documents/Abhishek 4302 G-A (1).pdf"

# 3. Index documents
curl -X POST http://localhost:8000/index-documents

# 4. Search for content
curl -X POST http://localhost:8000/search-documents -F "query=design" -F "k=3"

# 5. Analyze with AI
curl -X POST http://localhost:8000/analyze-query -F "query=What are the main topics discussed?"

# 6. Generate insights
curl -X POST http://localhost:8000/insights -H "Content-Type: application/json" -d '{"text": "Design principles and usability", "persona": "UX Designer", "job_to_be_done": "Understanding design"}'
```

This sequence will test the core functionality of your FastAPI backend with app.py integration! 🚀
