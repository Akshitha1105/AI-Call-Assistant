### System Architecture

Components:
- Gradio UI (HF Spaces): Auth (via API), upload samples, list voices, TTS generation
- FastAPI Backend (Render/AWS/GCP): Auth, Voice CRUD, TTS endpoint
- Celery + Redis: Background training orchestration
- Storage (S3/Local): user embeddings, model artifacts, generated audio
- Database (Postgres/SQLite): users, voices, generation jobs
- ML: Resemblyzer (speaker encoder), XTTS v2 (multilingual TTS)

Data Flow (MVP):
1) User uploads audio -> API averages embeddings -> stores NPY in storage -> creates Voice row
2) User triggers training -> enqueues Celery job -> status transitions to ready
3) TTS request -> loads embedding -> runs XTTS with speaker conditioning -> returns WAV stream

ASCII Diagram:

```
         [User Browser]
               |
           (Gradio)
               | HTTP
        +--------------+
        |   FastAPI    |
        |  Auth/Voices |
        +--------------+
          |        | \
          |        |  \
       (DB)     (Storage)  (Celery Broker)
        |           |           |
   [Postgres]   [S3/Local]   [Redis]
                               |
                            [Celery]
                               |
                            [ML Jobs]
                               |
                             [XTTS]
```

Scaling Notes:
- Move ML inference to GPU nodes (RunPod/Replicate) behind an internal service URL
- Swap embedding-only pipeline with full fine-tuning (so-vits-svc / VITS) in Celery
- Add Stripe for credit-limited TTS calls; rate limit per user

