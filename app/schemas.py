from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class VoiceCreate(BaseModel):
    name: str
    description: Optional[str] = None


class VoiceOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TTSRequest(BaseModel):
    voice_id: int
    text: str
    language: str | None = None
    emotion: str | None = None

