from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import json
import re
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models.task_models import TaskExtractionResponse, TaskModel


class LLMService:
    def __init__(self):
        # Initialize LangChain's Gemini model with 2.5-flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.0
        )
        
        # Create output parser for structured response
        self.output_parser = PydanticOutputParser(pydantic_object=TaskExtractionResponse)

    def _save_raw_transcript(self, transcript: str, meeting_id: str = None):
        """Save raw transcript before any processing"""
        try:
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"Created output directory: {output_dir}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"raw_transcript_{meeting_id}_{timestamp}.txt" if meeting_id else f"raw_transcript_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"RAW TRANSCRIPT\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if meeting_id:
                    f.write(f"Meeting ID: {meeting_id}\n")
                f.write("="*80 + "\n\n")
                f.write(transcript)
                f.write("\n\n" + "="*80 + "\n")
            
            print(f"Raw transcript saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving raw transcript: {e}")
            return None

    def _save_llm_response(self, llm_response: str, meeting_id: str = None):
        """Save LLM response before parsing"""
        try:
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"llm_response_{meeting_id}_{timestamp}.txt" if meeting_id else f"llm_response_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"LLM RAW RESPONSE\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if meeting_id:
                    f.write(f"Meeting ID: {meeting_id}\n")
                f.write("="*80 + "\n\n")
                f.write(llm_response)
                f.write("\n\n" + "="*80 + "\n")
            
            print(f"LLM response saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving LLM response: {e}")
            return None

    def _save_to_output_file(self, transcript: str, llm_response: str, tasks: list, meeting_id: str = None):
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

    def create_task_extraction_prompt(self) -> PromptTemplate:
        """Create a LangChain prompt template for task extraction"""
        template = """
You are an expert AI assistant specialized in analyzing meeting transcripts to extract actionable tasks.

Your job is to:
1. Identify clear action items that require someone to DO something
2. Extract the person responsible (assignee) from the conversation
3. Determine priority based on urgency discussed
4. Set reasonable deadlines based on context mentioned
5. Create clear, actionable task descriptions

Rules:
- Only extract tasks that are explicitly actionable (not just discussions)
- Use exact names mentioned in the transcript
- If no assignee is clear, use "Unassigned"
- Priority should be "High", "Medium", or "Low"
- Deadline format: YYYY-MM-DD or null if not mentioned
- Make task descriptions specific and actionable

Meeting Transcript:
{transcript}

{format_instructions}
"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

    def create_task_modification_prompt(self) -> PromptTemplate:
        """Create a LangChain prompt template for task modification"""
        template = """
You are an AI assistant helping to modify task assignments from a meeting transcript based on user feedback.

Original Meeting Transcript:
{transcript}

Current Task Assignments:
{existing_tasks}

User's Modification Request:
{modification_request}

Based on the user's request, please provide updated task assignments. Incorporate the user's modifications while keeping the original context and only include actionable tasks assigned to specific people.

{format_instructions}
"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript", "existing_tasks", "modification_request"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

    async def extract_tasks_from_transcript(self, transcript: str, additional_context: Optional[str] = None, meeting_id: str = None) -> Dict[str, Any]:
        """Extract tasks from meeting transcript using LangChain structured output with Gemini 2.5 Flash"""
        try:
            # Save the transcript before processing as requested
            self._save_raw_transcript(transcript, meeting_id)
            
            # Create the prompt template
            prompt_template = self.create_task_extraction_prompt()
            
            # Create the chain: prompt -> LLM -> parser
            chain = prompt_template | self.llm | self.output_parser
            
            # Execute the chain
            result = await chain.ainvoke({"transcript": transcript})
            
            # Convert Pydantic model to dict for compatibility with existing API
            tasks_data = []
            for task in result.tasks:
                tasks_data.append({
                    "title": task.title,
                    "task_description": task.description,  # Map to existing field name
                    "assignee_name": task.assignee,        # Map to existing field name
                    "priority": task.priority,
                    "status": task.status,
                    "deadline": task.deadline,
                    "category": task.category
                })
            
            # Save successful result
            self._save_to_output_file(
                transcript, 
                f"LANGCHAIN STRUCTURED OUTPUT SUCCESS:\n{json.dumps(tasks_data, indent=2)}", 
                tasks_data, 
                meeting_id
            )
            
            print(f"✅ Successfully extracted {len(tasks_data)} tasks using LangChain structured output")
            
            return {
                "success": True,
                "tasks": tasks_data
            }
            
        except Exception as e:
            print(f"❌ LangChain Gemini API Error: {str(e)}")
            
            # Save error details
            self._save_to_output_file(
                transcript, 
                f"LANGCHAIN ERROR:\n{str(e)}", 
                [], 
                meeting_id
            )
            
            return {
                "success": False,
                "error": f"Error processing with LangChain Gemini: {str(e)}"
            }

    async def modify_task_assignments(self, transcript: str, existing_tasks: List[Dict], modification_request: str, additional_context: Optional[str] = None) -> Dict[str, Any]:
        """Modify existing task assignments based on user request using LangChain structured output"""
        try:
            # Create the prompt template
            prompt_template = self.create_task_modification_prompt()
            
            # Create the chain: prompt -> LLM -> parser
            chain = prompt_template | self.llm | self.output_parser
            
            # Execute the chain
            result = await chain.ainvoke({
                "transcript": transcript,
                "existing_tasks": json.dumps(existing_tasks, indent=2),
                "modification_request": modification_request
            })
            
            # Convert Pydantic model to dict for compatibility with existing API
            tasks_data = []
            for task in result.tasks:
                tasks_data.append({
                    "title": task.title,
                    "task_description": task.description,  # Map to existing field name
                    "assignee_name": task.assignee,        # Map to existing field name
                    "priority": task.priority,
                    "status": task.status,
                    "deadline": task.deadline,
                    "category": task.category
                })
            
            # Save to output file for modification requests
            self._save_to_output_file(
                transcript, 
                f"MODIFICATION REQUEST: {modification_request}\n\nLangChain RESPONSE:\n{json.dumps(tasks_data, indent=2)}", 
                tasks_data, 
                "modification"
            )
            
            return {
                "success": True,
                "tasks": tasks_data
            }
            
        except Exception as e:
            print(f"❌ LangChain modification error: {str(e)}")
            return {
                "success": False,
                "error": f"Error processing modification with LangChain Gemini: {str(e)}"
            }


# Global instance
llm_service = LLMService()