from time import sleep
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.db import SessionLocal
from app import models


@celery_app.task
def finalize_voice_training(voice_id: int) -> str:
    # Simulate a training job; replace with real pipeline later
    sleep(2)
    db: Session = SessionLocal()
    try:
        voice = db.query(models.VoiceModel).filter(models.VoiceModel.id == voice_id).first()
        if not voice:
            return "voice_not_found"
        voice.status = "ready"
        db.add(voice)
        db.commit()
        return "ok"
    finally:
        db.close()

