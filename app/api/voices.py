from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app import models, schemas
from app.security import get_current_user
from app.storage import storage_save_bytes
from app.audio_utils import read_audio_bytes_to_wav
from app.ml import compute_embedding_from_wav_bytes, save_embedding
from app.tasks import finalize_voice_training


router = APIRouter()


@router.post("/upload_voice", response_model=schemas.VoiceOut)
async def upload_voice(
    name: str = Form(...),
    description: str | None = Form(None),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    # Aggregate multiple files into one embedding by averaging
    embeddings = []
    for f in files:
        content = await f.read()
        wav_bytes, _ = read_audio_bytes_to_wav(content, target_sr=16000)
        emb = compute_embedding_from_wav_bytes(wav_bytes)
        embeddings.append(emb)
    if not embeddings:
        raise HTTPException(status_code=400, detail="No audio provided")
    import numpy as np

    speaker_embedding = np.mean(np.vstack(embeddings), axis=0)

    # Persist embedding
    embedding_npy = speaker_embedding.astype(np.float32).tobytes()
    path, _ = storage_save_bytes(embedding_npy, ext=".npy", subdir=f"users/{user.id}/embeddings")
    # We saved raw bytes, ensure npy structure through helper
    save_embedding(speaker_embedding, path)

    voice = models.VoiceModel(
        user_id=user.id,
        name=name,
        description=description,
        status="ready",
        embedding_path=path,
    )
    db.add(voice)
    db.commit()
    db.refresh(voice)
    return voice


@router.post("/train_voice")
def train_voice(
    voice_id: int = Form(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    voice = db.query(models.VoiceModel).filter(models.VoiceModel.id == voice_id, models.VoiceModel.user_id == user.id).first()
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    voice.status = "training"
    db.add(voice)
    db.commit()
    finalize_voice_training.delay(voice.id)
    return {"status": "queued", "voice_id": voice.id}


@router.get("/list_voices", response_model=List[schemas.VoiceOut])
def list_voices(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    voices = db.query(models.VoiceModel).filter(models.VoiceModel.user_id == user.id).order_by(models.VoiceModel.created_at.desc()).all()
    return voices

