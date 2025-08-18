# Custom Podcast Query Feature

## Overview

This feature allows users to generate podcasts from custom queries using a text input box in the podcast panel. The system uses the new `/podcast/generate` endpoint to create AI-generated audio content based on the user's query. **NEW: Text selection now automatically triggers podcast generation!** **NEW: All audio segments are automatically combined into a single seamless podcast file!**

## Features

### Frontend Changes

1. **Text Input Box**: Added a textarea in the PodcastPanel component for entering custom queries
2. **Generate Button**: New button to trigger podcast generation from the custom query
3. **Automatic Text Selection**: Selected text automatically populates podcast query and triggers generation
4. **Automatic Audio Combining**: All audio segments are automatically combined into a single file
5. **Automatic Playback**: Combined podcasts automatically start playing after generation
6. **Enhanced Audio Controls**: Full playback functionality with volume adjustment for combined audio
7. **Loading States**: Proper loading indicators during generation and combining
8. **Error Handling**: Toast notifications for success/error states

### Backend Integration

1. **New API Method**: `generatePodcastFromQuery()` in the API service
2. **FormData Support**: Uses FormData to send queries to the backend
3. **Audio URL Construction**: Properly constructs audio URLs for playback
4. **Real Audio Playback**: Uses HTML5 audio element for actual audio streaming
5. **Automatic Audio Combining**: Uses ffmpeg to combine multiple audio segments into a single file
6. **File Cleanup**: Automatically cleans up individual audio segments after combining

## Usage

### In the Frontend

#### **Automatic Text Selection (NEW!):**
1. **Select any text** in the PDF document
2. **Podcast panel automatically opens** with the selected text as the query
3. **Podcast generation starts automatically**
4. **Audio segments are automatically combined** into a single seamless file
5. **Combined audio playback begins automatically** with full volume controls
6. Use the audio player controls to pause, seek, and adjust volume

#### **Manual Query Entry:**
1. Open the Podcast Panel in the application
2. Enter your query in the text box (e.g., "Alien", "Space exploration", "Technology trends")
3. Click "Generate Podcast from Query"
4. Wait for the generation and combining to complete
5. **The combined podcast will automatically start playing** with full volume controls
6. Use the audio player controls to pause, seek, and adjust volume

### API Testing

Test the endpoint using curl:

```bash
curl -X POST -F "query=Alien" "http://127.0.0.1:8000/podcast/generate"
```

Expected response:
```json
{
  "status": "success",
  "message": "Podcast generated successfully.",
  "filename": "podcast_uuid.mp3",
  "download_url": "/audio/podcast_uuid.mp3"
}
```

## Implementation Details

### API Service Changes

```typescript
async generatePodcastFromQuery(query: string): Promise<{
  status: string;
  message: string;
  filename: string;
  download_url: string;
}> {
  const formData = new FormData();
  formData.append('query', query);

  const response = await fetch(`${this.baseUrl}/podcast/generate`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Failed to generate podcast: ${response.statusText}`);
  }

  return response.json();
}
```

### Component Changes

1. **New State Variables**:
   - `customQuery`: Stores the user's input
   - `isGeneratingFromQuery`: Loading state for query generation

2. **New Functions**:
   - `handleGenerateFromQuery()`: Handles the podcast generation from custom query
   - `handleAutoPlay()`: Automatically starts playing the generated podcast

3. **Enhanced Audio Controls**:
   - Real HTML5 audio element with proper event handling
   - Volume adjustment with mute toggle
   - Seek functionality for navigation
   - Play/pause controls
   - Progress tracking

4. **UI Elements**:
   - Textarea for query input
   - Generate button with loading state
   - Divider between query input and existing functionality
   - Full audio player controls

## Testing

Run the comprehensive test script to verify the complete functionality:

```bash
python test_combined_audio_podcast.py
```

This will test:
- Automatic podcast generation from text selection
- Selected text automatically populating podcast query
- Podcast generation starting automatically
- Audio segments being automatically combined
- Single combined audio file creation and serving
- Frontend auto-playback with combined audio
- Complete integration flow verification

## Error Handling

- Empty query validation
- Network error handling
- Backend error responses
- Loading state management

## Future Enhancements

1. **Query History**: Save and display previous queries
2. **Query Suggestions**: Auto-suggest popular queries
3. **Advanced Options**: Voice selection, duration settings
4. **Batch Generation**: Generate multiple podcasts at once
