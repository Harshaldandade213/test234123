"""
Configuration module for Adobe V4
Loads environment variables and provides centralized configuration management.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Adobe V4 application."""
    
    # =============================================================================
    # GOOGLE API CONFIGURATION
    # =============================================================================
    GOOGLE_API_KEY: str = os.getenv('GOOGLE_API_KEY', 'AIzaSyB3RHGywLeBmdN485INVuoZNgRtV-1LbrI')
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', 'AIzaSyB3RHGywLeBmdN485INVuoZNgRtV-1LbrI')
    
    # =============================================================================
    # AZURE SPEECH SERVICES CONFIGURATION
    # =============================================================================
    AZURE_SPEECH_KEY: str = os.getenv('AZURE_SPEECH_KEY', '')
    AZURE_SPEECH_REGION: str = os.getenv('AZURE_SPEECH_REGION', 'centralindia')
    
    # =============================================================================
    # AWS CONFIGURATION
    # =============================================================================
    AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_REGION: str = os.getenv('AWS_REGION', 'us-east-1')
    
    # =============================================================================
    # APPLICATION CONFIGURATION
    # =============================================================================
    TTS_PROVIDER: str = os.getenv('TTS_PROVIDER', 'azure')
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8080'))  # Changed from 8000 to 8080
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB
    ALLOWED_EXTENSIONS: str = os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx,txt')
    
    # Document Processing Configuration
    MAX_CHUNK_SIZE: int = int(os.getenv('MAX_CHUNK_SIZE', '200'))
    CHUNK_OVERLAP: int = int(os.getenv('CHUNK_OVERLAP', '50'))
    MIN_CHUNK_LENGTH: int = int(os.getenv('MIN_CHUNK_LENGTH', '50'))
    
    # =============================================================================
    # SECURITY CONFIGURATION
    # =============================================================================
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
    ALLOWED_ORIGINS: str = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000')
    
    # =============================================================================
    # LOGGING CONFIGURATION
    # =============================================================================
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'adobev4.log')
    
    # =============================================================================
    # STORAGE CONFIGURATION
    # =============================================================================
    DOCUMENTS_DIR: str = os.getenv('DOCUMENTS_DIR', 'documents')
    AUDIO_DIR: str = os.getenv('AUDIO_DIR', 'audio')
    INDEX_DIR: str = os.getenv('INDEX_DIR', 'index')
    UPLOADS_DIR: str = os.getenv('UPLOADS_DIR', 'uploads')
    
    # =============================================================================
    # AI MODEL CONFIGURATION
    # =============================================================================
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # =============================================================================
    # PERFORMANCE CONFIGURATION
    # =============================================================================
    WORKERS: int = int(os.getenv('WORKERS', '4'))
    EMBEDDINGS_CACHE_SIZE: int = int(os.getenv('EMBEDDINGS_CACHE_SIZE', '1000'))
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv('MAX_CONCURRENT_REQUESTS', '10'))
    
    # =============================================================================
    # DEVELOPMENT CONFIGURATION
    # =============================================================================
    DEVELOPMENT_MODE: bool = os.getenv('DEVELOPMENT_MODE', 'True').lower() == 'true'
    VERBOSE_LOGGING: bool = os.getenv('VERBOSE_LOGGING', 'False').lower() == 'true'
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present."""
        required_vars = [
            'GOOGLE_API_KEY',
            'GEMINI_API_KEY',
            'AZURE_SPEECH_KEY',
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print("📝 Please check your .env file and ensure all required variables are set.")
            return False
        
        print("✅ Configuration validation passed")
        return True
    
    @classmethod
    def print_config_summary(cls):
        """Print a summary of the current configuration."""
        print("\n" + "="*60)
        print("ADOBE V4 CONFIGURATION SUMMARY")
        print("="*60)
        
        print(f"🔑 Google API Key: {'✅ Set' if cls.GOOGLE_API_KEY else '❌ Missing'}")
        print(f"🤖 Gemini API Key: {'✅ Set' if cls.GEMINI_API_KEY else '❌ Missing'}")
        print(f"🔊 Azure Speech Key: {'✅ Set' if cls.AZURE_SPEECH_KEY else '❌ Missing'}")
        print(f"🌍 Azure Region: {cls.AZURE_SPEECH_REGION}")
        print(f"🎤 TTS Provider: {cls.TTS_PROVIDER}")
        print(f"🌐 Server: {cls.HOST}:{cls.PORT}")
        print(f"🐛 Debug Mode: {cls.DEBUG}")
        print(f"📁 Documents Dir: {cls.DOCUMENTS_DIR}")
        print(f"📁 Audio Dir: {cls.AUDIO_DIR}")
        print(f"📁 Index Dir: {cls.INDEX_DIR}")
        print(f"🤖 Embedding Model: {cls.EMBEDDING_MODEL}")
        print(f"🤖 Gemini Model: {cls.GEMINI_MODEL}")
        print(f"⚙️ Workers: {cls.WORKERS}")
        print(f"🔧 Development Mode: {cls.DEVELOPMENT_MODE}")
        print("="*60)
    
    @classmethod
    def get_allowed_extensions_list(cls) -> list:
        """Get list of allowed file extensions."""
        return [ext.strip() for ext in cls.ALLOWED_EXTENSIONS.split(',')]
    
    @classmethod
    def get_allowed_origins_list(cls) -> list:
        """Get list of allowed CORS origins."""
        return [origin.strip() for origin in cls.ALLOWED_ORIGINS.split(',')]

# Create a global config instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance."""
    return config

def validate_and_print_config():
    """Validate configuration and print summary."""
    config.print_config_summary()
    return config.validate_config()

if __name__ == "__main__":
    # Test configuration when run directly
    validate_and_print_config()
