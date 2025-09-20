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
        """
        Clean transcript data and extract only text and speaker information.
        Based on your example: data -> segments with text and speaker fields.
        """
        try:
            processed_lines = []
            
            # Handle the structure you showed: data -> segments array with text and speaker
            if isinstance(raw_transcript, dict):
                # Check for different possible structures
                segments = None
                if "data" in raw_transcript and "segments" in raw_transcript["data"]:
                    segments = raw_transcript["data"]["segments"]
                elif "segments" in raw_transcript:
                    segments = raw_transcript["segments"]
                elif "transcript" in raw_transcript and isinstance(raw_transcript["transcript"], list):
                    segments = raw_transcript["transcript"]
                
                if segments and isinstance(segments, list):
                    for segment in segments:
                        # Extract only text and speaker as requested
                        speaker = segment.get("speaker", "Unknown")
                        text = segment.get("text", "")
                        
                        if text.strip():  # Only include segments with actual text
                            processed_lines.append(f"{speaker}: {text}")
            
            # If we couldn't extract segments, try to handle as a direct text
            if not processed_lines:
                if isinstance(raw_transcript, str):
                    processed_lines.append(raw_transcript)
                elif isinstance(raw_transcript, dict) and "text" in raw_transcript:
                    processed_lines.append(raw_transcript["text"])
                else:
                    processed_lines.append("No readable transcript content found")
            
            result = "\n".join(processed_lines)
            print(f"Processed transcript with {len(processed_lines)} segments")
            return result
        
        except Exception as e:
            print(f"Error processing transcript: {e}")
            return f"Error processing transcript: {str(e)}"
        
        except Exception as e:
            return f"Error processing transcript: {str(e)}"


# Global instance
vexa_service = VexaService()