# Adobe V4 Environment Configuration Guide

This guide explains how to set up and configure the environment variables for the Adobe V4 project.

## 📁 Files Created

1. **`.env`** - Environment variables file (not committed to Git)
2. **`config.py`** - Configuration management module
3. **`setup_env.py`** - Interactive setup script
4. **`ENV_SETUP_README.md`** - This guide

## 🚀 Quick Setup

### Option 1: Interactive Setup (Recommended)

Run the interactive setup script:

```bash
cd adobev4
python setup_env.py
```

This script will:
- Install required dependencies
- Guide you through entering your API keys
- Create the `.env` file automatically
- Validate the configuration

### Option 2: Manual Setup

1. **Install python-dotenv:**
   ```bash
   pip install python-dotenv
   ```

2. **Edit the `.env` file:**
   Replace the placeholder values with your actual credentials:

   ```env
   # Google API Key (Required)
   GOOGLE_API_KEY=your_actual_google_api_key_here
   
   # Azure Speech Services (Required)
   AZURE_SPEECH_KEY=your_actual_azure_speech_key_here
   AZURE_SPEECH_REGION=centralindia
   
   # AWS Configuration (Optional)
   AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
   AWS_REGION=us-east-1
   ```

## 🔑 Required API Keys

### 1. Google API Key

**Purpose:** Used for Google Gemini AI text generation and analysis.

**How to get it:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the "Generative Language API"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key

**Environment Variable:** `GOOGLE_API_KEY`

### 2. Azure Speech Services

**Purpose:** Used for Text-to-Speech (TTS) functionality.

**How to get it:**
1. Go to [Azure Portal](https://portal.azure.com/)
2. Create a new "Speech Service" resource
3. Go to "Keys and Endpoint"
4. Copy Key 1 or Key 2
5. Note the region (e.g., "centralindia")

**Environment Variables:**
- `AZURE_SPEECH_KEY` - Your Azure Speech API key
- `AZURE_SPEECH_REGION` - Your Azure region (e.g., "centralindia")

### 3. AWS Credentials (Optional)

**Purpose:** Alternative TTS provider using Amazon Polly.

**How to get it:**
1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Create an IAM user with Polly permissions
3. Generate Access Key ID and Secret Access Key

**Environment Variables:**
- `AWS_ACCESS_KEY_ID` - Your AWS Access Key ID
- `AWS_SECRET_ACCESS_KEY` - Your AWS Secret Access Key
- `AWS_REGION` - Your AWS region (e.g., "us-east-1")

## ⚙️ Configuration Options

### Application Settings

```env
# TTS Provider ('azure' or 'aws')
TTS_PROVIDER=azure

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# File Upload Limits
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=pdf,docx,txt

# Document Processing
MAX_CHUNK_SIZE=200
CHUNK_OVERLAP=50
MIN_CHUNK_LENGTH=50
```

### Security Settings

```env
# Secret key for sessions (auto-generated)
SECRET_KEY=your_secret_key_here

# CORS allowed origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000
```

### Storage Settings

```env
# Directory paths
DOCUMENTS_DIR=documents
AUDIO_DIR=audio
INDEX_DIR=index
UPLOADS_DIR=uploads
```

### AI Model Settings

```env
# Embedding model for semantic search
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Gemini model for text generation
GEMINI_MODEL=gemini-1.5-flash
```

## 🔧 Using the Configuration

### In Your Code

```python
from config import config

# Access configuration values
api_key = config.GOOGLE_API_KEY
azure_key = config.AZURE_SPEECH_KEY
port = config.PORT

# Validate configuration
if config.validate_config():
    print("Configuration is valid!")
else:
    print("Configuration validation failed!")
```

### Validation

Run the configuration validation:

```bash
python config.py
```

This will show:
- ✅/❌ Status for each required variable
- Current configuration summary
- Any missing or invalid settings

## 🛡️ Security Best Practices

1. **Never commit `.env` files to Git**
   - The `.env` file is already in `.gitignore`
   - Use `.env.example` for sharing configuration structure

2. **Use different keys for development and production**
   - Create separate API keys for different environments
   - Use environment-specific `.env` files

3. **Rotate API keys regularly**
   - Set up reminders to rotate keys every 90 days
   - Monitor API usage for unexpected charges

4. **Limit API key permissions**
   - Only grant necessary permissions to API keys
   - Use service accounts with minimal privileges

## 🚨 Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Check that your `.env` file exists in the `adobev4` directory
   - Verify all required variables are set
   - Run `python config.py` to see what's missing

2. **"Invalid API key"**
   - Verify your API keys are correct
   - Check if the APIs are enabled in your cloud console
   - Ensure you have sufficient quota/credits

3. **"Module not found: dotenv"**
   - Install python-dotenv: `pip install python-dotenv`

4. **"Permission denied"**
   - Check file permissions on the `.env` file
   - Ensure the application can read the file

### Validation Commands

```bash
# Check configuration
python config.py

# Test Google API
python test_api_key.py

# Test Azure Speech
python test_azure_credentials.py

# Run setup again
python setup_env.py
```

## 📝 Environment Variables Reference

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GOOGLE_API_KEY` | ✅ | Google Gemini API key | - |
| `AZURE_SPEECH_KEY` | ✅ | Azure Speech API key | - |
| `AZURE_SPEECH_REGION` | ✅ | Azure region | centralindia |
| `AWS_ACCESS_KEY_ID` | ❌ | AWS Access Key ID | - |
| `AWS_SECRET_ACCESS_KEY` | ❌ | AWS Secret Access Key | - |
| `AWS_REGION` | ❌ | AWS region | us-east-1 |
| `TTS_PROVIDER` | ❌ | TTS provider (azure/aws) | azure |
| `HOST` | ❌ | Server host | 0.0.0.0 |
| `PORT` | ❌ | Server port | 8000 |
| `DEBUG` | ❌ | Debug mode | False |
| `SECRET_KEY` | ❌ | Secret key for sessions | auto-generated |
| `ALLOWED_ORIGINS` | ❌ | CORS allowed origins | localhost URLs |

## 🎯 Next Steps

After setting up your environment:

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Or use uvicorn:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

4. **Test the setup:**
   - Upload a document
   - Generate audio
   - Test the API endpoints

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the validation commands
3. Review the error logs
4. Ensure all dependencies are installed

For additional help, check the main project documentation or create an issue in the repository.
