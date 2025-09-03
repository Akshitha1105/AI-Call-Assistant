## AI Voice Platform (MyVocal-like)

Production-ready scaffold for a MyVocal.ai-style platform: upload voice samples, train a custom voice (embedding-based MVP), generate speech, preview, and download.

### Components
- Backend: FastAPI + SQLAlchemy + JWT Auth + Celery (training background jobs)
- Storage: S3 or Local filesystem
- ML: Resemblyzer for embeddings; XTTS v2 for multilingual TTS with speaker conditioning
- Frontend: Gradio app for Hugging Face Spaces

### Quick Start (Local)
1. Copy `.env.example` to `.env` and adjust values
2. Build and run docker: `docker build -t ai-voice . && docker run --env-file .env -p 8000:8000 ai-voice`
3. Open API docs: http://localhost:8000/docs
4. Launch Gradio UI (if running separately): `python frontend/gradio_app.py`

### Backend Endpoints (MVP)
- POST /auth/signup
- POST /auth/login
- POST /voices/upload_voice
- POST /voices/train_voice
- GET  /voices/list_voices
- POST /tts/generate_speech

### Notes
- Training job in MVP computes and stores a speaker embedding from uploaded samples instead of full model fine-tuning. This enables custom voice conditioning with XTTS v2 at low cost. Swap in a full training pipeline (e.g., so-vits-svc) behind the Celery task when ready.

# AI-Call-Assistant