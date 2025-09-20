from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Meeting schemas
class MeetingCreate(BaseModel):
    meeting_url: str
    bot_name: Optional[str] = "MeetingBot"


class MeetingResponse(BaseModel):
    id: int
    meeting_id: str
    meeting_url: str
    bot_name: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# Task schemas
class TaskResponse(BaseModel):
    id: int
    assignee_name: str
    task_description: str
    deadline: Optional[str]
    priority: Optional[str]
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    assignee_name: str
    task_description: str
    deadline: Optional[str] = None
    priority: Optional[str] = None


# Transcript schemas
class TranscriptCreate(BaseModel):
    additional_context: Optional[str] = None


class TranscriptResponse(BaseModel):
    id: int
    meeting_id: int
    processed_transcript: str
    additional_context: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Task modification request
class TaskModificationRequest(BaseModel):
    modification_request: str
    meeting_id: int