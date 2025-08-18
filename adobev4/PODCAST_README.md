# 🎙️ Podcast Generation System

This system transforms your documents into engaging podcast episodes using AI-powered analysis and text-to-speech technology.

## Features

- **Document Analysis**: Automatically analyzes your documents for relevant content
- **Script Generation**: Creates natural conversations between two speakers (Alex & Dr. Sharma)
- **Audio Generation**: Converts scripts to high-quality MP3 audio using Google Text-to-Speech
- **Multi-format Support**: Works with PDF, DOCX, and TXT files

## Prerequisites

### 1. AWS Setup
You need an AWS account and credentials for the Polly Text-to-Speech service:

1. **Create AWS Account**:
   - Sign up at [AWS Console](https://aws.amazon.com/)
   - Create an IAM user with Polly permissions

2. **Configure AWS Credentials** (choose one method):
   
   **Method A: AWS CLI**
   ```bash
   pip install awscli
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and region
   ```
   
   **Method B: Environment Variables**
   ```bash
   # Windows (PowerShell)
   $env:AWS_ACCESS_KEY_ID="your_access_key"
   $env:AWS_SECRET_ACCESS_KEY="your_secret_key"
   $env:AWS_DEFAULT_REGION="us-east-1"
   ```
   
   **Method C: Credentials File**
   Create `~/.aws/credentials` (Windows: `%UserProfile%\.aws\credentials`):
   ```ini
   [default]
   aws_access_key_id = your_access_key
   aws_secret_access_key = your_secret_key
   ```

3. **Enable Polly Service**:
   - Polly is enabled by default in AWS
   - No additional setup required

### 2. Python Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```

## Quick Start

### Step 1: Add Documents
Place your documents in the `documents/` folder and index them:
```bash
python app.py add
```

### Step 2: Generate a Podcast
```bash
python app.py podcast "Your question here"
```

### Example
```bash
python app.py podcast "Is colonizing Mars a good idea?"
```

## How It Works

### Stage 1: Document Analysis
- Searches your documents for relevant passages
- Categorizes content as Agreement, Conflict, Illustrative Example, or Related Point
- Uses Gemini AI for intelligent analysis

### Stage 2: Script Generation
- Creates a 2-3 minute podcast script
- Features two speakers:
  - **Alex (Host)**: Asks questions and guides the conversation
  - **Dr. Sharma (Expert)**: Provides detailed, fact-based answers
- Script is grounded in your actual document content

### Stage 3: Audio Generation
- Converts script to audio using Google Text-to-Speech
- Uses different voices for each speaker
- Exports as MP3 file

## File Structure

```
test123/
├── app.py                 # Main application
├── demo.py               # Demo script
├── documents/            # Your documents (PDF, DOCX, TXT)
├── index/               # Search index (auto-generated)
├── podcast_output.mp3   # Generated podcast (output)
└── requirements.txt     # Python dependencies
```

## Commands

| Command | Description |
|---------|-------------|
| `python app.py add` | Index documents from the `documents/` folder |
| `python app.py search "query"` | Basic document search |
| `python app.py analyze "query"` | Advanced analysis with categorization |
| `python app.py podcast "query"` | Generate a complete podcast |

## Demo Script

Run the demo to test the system:
```bash
python demo.py
```

This will:
1. Use a sample query about Mars colonization
2. Generate a podcast script
3. Create an audio file (`demo_podcast.mp3`)

## Troubleshooting

### Common Issues

1. **AWS Authentication Error**:
   ```
   ❌ An error occurred during audio generation
   ```
   **Solution**: Configure AWS credentials using `aws configure` or set environment variables

2. **No Documents Found**:
   ```
   ❌ No search results found
   ```
   **Solution**: Add documents to the `documents/` folder and run `python app.py add`

3. **API Key Issues**:
   ```
   ❌ Error during analysis
   ```
   **Solution**: Check your Google API key in `app.py`

### Getting Help

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Google Cloud authentication: `gcloud auth list`
- Verify API is enabled in Google Cloud Console
- Check document format (PDF, DOCX, TXT only)

## Advanced Usage

### Custom Output Filename
```bash
python app.py podcast "Your query" --output "my_podcast.mp3"
```

### Programmatic Usage
```python
from app import generate_podcast

success = generate_podcast("Your question here", "output.mp3")
if success:
    print("Podcast generated successfully!")
```

## Technical Details

- **Embedding Model**: SentenceTransformer 'all-MiniLM-L6-v2'
- **AI Model**: Google Gemini 1.5 Flash
- **TTS Service**: AWS Polly (Neural Engine)
- **Audio Format**: MP3
- **Voice Options**: 
  - Alex: Matthew (Male, Neural)
  - Dr. Sharma: Joanna (Female, Neural)

## License

This project uses various open-source libraries. Please check individual library licenses.
