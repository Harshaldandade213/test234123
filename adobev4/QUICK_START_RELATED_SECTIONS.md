# Quick Start Guide: Enhanced Related Sections

## Overview

This guide will help you quickly set up and test the enhanced related sections functionality that integrates HARSHALADOBE's sophisticated logic into the adobev4 system.

## Prerequisites

1. **Python Environment**: Python 3.8+ with pip
2. **Google API Key**: Valid Google Gemini API key
3. **Documents**: Some PDF documents for testing

## Setup Instructions

### 1. Install Dependencies

```bash
cd adobev4
pip install -r requirements.txt
```

### 2. Configure API Key

Set your Google Gemini API key in the environment:

```bash
# Windows
set GOOGLE_API_KEY=your_api_key_here

# Linux/Mac
export GOOGLE_API_KEY=your_api_key_here
```

Or update the key directly in `main.py`:
```python
GOOGLE_API_KEY = "your_api_key_here"
```

### 3. Start the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

## Testing the Enhanced Functionality

### 1. Upload Test Documents

First, upload some documents to test with:

```bash
# Using curl to upload a PDF
curl -X POST "http://localhost:8000/upload-pdfs" \
  -F "files=@your_document.pdf" \
  -F "persona=Software Engineer" \
  -F "job_to_be_done=Design cloud infrastructure"
```

### 2. Run the Test Script

```bash
python test_related_sections.py
```

This will test the enhanced related sections endpoint and show detailed results.

### 3. Manual API Testing

You can also test manually using curl:

```bash
curl -X POST "http://localhost:8000/related-sections" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "document_ids=doc1&document_ids=doc2&current_page=5&current_section=Cloud Architecture&persona=Software Engineer&job_to_be_done=Design scalable infrastructure"
```

## Expected Results

### Successful Response

```json
{
  "related_sections": [
    {
      "document": "Cloud Computing Guide",
      "section_title": "Microservices Architecture",
      "page_number": 12,
      "relevance_score": 0.85,
      "explanation": "Addresses microservices directly relevant to your role and objectives with high contextual relevance.",
      "relationship_type": "related",
      "key_concepts": ["microservices", "architecture", "scalability"]
    },
    {
      "document": "System Design Patterns",
      "section_title": "Load Balancing Strategies",
      "page_number": 8,
      "relevance_score": 0.72,
      "explanation": "Provides information about load balancing for your design scalable infrastructure.",
      "relationship_type": "complementary",
      "key_concepts": ["load balancing", "scalability", "performance"]
    }
  ]
}
```

### Key Features to Observe

1. **Enhanced Explanations**: Detailed explanations of why sections are relevant
2. **Relationship Types**: Different types of relationships (related, complementary, etc.)
3. **Key Concepts**: Extracted key concepts that connect the sections
4. **Relevance Scores**: Sophisticated scoring based on multiple factors

## Frontend Integration

### 1. Start the Frontend

```bash
cd ../HARSHALADOBE
npm install
npm run dev
```

### 2. Test in Browser

1. Open `http://localhost:5173` (or your frontend URL)
2. Upload documents
3. Navigate to a PDF reader
4. Observe related sections being loaded automatically
5. Check the highlights and cross-connections panels

### 3. Verify Integration

- **Automatic Loading**: Related sections should load when you change pages
- **Visual Highlights**: Related sections should appear as colored highlights
- **Cross-Connections**: Check the cross-connections panel for document relationships
- **Copy/Export**: Related sections should be included in copy/download features

## Troubleshooting

### Common Issues

#### 1. "No related sections found"
**Solution**: 
- Ensure documents are properly uploaded and indexed
- Check that the search query is relevant
- Verify the API key is working

#### 2. "API quota exceeded"
**Solution**:
- The system will automatically fall back to keyword-based analysis
- Check your Google API usage
- Consider upgrading your API quota

#### 3. "Model initialization failed"
**Solution**:
- Check internet connection for model downloads
- Verify all dependencies are installed
- Check Python version compatibility

#### 4. "Slow response times"
**Solution**:
- First request may be slow due to model loading
- Subsequent requests should be faster
- Check server resources and network

### Debug Mode

Enable debug logging by adding this to `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Tips

### 1. Optimize for Speed
- Use smaller document sets for testing
- Cache embeddings when possible
- Monitor API usage to avoid rate limits

### 2. Improve Relevance
- Provide specific personas and job descriptions
- Use relevant document content
- Ensure good document quality

### 3. Enhance Diversity
- Upload diverse document types
- Include different topics and domains
- Use varied document sources

## Next Steps

### 1. Customize for Your Use Case
- Modify the scoring weights in `find_related_sections_enhanced()`
- Adjust the relationship types based on your needs
- Customize the explanation generation

### 2. Scale Up
- Add more documents to the system
- Implement caching for better performance
- Consider database storage for large document sets

### 3. Advanced Features
- Implement real-time updates
- Add user preference learning
- Create custom relationship types

## Support

If you encounter issues:

1. Check the logs in the terminal
2. Review the `ENHANCED_RELATED_SECTIONS.md` documentation
3. Test with the provided test script
4. Verify all dependencies are correctly installed

## Conclusion

The enhanced related sections functionality provides a powerful, AI-driven approach to discovering relevant content across documents. By following this guide, you should be able to quickly set up and test the system, and then integrate it into your own applications.

The system automatically handles fallbacks and provides robust error handling, ensuring a smooth user experience even when external APIs are unavailable.
