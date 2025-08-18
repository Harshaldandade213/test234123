# Quick Start Guide - Backend-Frontend Integration

## Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** installed
3. **Google API Key** for Gemini AI
4. **AWS Credentials** (optional, for advanced features)

## Backend Setup

### 1. Install Dependencies
```bash
cd adobev4
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the `adobev4` directory:
```bash
# Google API Key for Gemini AI
GOOGLE_API_KEY=your_google_api_key_here

# AWS Configuration (optional)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Backend Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### 3. Start Backend Server
```bash
cd adobev4
python main.py
```

The backend will start on `http://localhost:8000`

### 4. Verify Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2024-01-01T12:00:00"}
```

## Frontend Setup

### 1. Install Dependencies
```bash
cd HARSHALADOBE
npm install
```

### 2. Configure Environment
Create a `.env` file in the `HARSHALADOBE` directory:
```bash
# Backend API URL
VITE_API_URL=http://localhost:8000

# Frontend Configuration
VITE_APP_TITLE=Document Analysis Platform
```

### 3. Start Frontend Development Server
```bash
cd HARSHALADOBE
npm run dev
```

The frontend will start on `http://localhost:5173`

## Testing the Integration

### 1. Run Integration Tests
```bash
cd adobev4
python test_integration.py
```

This will test all backend endpoints to ensure they're working correctly.

### 2. Manual Testing

#### Upload a Document
1. Open `http://localhost:5173` in your browser
2. Navigate to the upload section
3. Select a PDF, DOCX, or TXT file
4. Add persona and job context (optional)
5. Click upload

#### Generate Insights
1. Select an uploaded document
2. Click "Generate Insights"
3. View AI-generated insights and analysis

#### Create Podcast
1. Select content from documents
2. Click "Generate Podcast"
3. Download the generated audio file

## API Documentation

Once the backend is running, you can access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### Backend Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **API Key Issues**
   - Verify your Google API key is valid
   - Check API quota limits
   - Ensure the key has access to Gemini models

### Frontend Issues

1. **CORS Errors**
   - Ensure backend is running on `http://localhost:8000`
   - Check CORS configuration in backend

2. **API Connection Failed**
   - Verify `VITE_API_URL` is set correctly
   - Check if backend is running and accessible

3. **Build Errors**
   ```bash
   npm run build
   # Check for specific error messages
   ```

### Common Error Messages

1. **"Failed to fetch"**
   - Backend server not running
   - Incorrect API URL
   - Network connectivity issues

2. **"Invalid API key"**
   - Google API key is invalid or expired
   - Key doesn't have access to Gemini models

3. **"File not found"**
   - Document was deleted or moved
   - File path issues

## Development Workflow

### 1. Backend Development
```bash
cd adobev4
# Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Development
```bash
cd HARSHALADOBE
# Start with hot reload
npm run dev
```

### 3. Testing Changes
```bash
# Test backend endpoints
cd adobev4
python test_integration.py

# Test frontend
cd HARSHALADOBE
npm run test
```

## Production Deployment

### Backend Deployment
1. Use a production WSGI server like Gunicorn
2. Set up proper environment variables
3. Configure reverse proxy (nginx)
4. Set up SSL certificates

### Frontend Deployment
1. Build the production version
2. Serve static files
3. Configure API URL for production backend

## Monitoring and Logs

### Backend Logs
```bash
# View backend logs
tail -f adobev4/server.log

# Enable debug logging
export DEBUG=true
python main.py
```

### Frontend Logs
Check browser developer console for frontend errors and API calls.

## Performance Optimization

1. **Backend**
   - Use connection pooling for database
   - Implement caching for frequently accessed data
   - Optimize document processing

2. **Frontend**
   - Implement lazy loading for documents
   - Use React.memo for expensive components
   - Optimize bundle size

## Security Checklist

- [ ] Use environment variables for sensitive data
- [ ] Implement proper CORS configuration
- [ ] Add input validation and sanitization
- [ ] Set up rate limiting
- [ ] Use HTTPS in production
- [ ] Implement authentication if needed

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Run integration tests
4. Check logs for error details

## Next Steps

1. **Customization**: Modify the UI and API to match your specific needs
2. **Features**: Add new AI-powered features using the existing infrastructure
3. **Integration**: Connect with external systems and databases
4. **Scaling**: Optimize for larger document volumes and user loads
