from celery import Celery
from app.settings import settings


celery_app = Celery(
    "ai_voice",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

