from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid


class TrainingSession(Base):
    __tablename__ = "training_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    voice_id = Column(Integer, ForeignKey("voices.id"), nullable=False)
    
    # Training status
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    progress = Column(Float, default=0.0)  # 0.0 to 100.0
    
    # Training configuration
    model_type = Column(String(50), default="vits")  # vits, so-vits-svc, bark
    training_config = Column(JSON, nullable=True)  # Training hyperparameters
    
    # Training metrics
    loss_history = Column(JSON, nullable=True)  # Training loss over epochs
    validation_metrics = Column(JSON, nullable=True)  # Validation scores
    
    # File paths
    audio_samples_path = Column(Text, nullable=True)  # Path to uploaded audio samples
    output_model_path = Column(String(500), nullable=True)  # Path to trained model
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="training_sessions")
    voice = relationship("Voice", back_populates="training_sessions")
    
    def __repr__(self):
        return f"<TrainingSession(id={self.id}, status='{self.status}', progress={self.progress})>"


class AudioSample(Base):
    __tablename__ = "audio_samples"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    training_session_id = Column(Integer, ForeignKey("training_sessions.id"), nullable=False)
    
    # Audio metadata
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    duration = Column(Float, nullable=False)  # in seconds
    sample_rate = Column(Integer, nullable=False)
    channels = Column(Integer, default=1)
    
    # Quality metrics
    noise_level = Column(Float, nullable=True)
    clarity_score = Column(Float, nullable=True)  # 0.0 to 1.0
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    embedding_path = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<AudioSample(id={self.id}, filename='{self.filename}', duration={self.duration})>"