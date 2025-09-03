from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid


class Voice(Base):
    __tablename__ = "voices"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Voice characteristics
    gender = Column(String(20), nullable=True)  # male, female, neutral
    age_group = Column(String(20), nullable=True)  # child, young, adult, senior
    accent = Column(String(50), nullable=True)
    language = Column(String(10), default="en")  # ISO language code
    
    # Model information
    model_path = Column(String(500), nullable=True)  # Path to trained model
    embedding_path = Column(String(500), nullable=True)  # Path to voice embedding
    sample_audio_path = Column(String(500), nullable=True)  # Path to sample audio
    
    # Training metadata
    training_samples_count = Column(Integer, default=0)
    training_duration = Column(Float, default=0.0)  # in seconds
    training_quality_score = Column(Float, nullable=True)  # 0.0 to 1.0
    
    # Status and visibility
    is_public = Column(Boolean, default=False)
    is_trained = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    trained_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="voices")
    training_sessions = relationship("TrainingSession", back_populates="voice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Voice(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"