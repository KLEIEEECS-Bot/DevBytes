from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Meeting
from app.models.schemas import MeetingCreate, MeetingResponse
from app.services.vexa_service import vexa_service
from typing import List

router = APIRouter()


@router.post("/start", response_model=dict)
async def start_meeting_bot(meeting_data: MeetingCreate, db: Session = Depends(get_db)):
    """Start a bot for a Google Meet session"""
    try:
        # Start the bot using Vexa API
        result = await vexa_service.start_bot(meeting_data.meeting_url, meeting_data.bot_name)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Save meeting to database
        meeting = Meeting(
            meeting_id=result["meeting_id"],
            meeting_url=meeting_data.meeting_url,
            bot_name=meeting_data.bot_name,
            status="active"
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        
        return {
            "message": "Bot started successfully",
            "meeting_id": result["meeting_id"],
            "meeting_db_id": meeting.id,
            "status": "active"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{meeting_id}/status", response_model=dict)
async def get_meeting_status(meeting_id: str, db: Session = Depends(get_db)):
    """Get the status of a meeting"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "meeting_id": meeting.meeting_id,
        "status": meeting.status,
        "created_at": meeting.created_at,
        "completed_at": meeting.completed_at
    }


@router.post("/{meeting_id}/complete", response_model=dict)
async def complete_meeting(meeting_id: str, db: Session = Depends(get_db)):
    """Mark a meeting as completed and remove the bot"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Remove bot from meeting
    result = await vexa_service.delete_bot(meeting_id)
    
    # Update meeting status regardless of bot removal result
    meeting.status = "completed"
    from datetime import datetime
    meeting.completed_at = datetime.utcnow()
    db.commit()
    
    return {
        "message": "Meeting completed",
        "meeting_id": meeting_id,
        "bot_removed": result["success"]
    }


@router.get("/", response_model=List[MeetingResponse])
async def get_meetings(db: Session = Depends(get_db)):
    """Get all meetings"""
    meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).all()
    return meetings


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    """Get a specific meeting"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return meeting