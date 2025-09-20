from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import meetings, tasks, transcripts, exports

app = FastAPI(
    title="Meeting Notes Processor",
    description="API for processing meeting transcripts and extracting action items",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(meetings.router, prefix="/api/meetings", tags=["meetings"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(transcripts.router, prefix="/api/transcripts", tags=["transcripts"])
app.include_router(exports.router, prefix="/api/exports", tags=["exports"])

@app.get("/")
async def root():
    return {"message": "Meeting Notes Processor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}