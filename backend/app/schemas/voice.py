from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VoiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    gender: Optional[str] = Field(None, regex="^(male|female|neutral)$")
    age_group: Optional[str] = Field(None, regex="^(child|young|adult|senior)$")
    accent: Optional[str] = None
    language: str = Field(default="en", regex="^[a-z]{2}$")
    is_public: bool = False


class VoiceCreate(VoiceBase):
    pass


class VoiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    gender: Optional[str] = Field(None, regex="^(male|female|neutral)$")
    age_group: Optional[str] = Field(None, regex="^(child|young|adult|senior)$")
    accent: Optional[str] = None
    language: Optional[str] = Field(None, regex="^[a-z]{2}$")
    is_public: Optional[bool] = None


class VoiceInDB(VoiceBase):
    id: int
    uuid: str
    owner_id: int
    
    # Model information
    model_path: Optional[str] = None
    embedding_path: Optional[str] = None
    sample_audio_path: Optional[str] = None
    
    # Training metadata
    training_samples_count: int = 0
    training_duration: float = 0.0
    training_quality_score: Optional[float] = None
    
    # Status
    is_trained: bool = False
    is_active: bool = True
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
    trained_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Voice(VoiceInDB):
    pass


class VoiceList(BaseModel):
    voices: List[Voice]
    total: int
    page: int
    per_page: int


class VoiceTrainingRequest(BaseModel):
    voice_id: int
    model_type: str = Field(default="vits", regex="^(vits|so-vits-svc|bark)$")
    training_config: Optional[dict] = None


class VoiceGenerationRequest(BaseModel):
    voice_id: int
    text: str = Field(..., min_length=1, max_length=1000)
    emotion: Optional[str] = Field(None, regex="^(happy|sad|angry|calm|excited|neutral)$")
    speed: Optional[float] = Field(1.0, ge=0.5, le=2.0)
    pitch: Optional[float] = Field(1.0, ge=0.5, le=2.0)