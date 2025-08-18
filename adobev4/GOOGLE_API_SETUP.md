# Google API Key Setup Guide

## Overview
The enhanced related sections functionality and other AI-powered features require a Google API key to access the Google Gemini Flash API. This guide will walk you through the process of obtaining and configuring your API key.

## Step 1: Get Google API Key

### Option A: Google AI Studio (Recommended)
1. **Visit Google AI Studio**: Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. **Sign In**: Use your Google account to sign in
3. **Create API Key**: Click "Create API Key" button
4. **Copy the Key**: Your API key will be displayed (starts with "AIza...")
5. **Save Securely**: Copy and save this key in a secure location

### Option B: Google Cloud Console
1. **Visit Google Cloud Console**: Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. **Create/Select Project**: Create a new project or select an existing one
3. **Enable Gemini API**: Go to "APIs & Services" > "Library" and search for "Gemini API"
4. **Enable the API**: Click "Enable"
5. **Create Credentials**: Go to "APIs & Services" > "Credentials"
6. **Create API Key**: Click "Create Credentials" > "API Key"
7. **Copy the Key**: Your API key will be displayed

## Step 2: Set Environment Variable

### Windows (PowerShell)
```powershell
# Set the environment variable
$env:GOOGLE_API_KEY="your_api_key_here"

# To make it permanent (optional)
[Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", "your_api_key_here", "User")
```

### Windows (Command Prompt)
```cmd
# Set the environment variable
set GOOGLE_API_KEY=your_api_key_here

# To make it permanent (optional)
setx GOOGLE_API_KEY "your_api_key_here"
```

### Linux/Mac
```bash
# Set the environment variable
export GOOGLE_API_KEY="your_api_key_here"

# To make it permanent, add to ~/.bashrc or ~/.zshrc
echo 'export GOOGLE_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

## Step 3: Verify Setup

### Test the API Key
Run this Python script to verify your API key works:

```python
import os
import google.generativeai as genai

# Check if API key is set
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ GOOGLE_API_KEY environment variable not set")
    exit(1)

# Configure the API
genai.configure(api_key=api_key)

try:
    # Test with a simple request
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, this is a test.")
    print("✅ Google API key is working correctly!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error testing API key: {e}")
```

### Save as test_api_key.py
```bash
# Create and run the test script
echo 'import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    exit(1)

genai.configure(api_key=api_key)
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Test message")
    print("✅ API key working!")
except Exception as e:
    print(f"❌ Error: {e}")' > test_api_key.py

python test_api_key.py
```

## Step 4: Alternative Setup Methods

### Method 1: .env File (Recommended for Development)
1. Create a `.env` file in the `adobev4` directory:
```bash
# adobev4/.env
GOOGLE_API_KEY=your_api_key_here
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Update `main.py` to load from .env file:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Method 2: Direct Configuration
If you prefer to set the API key directly in the code (not recommended for production):

```python
import google.generativeai as genai
genai.configure(api_key="your_api_key_here")
```

## Step 5: Security Best Practices

### ✅ Do's
- Keep your API key secure and private
- Use environment variables
- Set up API key restrictions in Google Cloud Console
- Monitor your API usage
- Use .env files for development (add to .gitignore)

### ❌ Don'ts
- Never commit API keys to version control
- Don't share API keys publicly
- Don't hardcode keys in production code
- Don't use the same key for multiple applications

## Step 6: API Key Restrictions (Optional but Recommended)

1. **Go to Google Cloud Console**: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. **Navigate to APIs & Services > Credentials**
3. **Find your API key and click on it**
4. **Set Application restrictions**:
   - Choose "HTTP referrers" for web apps
   - Choose "IP addresses" for server apps
5. **Set API restrictions**:
   - Select "Restrict key"
   - Choose "Gemini API" from the list

## Troubleshooting

### Common Issues

**Issue**: "API key not found"
- **Solution**: Make sure the environment variable is set correctly
- **Check**: Run `echo $GOOGLE_API_KEY` (Linux/Mac) or `echo %GOOGLE_API_KEY%` (Windows)

**Issue**: "Invalid API key"
- **Solution**: Verify the key is copied correctly from Google AI Studio
- **Check**: Ensure no extra spaces or characters

**Issue**: "Quota exceeded"
- **Solution**: Check your usage in Google Cloud Console
- **Alternative**: Create a new API key or wait for quota reset

**Issue**: "API not enabled"
- **Solution**: Enable the Gemini API in Google Cloud Console
- **Steps**: Go to APIs & Services > Library > Search "Gemini API" > Enable

## Next Steps

Once you have your Google API key set up:

1. **Test the key** using the verification script above
2. **Start the backend server**: `cd adobev4; python main.py`
3. **Run the tests**: `python run_all_tests.py`
4. **Test related sections**: Upload a document and test the enhanced functionality

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your API key is valid and has proper permissions
3. Ensure the Gemini API is enabled in your Google Cloud project
4. Check your internet connection and firewall settings
