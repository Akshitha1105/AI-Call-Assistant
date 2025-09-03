from __future__ import annotations

import os
import io
from typing import Optional

import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from TTS.api import TTS

from app.settings import settings


_encoder: Optional[VoiceEncoder] = None
_tts: Optional[TTS] = None


def get_encoder() -> VoiceEncoder:
    global _encoder
    if _encoder is None:
        _encoder = VoiceEncoder()
    return _encoder


def get_tts() -> TTS:
    global _tts
    if _tts is None:
        _tts = TTS(settings.tts_model_name).to(settings.device)
    return _tts


def compute_embedding_from_wav_bytes(wav_bytes: bytes) -> np.ndarray:
    wav = preprocess_wav(io.BytesIO(wav_bytes))
    encoder = get_encoder()
    return encoder.embed_utterance(wav)


def save_embedding(embedding: np.ndarray, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.save(path, embedding.astype(np.float32))


def load_embedding(path: str) -> np.ndarray:
    return np.load(path)


def tts_with_embedding(text: str, speaker_embedding: np.ndarray, language: Optional[str] = None) -> bytes:
    model = get_tts()
    wav = model.tts(text=text, speaker_wav=None, speaker_embeddings=speaker_embedding, language=language)
    import soundfile as sf
    import io

    buf = io.BytesIO()
    sf.write(buf, wav, 22050, format="WAV")
    return buf.getvalue()

