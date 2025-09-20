from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class TaskModel(BaseModel):
    """Pydantic model for a single task"""
    title: str = Field(description="Clear, concise title of the task")
    description: str = Field(description="Detailed, actionable description of what needs to be done")
    assignee: str = Field(description="Name of the person assigned to the task, or 'Unassigned' if no one is specified")
    priority: str = Field(description="Task priority: 'High', 'Medium', or 'Low'")
    status: str = Field(default="pending", description="Task status, defaults to 'pending'")
    deadline: Optional[str] = Field(None, description="Deadline in YYYY-MM-DD format, or null if not specified")
    category: str = Field(default="action_item", description="Task category, defaults to 'action_item'")


class TaskExtractionResponse(BaseModel):
    """Pydantic model for the complete task extraction response"""
    tasks: List[TaskModel] = Field(description="List of extracted tasks from the meeting transcript")