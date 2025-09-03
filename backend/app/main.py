from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from .config import settings
from .database import create_tables
from .api import auth, voices

# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Voice Cloning Platform...")
    create_tables()
    print("Database tables created/verified")
    
    yield
    
    # Shutdown
    print("Shutting down Voice Cloning Platform...")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Voice Cloning Platform API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(voices.router, prefix=settings.api_prefix)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.app_name}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Voice Cloning Platform API",
        "version": settings.app_version,
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )