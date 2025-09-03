from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.db import get_db
from app import models, schemas
from app.security import get_current_user
from app.ml import load_embedding, tts_with_embedding


router = APIRouter()


@router.post("/generate_speech")
def generate_speech(
    body: schemas.TTSRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    voice = db.query(models.VoiceModel).filter(models.VoiceModel.id == body.voice_id, models.VoiceModel.user_id == user.id).first()
    if not voice or not voice.embedding_path:
        raise HTTPException(status_code=404, detail="Voice not found or not ready")
    embedding = load_embedding(voice.embedding_path)

    wav_bytes = tts_with_embedding(text=body.text, speaker_embedding=embedding, language=body.language)

    return StreamingResponse(io.BytesIO(wav_bytes), media_type="audio/wav")

