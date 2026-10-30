"""
Application configuration management using environment variables.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Global platform configuration settings for SemanticShield AI.
    """
    PROJECT_NAME: str = "SemanticShield AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Threat Intelligence API Keys
    VIRUSTOTAL_API_KEY: str = os.getenv("VIRUSTOTAL_API_KEY", "")
    ABUSEIPDB_API_KEY: str = os.getenv("ABUSEIPDB_API_KEY", "")
    URLSCAN_API_KEY: str = os.getenv("URLSCAN_API_KEY", "")
    
    # Threat Intel Engine Configuration
    THREAT_INTEL_CACHE_TTL: int = int(os.getenv("THREAT_INTEL_CACHE_TTL", "3600"))
    THREAT_INTEL_MOCK_MODE: bool = os.getenv("THREAT_INTEL_MOCK_MODE", "True").lower() in ("true", "1", "t")
    
    # AI Fallback Freeze Configuration
    AI_FREEZE_DURATION_SECONDS: int = 300
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["*"]
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./semanticshield.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False").lower() in ("true", "1", "t")
    DATABASE_AUTO_MIGRATE: bool = os.getenv("DATABASE_AUTO_MIGRATE", "True").lower() in ("true", "1", "t")
    DATABASE_SEED_DEV_DATA: bool = os.getenv("DATABASE_SEED_DEV_DATA", "True").lower() in ("true", "1", "t")
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")


settings = Settings()

