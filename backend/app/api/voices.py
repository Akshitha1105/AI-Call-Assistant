from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas.voice import Voice, VoiceCreate, VoiceUpdate, VoiceList
from ..core.auth import get_current_active_user
from ..models.user import User
from ..models.voice import Voice as VoiceModel

router = APIRouter(prefix="/voices", tags=["voices"])


@router.post("/", response_model=Voice, status_code=status.HTTP_201_CREATED)
def create_voice(
    voice_create: VoiceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new voice"""
    try:
        db_voice = VoiceModel(
            **voice_create.dict(),
            owner_id=current_user.id
        )
        db.add(db_voice)
        db.commit()
        db.refresh(db_voice)
        return db_voice
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create voice: {str(e)}"
        )


@router.get("/", response_model=VoiceList)
def list_voices(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    public_only: bool = Query(False),
    search: Optional[str] = Query(None)
):
    """List voices with pagination and filtering"""
    try:
        query = db.query(VoiceModel)
        
        if public_only:
            query = query.filter(VoiceModel.is_public == True)
        else:
            # Show user's own voices and public voices
            query = query.filter(
                (VoiceModel.owner_id == current_user.id) | (VoiceModel.is_public == True)
            )
        
        if search:
            query = query.filter(
                VoiceModel.name.ilike(f"%{search}%") | 
                VoiceModel.description.ilike(f"%{search}%")
            )
        
        total = query.count()
        voices = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return VoiceList(
            voices=voices,
            total=total,
            page=page,
            per_page=per_page
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list voices: {str(e)}"
        )


@router.get("/{voice_id}", response_model=Voice)
def get_voice(
    voice_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific voice by ID"""
    try:
        voice = db.query(VoiceModel).filter(VoiceModel.id == voice_id).first()
        if not voice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voice not found"
            )
        
        # Check if user can access this voice
        if not voice.is_public and voice.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return voice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get voice: {str(e)}"
        )


@router.put("/{voice_id}", response_model=Voice)
def update_voice(
    voice_id: int,
    voice_update: VoiceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a voice"""
    try:
        voice = db.query(VoiceModel).filter(VoiceModel.id == voice_id).first()
        if not voice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voice not found"
            )
        
        # Check ownership
        if voice.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only voice owner can update voice"
            )
        
        # Update fields
        update_data = voice_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(voice, field, value)
        
        db.commit()
        db.refresh(voice)
        return voice
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update voice: {str(e)}"
        )


@router.delete("/{voice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voice(
    voice_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a voice"""
    try:
        voice = db.query(VoiceModel).filter(VoiceModel.id == voice_id).first()
        if not voice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voice not found"
            )
        
        # Check ownership
        if voice.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only voice owner can delete voice"
            )
        
        db.delete(voice)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete voice: {str(e)}"
        )