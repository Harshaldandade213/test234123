# Simplify Text Integration

## Overview
The Simplify Text feature allows users to select text from PDF documents and automatically simplify it using AI. The feature is fully integrated between the frontend and backend, providing a seamless user experience.

## Key Features

### 🎯 **Text Selection Integration**
- Users can select text directly from PDF documents
- Selected text is automatically passed to the Text Simplifier component
- Real-time text processing with visual feedback

### 🤖 **AI-Powered Simplification**
- Uses Google Gemini AI for intelligent text simplification
- Maintains core meaning while making text easier to understand
- Handles complex technical and academic content

### 🎨 **User Interface**
- Clean, modern interface with difficulty level selection
- Real-time loading states and error handling
- Copy and reset functionality for simplified text

## Technical Implementation

### Backend (`adobev4/main.py`)

#### Endpoint: `POST /simplify`
```python
@app.post("/simplify")
async def simplify_text_endpoint(request: SimplifyTextRequest):
    """Simplify text difficulty using AI"""
    try:
        text = request.text
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Use Gemini to simplify text
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Simplify the following text to make it easier to understand while maintaining the core meaning:
        
        {text}
        
        Return only the simplified text without any additional formatting or explanations.
        """
        
        response = model.generate_content(prompt)
        simplified_text = response.text.strip()
        
        return {
            "text": simplified_text,
            "original": text
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for empty text)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to simplify text: {str(e)}")
```

#### Request Model
```python
class SimplifyTextRequest(BaseModel):
    text: str
```

#### Response Format
```json
{
  "text": "Simplified version of the text",
  "original": "Original text that was submitted"
}
```

### Frontend Integration

#### API Service (`HARSHALADOBE/src/lib/api.ts`)
```typescript
async simplifyText(text: string): Promise<SimplifiedText> {
  const response = await fetch(`${this.baseUrl}/simplify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error(`Failed to simplify text: ${response.statusText}`);
  }

  return response.json();
}
```

#### TextSimplifier Component (`HARSHALADOBE/src/components/TextSimplifier.tsx`)
```typescript
interface TextSimplifierProps {
  originalText?: string;
  onSimplifiedText?: (text: string) => void;
}

export function TextSimplifier({ originalText, onSimplifiedText }: TextSimplifierProps) {
  const [simplifiedText, setSimplifiedText] = useState<string>('');
  const [isSimplifying, setIsSimplifying] = useState(false);
  
  const handleSimplify = async () => {
    if (!originalText?.trim()) {
      toast({
        title: "No text to simplify",
        description: "Please provide text to simplify.",
        variant: "destructive"
      });
      return;
    }

    setIsSimplifying(true);
    try {
      const result = await apiService.simplifyText(originalText);
      setSimplifiedText(result.text);
      
      if (onSimplifiedText) {
        onSimplifiedText(result.text);
      }
      
      toast({
        title: "Text simplified",
        description: `Successfully simplified text.`
      });
      
    } catch (error) {
      console.error('Failed to simplify text:', error);
      toast({
        title: "Simplification failed",
        description: "Unable to simplify text. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsSimplifying(false);
    }
  };
  
  // ... rest of component
}
```

#### PDFReader Integration (`HARSHALADOBE/src/components/PDFReader.tsx`)
```typescript
// Text selection handler
const handleTextSelection = async (text: string, page: number) => {
  console.log('Text selected:', text, 'on page:', page);
  setSelectedText(text);
  setCurrentPage(page);
  
  // Always open right panel when text is selected
  setRightPanelOpen(true);
  
  // ... other logic
};

// TextSimplifier component usage
{activeRightPanel === 'simplifier' && (
  <div className="min-w-0 overflow-hidden h-full">
    <TextSimplifier 
      originalText={selectedText || getCurrentSectionTitle()}
      onSimplifiedText={(text) => console.log('Simplified:', text)}
    />
  </div>
)}
```

## User Experience Flow

### 1. **Text Selection**
- User selects text in the PDF viewer
- Selected text is automatically captured
- Right panel opens with the Text Simplifier

### 2. **Simplification Process**
- User clicks "Simplify Text" button
- Loading state is shown with spinner
- AI processes the text in the background

### 3. **Results Display**
- Simplified text appears in the results box
- Original text is preserved for reference
- Copy and reset options are available

### 4. **Error Handling**
- Empty text validation with user-friendly messages
- Network error handling with retry options
- API error messages displayed to user

## Testing

### Automated Testing
Run the integration test:
```bash
cd adobev4
python test_simplify_integration.py
```

### Manual Testing
1. Start the backend server:
   ```bash
   cd adobev4
   python main.py
   ```

2. Start the frontend:
   ```bash
   cd HARSHALADOBE
   npm run dev
   ```

3. Test the feature:
   - Upload a PDF document
   - Select text from the document
   - Open the Text Simplifier panel
   - Click "Simplify Text"
   - Verify the simplified result

## Error Handling

### Backend Errors
- **400 Bad Request**: Empty or invalid text
- **500 Internal Server Error**: AI processing failure
- **429 Too Many Requests**: API rate limiting

### Frontend Errors
- Network connectivity issues
- Invalid response format
- User input validation

## Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for Gemini AI access
- `API_BASE_URL`: Backend server URL (default: http://localhost:8000)

### AI Model Configuration
- Model: `gemini-1.5-flash-latest`
- Prompt: Optimized for text simplification while preserving meaning
- Response: Clean text without additional formatting

## Performance Considerations

### Backend
- Async processing to prevent blocking
- Error handling for API rate limits
- Response caching for repeated requests

### Frontend
- Loading states for better UX
- Error boundaries for component stability
- Optimistic updates for faster perceived performance

## Future Enhancements

### Potential Improvements
1. **Difficulty Levels**: Add different simplification levels (simple, moderate, advanced)
2. **Batch Processing**: Allow multiple text selections to be simplified at once
3. **Custom Prompts**: Let users specify simplification criteria
4. **History**: Save simplified text history for reference
5. **Export Options**: Export simplified text to various formats

### Technical Enhancements
1. **Caching**: Cache simplified results to reduce API calls
2. **Offline Mode**: Basic simplification without AI when offline
3. **Progressive Enhancement**: Fallback to simpler methods if AI fails
4. **Analytics**: Track usage patterns for optimization

## Troubleshooting

### Common Issues

#### Backend Not Responding
```bash
# Check if server is running
curl http://localhost:8000/health

# Start server if needed
cd adobev4
python main.py
```

#### API Key Issues
```bash
# Check environment variable
echo $GOOGLE_API_KEY

# Set if missing
export GOOGLE_API_KEY="your-api-key-here"
```

#### Frontend Integration Issues
1. Check browser console for errors
2. Verify API service configuration
3. Ensure CORS is properly configured
4. Check network connectivity

### Debug Mode
Enable debug logging in the backend:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

### Input Validation
- Text length limits to prevent abuse
- Content filtering for inappropriate text
- Rate limiting per user/IP

### API Security
- Secure API key storage
- Request authentication (future enhancement)
- Input sanitization

## Conclusion

The Simplify Text integration provides a powerful, user-friendly feature that enhances document comprehension. The seamless integration between frontend and backend ensures a smooth user experience while maintaining robust error handling and performance optimization.

The feature is production-ready and can be easily extended with additional functionality as needed.
