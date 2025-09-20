import httpx
import json
from typing import Dict, Any, Optional
from app.core.config import settings


class VexaService:
    def __init__(self):
        self.base_url = settings.VEXA_BASE_URL
        self.api_key = settings.VEXA_API_KEY
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        }

    def extract_meeting_id_from_url(self, meeting_url: str) -> str:
        """Extract meeting ID from Google Meet URL"""
        # Google Meet URLs are typically like: https://meet.google.com/abc-def-ghi
        if "meet.google.com/" in meeting_url:
            return meeting_url.split("meet.google.com/")[-1].split("?")[0]
        else:
            raise ValueError("Invalid Google Meet URL format")

    async def start_bot(self, meeting_url: str, bot_name: str = "MeetingBot") -> Dict[str, Any]:
        """Start a bot for the given Google Meet URL"""
        try:
            meeting_id = self.extract_meeting_id_from_url(meeting_url)
            
            payload = {
                "platform": "google_meet",
                "native_meeting_id": meeting_id,
                "bot_name": bot_name
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/bots",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                return {
                    "success": True,
                    "meeting_id": meeting_id,
                    "data": response.json()
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_transcript(self, meeting_id: str) -> Dict[str, Any]:
        """Get transcript for a completed meeting"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/transcripts/google_meet/{meeting_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return {
                    "success": True,
                    "transcript": response.json()
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def delete_bot(self, meeting_id: str) -> Dict[str, Any]:
        """Delete/remove bot from meeting"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/bots/google_meet/{meeting_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return {
                    "success": True,
                    "message": "Bot removed successfully"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def process_transcript_data(self, raw_transcript: Dict[str, Any]) -> str:
        """Clean transcript data and extract text and speaker information"""
        try:
            # The transcript structure may vary, but typically contains segments with text and speaker info
            processed_lines = []
            
            # Handle different possible transcript structures
            if "segments" in raw_transcript:
                for segment in raw_transcript["segments"]:
                    speaker = segment.get("speaker", "Unknown")
                    text = segment.get("text", "")
                    if text.strip():
                        processed_lines.append(f"{speaker}: {text}")
            
            elif "transcript" in raw_transcript:
                # Alternative structure
                transcript_data = raw_transcript["transcript"]
                if isinstance(transcript_data, list):
                    for item in transcript_data:
                        speaker = item.get("speaker", "Unknown")
                        text = item.get("text", "")
                        if text.strip():
                            processed_lines.append(f"{speaker}: {text}")
            
            # Fallback: try to extract any text content
            if not processed_lines and "text" in raw_transcript:
                processed_lines.append(raw_transcript["text"])
            
            return "\n".join(processed_lines)
        
        except Exception as e:
            return f"Error processing transcript: {str(e)}"


# Global instance
vexa_service = VexaService()