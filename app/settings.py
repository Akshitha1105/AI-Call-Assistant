from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ai-voice"
    api_prefix: str = "/api"
    secret_key: str = "change_me"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite:///./data.db"

    storage_backend: str = "local"  # local | s3
    storage_local_dir: str = "./storage"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_default_region: str | None = None
    s3_bucket_name: str | None = None

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    tts_model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    device: str = "cpu"

    class Config:
        env_file = ".env"


settings = Settings()
if not settings.celery_broker_url:
    settings.celery_broker_url = settings.redis_url
if not settings.celery_result_backend:
    settings.celery_result_backend = settings.redis_url

