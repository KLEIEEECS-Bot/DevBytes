from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Task, Meeting
from app.models.schemas import TaskResponse, TaskModificationRequest
from app.services.llm_service import llm_service
from typing import List
import json

router = APIRouter()


@router.get("/{meeting_id}", response_model=List[TaskResponse])
async def get_tasks_for_meeting(meeting_id: str, db: Session = Depends(get_db)):
    """Get all tasks for a specific meeting"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    tasks = db.query(Task).filter(Task.meeting_id == meeting.id).all()
    return tasks


@router.post("/{meeting_id}/modify", response_model=dict)
async def modify_tasks(
    meeting_id: str, 
    modification_request: TaskModificationRequest, 
    db: Session = Depends(get_db)
):
    """Modify task assignments based on user feedback"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Get existing tasks
    existing_tasks = db.query(Task).filter(Task.meeting_id == meeting.id).all()
    existing_tasks_data = [
        {
            "assignee_name": task.assignee_name,
            "task_description": task.task_description,
            "deadline": task.deadline,
            "priority": task.priority
        } for task in existing_tasks
    ]
    
    # Get transcript
    from app.models.database import Transcript
    transcript = db.query(Transcript).filter(Transcript.meeting_id == meeting.id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    try:
        # Use LLM to modify tasks based on user request
        llm_result = await llm_service.modify_task_assignments(
            transcript.processed_transcript,
            existing_tasks_data,
            modification_request.modification_request,
            transcript.additional_context
        )
        
        if not llm_result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to modify tasks: {llm_result['error']}")
        
        # Delete existing tasks
        db.query(Task).filter(Task.meeting_id == meeting.id).delete()
        
        # Add new modified tasks
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
            "message": "Tasks modified successfully",
            "tasks_count": len(llm_result["tasks"]),
            "tasks": llm_result["tasks"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{task_id}/complete", response_model=dict)
async def mark_task_complete(task_id: int, db: Session = Depends(get_db)):
    """Mark a task as completed"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_completed = True
    db.commit()
    
    return {"message": "Task marked as completed", "task_id": task_id}


@router.get("/{meeting_id}/export", response_model=dict)
async def export_tasks(meeting_id: str, db: Session = Depends(get_db)):
    """Generate export data for tasks"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    tasks = db.query(Task).filter(Task.meeting_id == meeting.id).all()
    
    export_data = {
        "meeting_id": meeting_id,
        "meeting_url": meeting.meeting_url,
        "created_at": meeting.created_at.isoformat(),
        "tasks": [
            {
                "assignee_name": task.assignee_name,
                "task_description": task.task_description,
                "deadline": task.deadline,
                "priority": task.priority,
                "is_completed": task.is_completed
            } for task in tasks
        ]
    }
    
    return export_data