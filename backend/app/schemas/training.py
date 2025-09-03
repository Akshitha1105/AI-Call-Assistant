from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TrainingSessionBase(BaseModel):
    voice_id: int
    model_type: str = Field(default="vits", regex="^(vits|so-vits-svc|bark)$")
    training_config: Optional[Dict[str, Any]] = None


class TrainingSessionCreate(TrainingSessionBase):
    pass


class TrainingSessionUpdate(BaseModel):
    status: Optional[str] = Field(None, regex="^(pending|processing|completed|failed)$")
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    training_config: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class TrainingSessionInDB(TrainingSessionBase):
    id: int
    uuid: str
    user_id: int
    
    # Training status
    status: str = "pending"
    progress: float = 0.0
    
    # Training metrics
    loss_history: Optional[Dict[str, Any]] = None
    validation_metrics: Optional[Dict[str, Any]] = None
    
    # File paths
    audio_samples_path: Optional[str] = None
    output_model_path: Optional[str] = None
    
    # Error handling
    error_message: Optional[str] = None
    retry_count: int = 0
    
    # Timestamps
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TrainingSession(TrainingSessionInDB):
    pass


class TrainingSessionList(BaseModel):
    training_sessions: list[TrainingSession]
    total: int
    page: int
    per_page: int


class AudioSampleBase(BaseModel):
    filename: str
    duration: float
    sample_rate: int
    channels: int = 1


class AudioSampleCreate(AudioSampleBase):
    file_path: str
    file_size: int


class AudioSampleInDB(AudioSampleBase):
    id: int
    uuid: str
    training_session_id: int
    
    # Audio metadata
    file_path: str
    file_size: int
    
    # Quality metrics
    noise_level: Optional[float] = None
    clarity_score: Optional[float] = None
    
    # Processing status
    is_processed: bool = False
    embedding_path: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AudioSample(AudioSampleInDB):
    pass


class TrainingProgress(BaseModel):
    session_id: int
    status: str
    progress: float
    current_step: str
    estimated_time_remaining: Optional[int] = None  # in seconds
    loss_history: Optional[Dict[str, Any]] = None
    validation_metrics: Optional[Dict[str, Any]] = None