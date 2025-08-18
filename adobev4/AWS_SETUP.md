# AWS Setup Guide for Podcast Generation

This guide will help you set up AWS credentials to use the podcast generation system with AWS Polly Text-to-Speech.

## Step 1: Create AWS Account

1. Go to [AWS Console](https://aws.amazon.com/)
2. Click "Create an AWS Account"
3. Follow the registration process
4. **Important**: You'll need a credit card, but AWS Polly has a generous free tier

## Step 2: Create IAM User

1. Log into AWS Console
2. Go to **IAM** (Identity and Access Management)
3. Click **Users** → **Create user**
4. Enter a username (e.g., "podcast-tts-user")
5. Select **Programmatic access**
6. Click **Next: Permissions**

## Step 3: Attach Permissions

1. Click **Attach existing policies directly**
2. Search for "Polly" and select **AmazonPollyFullAccess**
3. Click **Next: Tags** (optional)
4. Click **Next: Review**
5. Click **Create user**

## Step 4: Get Credentials

1. After creating the user, you'll see a success message
2. **IMPORTANT**: Click **Download .csv** to save your credentials
3. Note down your:
   - **Access Key ID**
   - **Secret Access Key**

⚠️ **Security Warning**: Keep these credentials secure and never share them!

## Step 5: Configure Credentials

Choose one of these methods:

### Method A: AWS CLI (Recommended)

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure

# Enter the following when prompted:
# AWS Access Key ID: [your_access_key]
# AWS Secret Access Key: [your_secret_key]
# Default region name: us-east-1
# Default output format: json
```

### Method B: Environment Variables

**Windows (PowerShell):**
```powershell
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
$env:AWS_DEFAULT_REGION="us-east-1"
```

**Windows (Command Prompt):**
```cmd
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=us-east-1
```

**Linux/Mac:**
```bash
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
export AWS_DEFAULT_REGION="us-east-1"
```

### Method C: Credentials File

**Windows:**
Create file: `%UserProfile%\.aws\credentials`
```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here
```

**Linux/Mac:**
Create file: `~/.aws/credentials`
```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here
```

## Step 6: Test Configuration

Test your setup:

```bash
# Test AWS CLI
aws polly describe-voices --region us-east-1

# If successful, you'll see a list of available voices
```

## Step 7: Run Podcast Generation

Now you can use the podcast generation system:

```bash
# First, index your documents
python app.py add

# Then generate a podcast
python app.py podcast "Your question here"
```

## Troubleshooting

### Common Issues:

1. **"NoCredentialsError"**
   - Solution: Check that credentials are properly configured
   - Run: `aws configure list`

2. **"AccessDenied"**
   - Solution: Ensure IAM user has Polly permissions
   - Check: IAM → Users → Your User → Permissions

3. **"Region" errors**
   - Solution: Set correct region in credentials
   - Default: `us-east-1`

### Cost Information:

- **AWS Polly Free Tier**: 5 million characters per month
- **Neural Voices**: $4.00 per 1 million characters
- **Standard Voices**: $4.00 per 1 million characters

A typical 3-minute podcast uses about 2,000-3,000 characters, so you can generate hundreds of podcasts within the free tier.

## Security Best Practices

1. **Never commit credentials to version control**
2. **Use IAM roles when possible**
3. **Rotate access keys regularly**
4. **Use least privilege principle**
5. **Monitor usage in AWS Console**

## Support

If you encounter issues:
1. Check AWS Console → CloudTrail for error logs
2. Verify IAM permissions
3. Test with AWS CLI first
4. Check region settings
