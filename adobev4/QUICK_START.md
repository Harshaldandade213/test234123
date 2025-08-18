# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Setup (One-time)
```bash
python setup.py
```

### 2. Add Your Documents
- Place PDF, DOCX, or TXT files in the `documents/` folder
- Run: `python app.py add`

### 3. Search Your Documents
```bash
python app.py search "your search query here"
```

## 📁 What You Have

- **`app.py`** - Main application with CLI interface
- **`documents/`** - Put your files here
- **`index/`** - Auto-generated search index (don't delete)
- **`demo.py`** - Run `python demo.py` to see it in action
- **`setup.py`** - One-click setup script

## 🔍 Example Searches

```bash
# Search for specific topics
python app.py search "machine learning types"
python app.py search "supervised learning algorithms"
python app.py search "healthcare applications"

# Search for concepts (semantic search)
python app.py search "data quality issues"
python app.py search "neural networks deep learning"
```

## ✨ Key Features

- **Smart**: Finds conceptually similar content, not just keywords
- **Fast**: Once indexed, searches are instant
- **Incremental**: Only processes new files when you run `add`
- **Multi-format**: Supports PDF, Word, and text files
- **Persistent**: Index is saved and reused

## 🛠️ Adding More Documents

1. Drop new files into `documents/` folder
2. Run: `python app.py add`
3. That's it! The system automatically detects new files

## 📊 Current Status

✅ **System Ready**: All dependencies installed  
✅ **Index Created**: Sample document processed  
✅ **Search Working**: Tested with multiple queries  

Your semantic search system is ready to use!
