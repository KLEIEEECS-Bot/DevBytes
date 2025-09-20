from openai import OpenAI
import json
import re
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _extract_json_from_response(self, content: str) -> str:
        """Extract JSON from LLM response, handling various formats"""
        # Remove any leading/trailing whitespace
        content = content.strip()
        
        # If content is wrapped in code blocks, extract it
        if "```json" in content:
            json_start = content.find("```json") + 7
            json_end = content.find("```", json_start)
            if json_end != -1:
                content = content[json_start:json_end].strip()
        elif "```" in content:
            # Handle cases where it's just ```
            json_start = content.find("```") + 3
            json_end = content.rfind("```")
            if json_end != -1 and json_end != json_start - 3:
                content = content[json_start:json_end].strip()
        
        # Use regex to clean up problematic characters more aggressively
        content = re.sub(r'^[\n\r\t\s"\']*', '', content)
        content = re.sub(r'[\n\r\t\s"\']*$', '', content)
        
        # Try to extract JSON object/array using regex
        json_pattern = r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\])'
        json_match = re.search(json_pattern, content, re.DOTALL)
        
        if json_match:
            content = json_match.group(1)
        else:
            # Fallback: find first { or [ and try to balance brackets
            start_pos = -1
            for i, char in enumerate(content):
                if char in '{[':
                    start_pos = i
                    break
            
            if start_pos != -1:
                content = content[start_pos:]
                # Try to find the matching closing bracket
                if content[0] == '{':
                    bracket_count = 0
                    for i, char in enumerate(content):
                        if char == '{':
                            bracket_count += 1
                        elif char == '}':
                            bracket_count -= 1
                            if bracket_count == 0:
                                content = content[:i+1]
                                break
                elif content[0] == '[':
                    bracket_count = 0
                    for i, char in enumerate(content):
                        if char == '[':
                            bracket_count += 1
                        elif char == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                content = content[:i+1]
                                break
        
        return content

    def _save_to_output_file(self, transcript: str, llm_response: str, tasks: List[Dict], meeting_id: str = None):
        """Save transcript and LLM output to output.txt file"""
        try:
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output_{meeting_id}_{timestamp}.txt" if meeting_id else f"output_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"MEETING TRANSCRIPT AND TASK EXTRACTION\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if meeting_id:
                    f.write(f"Meeting ID: {meeting_id}\n")
                f.write("="*80 + "\n\n")
                
                f.write("ORIGINAL TRANSCRIPT:\n")
                f.write("-"*40 + "\n")
                f.write(transcript)
                f.write("\n\n" + "-"*40 + "\n\n")
                
                f.write("LLM RAW RESPONSE:\n")
                f.write("-"*40 + "\n")
                f.write(llm_response)
                f.write("\n\n" + "-"*40 + "\n\n")
                
                f.write("EXTRACTED TASKS:\n")
                f.write("-"*40 + "\n")
                for i, task in enumerate(tasks, 1):
                    f.write(f"Task {i}:\n")
                    f.write(f"  Assignee: {task.get('assignee_name', 'Unknown')}\n")
                    f.write(f"  Description: {task.get('task_description', 'No description')}\n")
                    f.write(f"  Deadline: {task.get('deadline', 'Not specified')}\n")
                    f.write(f"  Priority: {task.get('priority', 'Not specified')}\n")
                    f.write("\n")
                
                f.write("="*80 + "\n")
            
            print(f"Output saved to: {filepath}")
            
        except Exception as e:
            print(f"Error saving output file: {e}")

    def create_task_extraction_prompt(self, transcript: str, additional_context: Optional[str] = None) -> str:
        """Create a prompt for task extraction from meeting transcript"""
        base_prompt = """
You are an AI assistant specialized in analyzing meeting transcripts to extract action items and assign them to people.

Your task is to analyze the following meeting transcript and extract actionable tasks, assigning them to the appropriate people mentioned in the meeting.

For each person mentioned who has been assigned tasks or responsibilities, provide the output in the following JSON format:

{
    "tasks": [
        {
            "assignee_name": "Person's Name",
            "task_description": "Clear, actionable description of what they need to do",
            "deadline": "Deadline if mentioned (e.g., 'next Friday', 'by end of week', 'March 15th') or null if not specified",
            "priority": "high/medium/low if mentioned, otherwise null"
        }
    ]
}

Guidelines:
1. Only extract tasks that are clearly actionable and assigned to specific people
2. Be specific about what needs to be done
3. Include deadlines only if they are explicitly mentioned or strongly implied
4. Use the exact names as mentioned in the transcript
5. If someone is mentioned but no specific task is assigned, do not include them
6. Group similar tasks for the same person if appropriate
7. Make task descriptions clear and actionable

Meeting Transcript:
{transcript}
"""
        
        if additional_context:
            base_prompt += f"\n\nAdditional Context:\n{additional_context}"
        
        return base_prompt.format(transcript=transcript)

    def create_task_modification_prompt(self, transcript: str, existing_tasks: List[Dict], modification_request: str, additional_context: Optional[str] = None) -> str:
        """Create a prompt for modifying existing task assignments"""
        existing_tasks_json = json.dumps(existing_tasks, indent=2)
        
        prompt = f"""
You are an AI assistant helping to modify task assignments from a meeting transcript based on user feedback.

Original Meeting Transcript:
{transcript}

Current Task Assignments:
{existing_tasks_json}

User's Modification Request:
{modification_request}

Based on the user's request, please provide updated task assignments in the same JSON format:

{{
    "tasks": [
        {{
            "assignee_name": "Person's Name",
            "task_description": "Clear, actionable description of what they need to do",
            "deadline": "Deadline if mentioned or null if not specified",
            "priority": "high/medium/low if mentioned, otherwise null"
        }}
    ]
}}

Guidelines:
1. Incorporate the user's modifications while keeping the original context
2. Maintain the same JSON structure
3. Only include actionable tasks assigned to specific people
4. Be specific and clear in task descriptions
"""
        
        if additional_context:
            prompt += f"\n\nAdditional Context:\n{additional_context}"
        
        return prompt

    async def extract_tasks_from_transcript(self, transcript: str, additional_context: Optional[str] = None, meeting_id: str = None) -> Dict[str, Any]:
        """Extract tasks from meeting transcript using LLM"""
        try:
            prompt = self.create_task_extraction_prompt(transcript, additional_context)
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing meeting transcripts and extracting actionable tasks. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean the content to extract JSON
            cleaned_content = self._extract_json_from_response(content)
            
            # Try to parse JSON response
            try:
                result = json.loads(cleaned_content)
                tasks = result.get("tasks", [])
                
                # Save to output file
                self._save_to_output_file(transcript, content, tasks, meeting_id)
                
                return {
                    "success": True,
                    "tasks": tasks
                }
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed. Original content: {repr(content)}")
                print(f"Cleaned content: {repr(cleaned_content)}")
                print(f"JSON error: {e}")
                
                # Save raw response for debugging
                self._save_to_output_file(transcript, f"PARSING FAILED:\n{content}", [], meeting_id)
                
                return {
                    "success": False,
                    "error": f"Failed to parse LLM response as JSON: {str(e)}. Content: {content[:200]}..."
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing with LLM: {str(e)}"
            }

    async def modify_task_assignments(self, transcript: str, existing_tasks: List[Dict], modification_request: str, additional_context: Optional[str] = None) -> Dict[str, Any]:
        """Modify existing task assignments based on user request"""
        try:
            prompt = self.create_task_modification_prompt(transcript, existing_tasks, modification_request, additional_context)
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at modifying task assignments based on user feedback. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean the content to extract JSON
            cleaned_content = self._extract_json_from_response(content)
            
            # Try to parse JSON response
            try:
                result = json.loads(cleaned_content)
                tasks = result.get("tasks", [])
                
                # Save to output file for modification requests
                self._save_to_output_file(transcript, f"MODIFICATION REQUEST: {modification_request}\n\nLLM RESPONSE:\n{content}", tasks, "modification")
                
                return {
                    "success": True,
                    "tasks": tasks
                }
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed in modify_task_assignments. Original content: {repr(content)}")
                print(f"Cleaned content: {repr(cleaned_content)}")
                print(f"JSON error: {e}")
                
                # Save raw response for debugging
                self._save_to_output_file(transcript, f"MODIFICATION PARSING FAILED:\nREQUEST: {modification_request}\nRESPONSE: {content}", [], "modification_failed")
                
                return {
                    "success": False,
                    "error": f"Failed to parse LLM response as JSON: {str(e)}. Content: {content[:200]}..."
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing modification with LLM: {str(e)}"
            }


# Global instance
llm_service = LLMService()