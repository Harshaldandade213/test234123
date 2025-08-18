#!/usr/bin/env python3
"""
FastAPI Server Startup Script
This script starts the FastAPI backend server with proper configuration.
"""

import uvicorn
import os
import sys

def main():
    """Start the FastAPI server"""
    print("🚀 Starting Document Analysis & Podcast Generation API Server")
    print("=" * 60)
    
    # Check if required directories exist
    required_dirs = ["documents", "index", "audio"]
    for dir_name in required_dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Ensured directory exists: {dir_name}")
    
    # Configuration
    host = "0.0.0.0"
    port = 8000
    reload = True  # Enable auto-reload for development
    
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation will be at: http://{host}:{port}/docs")
    print(f"🔧 Auto-reload: {'Enabled' if reload else 'Disabled'}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
