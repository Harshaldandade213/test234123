# Gemini API Setup Guide

## ✅ API Key Updated

Your new Gemini API key has been successfully added to the system:

**API Key**: `AIzaSyAEYT0RCElrr1U__4uAKIV0XpJ41Dum6ro`

## 📝 What Was Updated

1. **`backend/app/llm_services.py`** - Updated default API key
2. **`backend/app/document_intelligence.py`** - Updated default API key
3. **Created setup scripts** for easy configuration

## 🚀 Quick Setup

### Option 1: Automatic Setup (Recommended)
```bash
cd HARSHALADOBE/backend
python setup_env.py
```

### Option 2: Manual Setup
1. Create a `.env` file in `HARSHALADOBE/backend/`
2. Add this line:
   ```
   GEMINI_API_KEY=AIzaSyAEYT0RCElrr1U__4uAKIV0XpJ41Dum6ro
   ```

## 🧪 Test Your Setup

Run the test script to verify everything is working:

```bash
cd HARSHALADOBE/backend
python test_gemini_api.py
```

## 🎙️ Test Podcast Generation

1. **Start your backend server**:
   ```bash
   cd HARSHALADOBE/backend
   python start.py
   ```

2. **Start your frontend**:
   ```bash
   cd HARSHALADOBE
   npm run dev
   ```

3. **Test the podcast feature**:
   - Open the app in your browser
   - Upload a PDF or go to the podcast panel
   - Try pasting a query like: "Explain artificial intelligence"
   - The system should automatically generate a podcast

## 🔧 Troubleshooting

### If you get quota errors:
- The new API key should have fresh quota
- Wait a few minutes if you've been testing extensively
- Check the API key is correct

### If the backend won't start:
- Make sure you're in the correct directory
- Check that all dependencies are installed
- Verify the `.env` file exists and has the correct API key

### If podcast generation fails:
- Check the backend logs for error messages
- Verify the API key is being loaded correctly
- Try the test script to isolate the issue

## 📋 Features Now Available

With the new API key, you can use:

- ✅ **Podcast Generation from Queries** - Paste any text and generate podcasts
- ✅ **AI Insights** - Get intelligent analysis of your documents
- ✅ **Document Intelligence** - Advanced document processing
- ✅ **Cross-document Connections** - Find relationships between documents
- ✅ **Strategic Insights** - Get actionable recommendations

## 🎯 Next Steps

1. **Test the podcast feature** by pasting queries
2. **Upload some PDFs** and test the AI insights
3. **Try the cross-document analysis** if you have multiple documents
4. **Explore all the AI-powered features** in the interface

## 📞 Support

If you encounter any issues:
1. Check the backend logs for error messages
2. Run the test script to verify API connectivity
3. Ensure all environment variables are set correctly

---

**Happy podcasting! 🎙️✨**
