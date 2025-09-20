from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Task, Meeting
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from fastapi.responses import FileResponse
import tempfile
import os
from datetime import datetime

router = APIRouter()


def generate_pdf_report(meeting: Meeting, tasks: list) -> str:
    """Generate a PDF report for meeting tasks"""
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    
    # Create PDF document
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceBefore=12,
        spaceAfter=30,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceBefore=20,
        spaceAfter=12,
    )
    
    # Title
    title = Paragraph("Meeting Action Items Report", title_style)
    story.append(title)
    
    # Meeting info
    meeting_info = f"""
    <b>Meeting ID:</b> {meeting.meeting_id}<br/>
    <b>Meeting Date:</b> {meeting.created_at.strftime('%B %d, %Y at %I:%M %p')}<br/>
    <b>Status:</b> {meeting.status.title()}<br/>
    <b>Total Tasks:</b> {len(tasks)}
    """
    story.append(Paragraph(meeting_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Group tasks by assignee
    tasks_by_assignee = {}
    for task in tasks:
        assignee = task.assignee_name
        if assignee not in tasks_by_assignee:
            tasks_by_assignee[assignee] = []
        tasks_by_assignee[assignee].append(task)
    
    # Add tasks for each assignee
    for assignee, assignee_tasks in tasks_by_assignee.items():
        # Assignee heading
        assignee_heading = Paragraph(f"Tasks for {assignee}", heading_style)
        story.append(assignee_heading)
        
        # Task table
        task_data = [['Task Description', 'Deadline', 'Priority', 'Status']]
        
        for task in assignee_tasks:
            status = "✓ Completed" if task.is_completed else "○ Pending"
            task_data.append([
                task.task_description[:60] + "..." if len(task.task_description) > 60 else task.task_description,
                task.deadline or "Not specified",
                task.priority or "Not specified",
                status
            ])
        
        task_table = Table(task_data, colWidths=[3*inch, 1.2*inch, 0.8*inch, 1*inch])
        task_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        story.append(task_table)
        story.append(Spacer(1, 20))
    
    # Summary
    completed_tasks = sum(1 for task in tasks if task.is_completed)
    pending_tasks = len(tasks) - completed_tasks
    
    summary_heading = Paragraph("Summary", heading_style)
    story.append(summary_heading)
    
    summary_text = f"""
    <b>Total Tasks:</b> {len(tasks)}<br/>
    <b>Completed Tasks:</b> {completed_tasks}<br/>
    <b>Pending Tasks:</b> {pending_tasks}<br/>
    <b>Completion Rate:</b> {(completed_tasks/len(tasks)*100) if len(tasks) > 0 else 0:.1f}%<br/>
    <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    return temp_file.name


@router.get("/{meeting_id}/pdf")
async def export_tasks_pdf(meeting_id: str, db: Session = Depends(get_db)):
    """Export tasks as PDF"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    tasks = db.query(Task).filter(Task.meeting_id == meeting.id).all()
    
    try:
        pdf_path = generate_pdf_report(meeting, tasks)
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"meeting-tasks-{meeting_id}.pdf",
            background=lambda: os.unlink(pdf_path)  # Clean up temp file after response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")