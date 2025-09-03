from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "Voice Cloning Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "postgresql://user:password@localhost/voice_cloning"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Storage
    storage_type: str = "local"  # local, s3, gcs
    local_storage_path: str = "./storage"
    
    # AWS S3
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: Optional[str] = None
    
    # Google Cloud Storage
    gcs_project_id: Optional[str] = None
    gcs_bucket_name: Optional[str] = None
    gcs_credentials_path: Optional[str] = None
    
    # ML Models
    model_cache_dir: str = "./models"
    max_audio_duration: int = 600  # 10 minutes in seconds
    supported_audio_formats: list = [".wav", ".mp3", ".flac", ".m4a"]
    
    # Training
    max_training_duration: int = 3600  # 1 hour in seconds
    min_voice_samples: int = 5
    max_voice_samples: int = 50
    
    # API
    api_prefix: str = "/api/v1"
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Ensure storage directories exist
os.makedirs(settings.local_storage_path, exist_ok=True)
os.makedirs(settings.model_cache_dir, exist_ok=True)