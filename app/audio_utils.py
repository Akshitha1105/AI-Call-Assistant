import io
from typing import Tuple
import librosa
import soundfile as sf


def read_audio_bytes_to_wav(content: bytes, target_sr: int = 16000) -> Tuple[bytes, int]:
    y, sr = librosa.load(io.BytesIO(content), sr=None, mono=True)
    if sr != target_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
    wav_bytes = io.BytesIO()
    sf.write(wav_bytes, y, sr, format="WAV")
    return wav_bytes.getvalue(), sr

