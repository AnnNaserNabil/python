"""Application configuration settings."""
import os
from functools import lru_cache
from pydantic import BaseSettings, Field, PostgresDsn, validator
from typing import Optional, Dict, Any, List

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "Google Ads MCP Server"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    VERSION: str = "0.1.0"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "google-ads-mcp"
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str = Field(..., env="GOOGLE_CLOUD_PROJECT")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Google Ads API
    GOOGLE_ADS_CLIENT_ID: str = Field(..., env="GOOGLE_ADS_CLIENT_ID")
    GOOGLE_ADS_CLIENT_SECRET: str = Field(..., env="GOOGLE_ADS_CLIENT_SECRET")
    GOOGLE_ADS_DEVELOPER_TOKEN: str = Field(..., env="GOOGLE_ADS_DEVELOPER_TOKEN")
    GOOGLE_ADS_REFRESH_TOKEN: str = Field(..., env="GOOGLE_ADS_REFRESH_TOKEN")
    GOOGLE_ADS_LOGIN_CUSTOMER_ID: str = Field(..., env="GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    
    # Database
    FIRESTORE_COLLECTION_PREFIX: str = os.getenv("FIRESTORE_COLLECTION_PREFIX", "mcp_")
    
    # Pub/Sub
    PUBSUB_TOPIC_ID: str = os.getenv("PUBSUB_TOPIC_ID", "mcp-events")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()

# Global settings instance
settings = get_settings()
