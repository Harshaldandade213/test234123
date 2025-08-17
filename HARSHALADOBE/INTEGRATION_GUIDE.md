# Integrated Frontend-Backend System

## 🎯 Overview

This system integrates the HARSHALADOBE frontend with both adobev4 and HARSHALADOBE backends, providing intelligent routing where:

- **Insights calls** → Route to **adobev4's `analyze_and_categorize` function**
- **Other endpoints** → Use **HARSHALADOBE backend** for missing FastAPI mappings

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Integrated API  │    │   Backends      │
│   (React)       │◄──►│   Service        │◄──►│                 │
│   Port: 5173    │    │   (TypeScript)   │    │                 │
└─────────────────┘    └──────────────────┘    │ ┌─────────────┐ │
                                               │ │ adobev4     │ │
                                               │ │ Port: 8000  │ │
                                               │ └─────────────┘ │
                                               │ ┌─────────────┐ │
                                               │ │ HARSHALADOBE│ │
                                               │ │ Port: 8001  │ │
                                               │ └─────────────┘ │
                                               └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)

**Windows:**
```bash
# Start both backends
start-dual-backends.bat

# Start frontend (in separate terminal)
cd HARSHALADOBE
npm install
npm run dev
```

**PowerShell:**
```powershell
# Start both backends
.\start-dual-backends.ps1

# Start frontend (in separate terminal)
cd HARSHALADOBE
npm install
npm run dev
```

### Option 2: Manual Startup

**Terminal 1 - adobev4 Backend:**
```bash
cd adobev4
pip install -r requirements.txt
python main.py
```

**Terminal 2 - HARSHALADOBE Backend:**
```bash
cd HARSHALADOBE/backend
pip install -r requirements.txt
python main.py
```

**Terminal 3 - Frontend:**
```bash
cd HARSHALADOBE
npm install
npm run dev
```

## 🔌 API Routing Strategy

### Routes to adobev4 (Port 8000)

| Endpoint | Purpose | Uses app.py Function |
|----------|---------|---------------------|
| `/analyze-documents` | Document analysis | `analyze_and_categorize()` |
| `/search-documents` | Semantic search | `perform_search()` |
| `/generate-podcast` | Podcast generation | `generate_podcast()` |
| `/related-sections` | Related content | `perform_search()` |
| `/cross-connections/{id}` | Document relationships | `perform_search()` |

### Routes to HARSHALADOBE (Port 8001)

| Endpoint | Purpose | Implementation |
|----------|---------|----------------|
| `/upload-pdfs` | Document upload | Direct implementation |
| `/documents` | Document management | Direct implementation |
| `/insights` | Basic insights | Gemini AI direct |
| `/comprehensive-insights` | Detailed insights | Gemini AI direct |
| `/simplify` | Text simplification | Gemini AI direct |
| `/define-term` | Term definition | Gemini AI direct |
| `/reading-progress` | Progress tracking | Direct implementation |
| `/highlights` | Document highlighting | Direct implementation |
| `/strategic-insights` | Strategic analysis | Gemini AI direct |
| `/contextual-analysis` | Context analysis | Gemini AI direct |

## 🎯 Key Integration Features

### 1. Intelligent Fallback System

The integrated API service provides automatic fallback:

```typescript
// Example: Insights generation
async generateInsights(text, persona, jobToBeDone) {
  try {
    // First, try adobev4's analyze_and_categorize
    const analysis = await fetch(`${adobev4Url}/analyze-documents`, {
      method: 'POST',
      body: JSON.stringify({ persona, job_to_be_done: jobToBeDone })
    });
    
    if (analysis.ok) {
      return convertToInsights(analysis.data);
    }
  } catch (error) {
    // Fallback to HARSHALADOBE backend
    return this.fallbackToHarshalaInsights(text, persona, jobToBeDone);
  }
}
```

### 2. Dual Backend Health Monitoring

```typescript
async healthCheck(): Promise<{ adobev4: boolean; harshala: boolean }> {
  const adobev4Health = await fetch(`${adobev4Url}/health`).then(r => r.ok);
  const harshalaHealth = await fetch(`${harshalaUrl}/health`).then(r => r.ok);
  
  return { adobev4: adobev4Health, harshala: harshalaHealth };
}
```

### 3. Seamless Data Conversion

The integrated service converts between different response formats:

```typescript
// Convert adobev4 analysis to insights format
const insights: Insight[] = analysisData.insights.map((insight, index) => ({
  type: 'takeaway' as const,
  content: insight
}));
```

## 📁 File Structure

```
HARSHALADOBE/
├── src/
│   ├── lib/
│   │   ├── api.ts                    # Original API service
│   │   └── integrated-api.ts         # NEW: Integrated API service
│   └── components/                   # React components
├── backend/
│   ├── main.py                       # HARSHALADOBE backend (port 8001)
│   └── requirements.txt
├── start-dual-backends.bat           # NEW: Dual backend startup
├── start-dual-backends.ps1           # NEW: PowerShell startup
└── INTEGRATION_GUIDE.md              # This file

adobev4/
├── main.py                           # adobev4 backend (port 8000)
├── app.py                            # Core analysis functions
└── requirements.txt
```

