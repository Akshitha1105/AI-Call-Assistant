from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.api import auth, voices, tts
from app.db import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix=settings.api_prefix, tags=["auth"])
    app.include_router(voices.router, prefix=f"{settings.api_prefix}/voices", tags=["voices"])
    app.include_router(tts.router, prefix=f"{settings.api_prefix}/tts", tags=["tts"])

    @app.get("/")
    def root():
        return {"status": "ok", "name": settings.app_name}

    @app.on_event("startup")
    def _startup():
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()

