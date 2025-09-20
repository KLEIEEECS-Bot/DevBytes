from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.core.config import settings

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, unique=True, index=True)  # Google Meet ID
    meeting_url = Column(String)
    bot_name = Column(String, default="MeetingBot")
    status = Column(String, default="pending")  # pending, active, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    transcript = relationship("Transcript", back_populates="meeting", uselist=False)
    tasks = relationship("Task", back_populates="meeting")


class Transcript(Base):
    __tablename__ = "transcripts"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    raw_transcript = Column(Text)  # Raw JSON from Vexa
    processed_transcript = Column(Text)  # Cleaned text with speakers
    additional_context = Column(Text, nullable=True)  # User-provided context
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="transcript")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    assignee_name = Column(String)
    task_description = Column(Text)
    deadline = Column(String, nullable=True)  # Store as string since LLM might return various formats
    priority = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="tasks")


# Create all tables
Base.metadata.create_all(bind=engine)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()