## 🔧 Configuration

### Environment Variables

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8001  # Default to HARSHALADOBE backend
```

**Integrated API Service:**
```typescript
const ADOBEV4_API_URL = 'http://localhost:8000';     // adobev4 backend
const HARSHALADOBE_API_URL = 'http://localhost:8001'; // HARSHALADOBE backend
```

### Port Configuration

- **adobev4 Backend**: Port 8000
- **HARSHALADOBE Backend**: Port 8001  
- **Frontend**: Port 5173

## 🎯 Usage Examples

### 1. Using Integrated API Service

```typescript
import { integratedApiService } from '@/lib/api';

// This will route to adobev4's analyze_and_categorize
const insights = await integratedApiService.generateInsights(
  "Climate change impact on agriculture",
  "Student",
  "Research Paper"
);

// This will use HARSHALADOBE backend
const documents = await integratedApiService.getDocuments();
```

### 2. Fallback Behavior

```typescript
// If adobev4 is down, automatically falls back to HARSHALADOBE
try {
  const analysis = await integratedApiService.generateInsights(text, persona, job);
  console.log('Used adobev4 backend');
} catch (error) {
  console.log('Fell back to HARSHALADOBE backend');
}
```

### 3. Health Monitoring

```typescript
const health = await integratedApiService.healthCheck();
console.log(`adobev4: ${health.adobev4}, HARSHALADOBE: ${health.harshala}`);
```

## 🔄 Migration Guide

### From Single Backend to Integrated

1. **Update imports:**
   ```typescript
   // Old
   import { apiService } from '@/lib/api';
   
   // New (optional - for dual backend support)
   import { integratedApiService } from '@/lib/api';
   ```

2. **API calls remain the same:**
   ```typescript
   // Works with both services
   const insights = await apiService.generateInsights(text, persona, job);
   // OR
   const insights = await integratedApiService.generateInsights(text, persona, job);
   ```

3. **Start both backends:**
   ```bash
   # Use the new startup scripts
   start-dual-backends.bat
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts:**
   ```bash
   # Check if ports are in use
   netstat -ano | findstr :8000
   netstat -ano | findstr :8001
   
   # Kill processes if needed
   taskkill /PID <PID> /F
   ```

2. **Backend Not Starting:**
   ```bash
   # Check dependencies
   pip install -r requirements.txt
   
   # Check Python version
   python --version
   ```

3. **Frontend Connection Issues:**
   ```bash
   # Verify backend URLs
   curl http://localhost:8000/health
   curl http://localhost:8001/health
   ```

### Debug Mode

Enable debug logging in the integrated API service:

```typescript
// Add to integrated-api.ts
const DEBUG = true;

if (DEBUG) {
  console.log('Routing to adobev4:', endpoint);
}
```

## 📊 Performance Considerations

### Load Balancing

- **adobev4**: Handles analysis-intensive operations
- **HARSHALADOBE**: Handles document management and UI-specific features

### Caching Strategy

```typescript
// Cache analysis results
const cache = new Map();

async generateInsights(text, persona, job) {
  const key = `${text}-${persona}-${job}`;
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const result = await this.callBackend(text, persona, job);
  cache.set(key, result);
  return result;
}
```

## 🔒 Security

### CORS Configuration

Both backends are configured with CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Key Management

- **Google Gemini API**: Configured in both backends
- **AWS Credentials**: Required for podcast generation

## 🚀 Production Deployment

### Docker Setup

```dockerfile
# adobev4 backend
FROM python:3.9
WORKDIR /app
COPY adobev4/ .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "main.py"]

# HARSHALADOBE backend  
FROM python:3.9
WORKDIR /app
COPY HARSHALADOBE/backend/ .
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["python", "main.py"]
```

### Environment Configuration

```bash
# Production environment variables
ADOBEV4_API_URL=https://api.adobev4.com
HARSHALADOBE_API_URL=https://api.harshala.com
```

## 📈 Monitoring

### Health Checks

```typescript
// Regular health monitoring
setInterval(async () => {
  const health = await integratedApiService.healthCheck();
  if (!health.adobev4 || !health.harshala) {
    console.warn('Backend health issue detected');
  }
}, 30000); // Check every 30 seconds
```

### Metrics

Track API usage patterns:

```typescript
// Usage analytics
const metrics = {
  adobev4_calls: 0,
  harshala_calls: 0,
  fallbacks: 0
};
```

---

## 🎉 Summary

This integrated system provides:

✅ **Intelligent routing** - Insights → adobev4, others → HARSHALADOBE  
✅ **Automatic fallback** - Seamless failover between backends  
✅ **Unified API** - Single interface for both backends  
✅ **Health monitoring** - Real-time backend status  
✅ **Easy migration** - Minimal code changes required  

**Ready to use both backends efficiently!** 🚀
