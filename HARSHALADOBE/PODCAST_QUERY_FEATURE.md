# Podcast Query Feature

## Overview

The Podcast Query feature allows users to manually paste or type any query and automatically generate a podcast about that topic. This feature is available in the Podcast Panel component.

## How to Use

### 1. Access the Podcast Panel
- Open the right sidebar in the PDF reader
- Click on the "Podcast" tab
- You'll see the "Generate Podcast from Query" section

### 2. Enter Your Query
You can:
- **Type** any topic or question
- **Paste** text from anywhere (articles, notes, etc.)
- **Use example queries** like:
  - "Explain quantum computing in simple terms"
  - "What are the latest developments in renewable energy?"
  - "How does machine learning impact healthcare?"
  - "Discuss the future of remote work"
  - "What are the environmental impacts of electric vehicles?"

### 3. Auto-Generation
- The system automatically generates a podcast when you paste or type substantial text (10+ characters)
- You'll see a green indicator when ready to auto-generate
- An orange indicator shows when you need more text

### 4. Manual Generation
- Click the "Generate Podcast Now" button to manually trigger generation
- Use the "✕" button to clear your query

## Features

### Auto-Generation
- **Paste Detection**: Automatically detects when you paste text
- **Smart Threshold**: Requires minimum 10 characters to prevent accidental generation
- **Visual Feedback**: Color-coded indicators show generation status

### Audio Controls
- **Play/Pause**: Control podcast playback
- **Skip Controls**: Jump forward/backward 15 seconds
- **Volume Control**: Adjust audio volume
- **Progress Bar**: See playback progress
- **Transcript**: View the generated script

### File Management
- **Unique Filenames**: Each generated podcast gets a unique timestamp
- **Audio Cache**: Files are stored locally for quick access
- **Download**: Save podcasts for offline listening

## Technical Implementation

### Frontend (PodcastPanel.tsx)
- Textarea with paste detection
- Auto-generation triggers
- Visual status indicators
- Audio player controls
- Transcript display

### Backend API
- **Endpoint**: `POST /podcast/generate`
- **Input**: Form data with query string
- **Output**: Audio file URL and metadata

### LLM Service
- **Method**: `generate_podcast_script_from_query(query: str)`
- **Prompt**: Creates engaging 2-5 minute podcast scripts
- **Features**: Conversational tone, educational content, proper pacing

### TTS Service
- **Audio Generation**: Converts script to speech
- **File Management**: Creates unique filenames
- **Cache Storage**: Stores audio files locally

## Example Usage

### Basic Query
```
Query: "Explain artificial intelligence"
Result: 3-minute podcast about AI basics, applications, and future implications
```

### Complex Topic
```
Query: "How does climate change affect global food security?"
Result: 4-minute podcast exploring climate impacts on agriculture, food systems, and solutions
```

### Technical Subject
```
Query: "What is blockchain technology and how does it work?"
Result: 3-minute podcast explaining blockchain concepts, use cases, and real-world applications
```

## Error Handling

- **Empty Query**: Shows error message requiring input
- **Generation Failure**: Graceful fallback with error notification
- **Audio Playback Issues**: Browser TTS fallback if available
- **Network Issues**: Clear error messages and retry options

## Future Enhancements

- **Voice Selection**: Choose different AI voices
- **Podcast Templates**: Different styles (news, educational, conversational)
- **Multi-language Support**: Generate podcasts in different languages
- **Podcast Series**: Create connected episodes on related topics
- **Export Options**: Save as MP3, WAV, or other formats
- **Sharing**: Share podcasts via links or social media

## Troubleshooting

### Podcast Won't Generate
1. Check if query has at least 10 characters
2. Verify backend service is running
3. Check browser console for errors
4. Try refreshing the page

### Audio Won't Play
1. Check volume settings
2. Verify audio file was generated
3. Try downloading the file directly
4. Check browser audio permissions

### Slow Generation
1. Complex queries may take longer
2. Check network connection
3. Server may be processing other requests
4. Try a simpler query first
