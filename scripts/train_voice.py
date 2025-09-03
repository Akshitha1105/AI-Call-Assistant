import argparse
import glob
import numpy as np
import os

from app.db import SessionLocal
from app import models
from app.ml import compute_embedding_from_wav_bytes, save_embedding
from app.storage import storage_path


def main():
    parser = argparse.ArgumentParser(description="Compute speaker embedding and register a voice")
    parser.add_argument("--user-id", type=int, required=True)
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--input-dir", type=str, required=True, help="Directory containing wav/mp3 files")
    args = parser.parse_args()

    files = []
    for ext in ("wav", "mp3", "m4a", "flac"):
        files.extend(glob.glob(os.path.join(args.input_dir, f"*.{ext}")))
    if not files:
        raise SystemExit("No audio files found in input dir")

    embeddings = []
    for p in files:
        with open(p, "rb") as f:
            content = f.read()
        # The API converges to wav inside
        from app.audio_utils import read_audio_bytes_to_wav

        wav_bytes, _ = read_audio_bytes_to_wav(content, target_sr=16000)
        emb = compute_embedding_from_wav_bytes(wav_bytes)
        embeddings.append(emb)

    speaker_embedding = np.mean(np.vstack(embeddings), axis=0)

    dst = storage_path(f"users/{args.user_id}/embeddings/{args.name.replace(' ', '_')}.npy")
    save_embedding(speaker_embedding, dst)

    db = SessionLocal()
    try:
        voice = models.VoiceModel(user_id=args.user_id, name=args.name, status="ready", embedding_path=dst)
        db.add(voice)
        db.commit()
        db.refresh(voice)
        print(f"Created voice id={voice.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

