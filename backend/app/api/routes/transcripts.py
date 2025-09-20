from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Transcript, Meeting
from app.models.schemas import TranscriptCreate, TranscriptResponse
from app.services.vexa_service import vexa_service
from app.services.llm_service import llm_service

router = APIRouter()


@router.post("/{meeting_id}/process", response_model=dict)
async def process_transcript(
    meeting_id: str, 
    transcript_data: TranscriptCreate, 
    db: Session = Depends(get_db)
):
    """Process transcript for a meeting and extract tasks"""
    # Get meeting from database
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    try:
        # Get transcript from Vexa API
        transcript_result = await vexa_service.get_transcript(meeting_id)
        
        if not transcript_result["success"]:
            raise HTTPException(status_code=400, detail=f"Failed to fetch transcript: {transcript_result['error']}")
        
        # Process the raw transcript
        raw_transcript = transcript_result["transcript"]
        processed_transcript = vexa_service.process_transcript_data(raw_transcript)
        
        # Save transcript to database
        transcript = Transcript(
            meeting_id=meeting.id,
            raw_transcript=str(raw_transcript),
            processed_transcript=processed_transcript,
            additional_context=transcript_data.additional_context
        )
        db.add(transcript)
        db.commit()
        db.refresh(transcript)
        
        # Extract tasks using LLM
        llm_result = await llm_service.extract_tasks_from_transcript(
            processed_transcript, 
            transcript_data.additional_context,
            meeting_id
        )
        
        if not llm_result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to extract tasks: {llm_result['error']}")
        
        # Save extracted tasks to database
        from app.models.database import Task
        for task_data in llm_result["tasks"]:
            task = Task(
                meeting_id=meeting.id,
                assignee_name=task_data["assignee_name"],
                task_description=task_data["task_description"],
                deadline=task_data.get("deadline"),
                priority=task_data.get("priority")
            )
            db.add(task)
        
        db.commit()
        
        return {
            "message": "Transcript processed successfully",
            "transcript_id": transcript.id,
            "tasks_extracted": len(llm_result["tasks"]),
            "tasks": llm_result["tasks"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{meeting_id}", response_model=TranscriptResponse)
async def get_transcript(meeting_id: str, db: Session = Depends(get_db)):
    """Get processed transcript for a meeting"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    transcript = db.query(Transcript).filter(Transcript.meeting_id == meeting.id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    return transcript