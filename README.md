# Meeting Notes Processor

A web application that automatically processes meeting transcripts and extracts action items, assigning them to the right people with deadlines.

## Features

- **Automated Meeting Recording**: Uses Vexa API to join Google Meet sessions and record conversations
- **AI-Powered Task Extraction**: Leverages OpenAI GPT-4 to analyze transcripts and extract actionable tasks
- **Smart Task Assignment**: Automatically assigns tasks to meeting participants with deadlines
- **Interactive Dashboard**: View, modify, and manage extracted tasks
- **Export Capabilities**: Export tasks to PDF or JSON format
- **Google Calendar Integration**: Add tasks directly to Google Calendar
- **Meeting History**: Track and manage all processed meetings

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **OpenAI API**: For LLM-powered task extraction
- **Vexa API**: For meeting recording and transcription
- **ReportLab**: PDF generation

### Frontend
- **React**: User interface framework
- **Tailwind CSS**: Styling and design
- **React Router**: Navigation
- **Axios**: API communication
- **Lucide React**: Icons

## Project Structure

```
meeting-notes-app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # API endpoints
│   │   ├── core/
│   │   │   └── config.py        # Configuration
│   │   ├── models/
│   │   │   ├── database.py      # Database models
│   │   │   └── schemas.py       # Pydantic schemas
│   │   └── services/
│   │       ├── vexa_service.py  # Vexa API integration
│   │       └── llm_service.py   # OpenAI integration
│   ├── main.py                  # FastAPI app
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
└── frontend/
    ├── src/
    │   ├── components/          # React components
    │   ├── pages/              # Page components
    │   └── services/           # API services
    ├── package.json            # Node.js dependencies
    └── public/                 # Static files
```

## Setup Instructions

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- OpenAI API key
- Vexa API access

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:
   ```
   DATABASE_URL=sqlite:///./meeting_notes.db
   VEXA_API_KEY=your_vexa_api_key_here
   VEXA_BASE_URL=https://api.cloud.vexa.ai
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_secret_key_here
   CORS_ORIGINS=http://localhost:3000
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage Flow

1. **Enter Meeting Link**: User provides Google Meet URL on the setup page
2. **Start Bot**: Bot joins the meeting and begins recording
3. **Meeting Ends**: Bot automatically leaves when meeting ends
4. **Process Transcript**: User initiates transcript processing with optional context
5. **AI Analysis**: GPT-4 analyzes transcript and extracts tasks with assignments
6. **Review & Modify**: User reviews tasks and can request modifications
7. **Export & Calendar**: Tasks can be exported to PDF/JSON or added to Google Calendar

## API Endpoints

### Meetings
- `POST /api/meetings/start` - Start a meeting bot
- `GET /api/meetings/{meeting_id}/status` - Get meeting status
- `POST /api/meetings/{meeting_id}/complete` - Complete meeting
- `GET /api/meetings/` - Get all meetings

### Transcripts
- `POST /api/transcripts/{meeting_id}/process` - Process transcript
- `GET /api/transcripts/{meeting_id}` - Get transcript

### Tasks
- `GET /api/tasks/{meeting_id}` - Get tasks for meeting
- `POST /api/tasks/{meeting_id}/modify` - Modify tasks
- `PATCH /api/tasks/{task_id}/complete` - Mark task complete
- `GET /api/tasks/{meeting_id}/export` - Export tasks JSON

### Exports
- `GET /api/exports/{meeting_id}/pdf` - Export tasks as PDF

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | Yes |
| `VEXA_API_KEY` | Vexa API key for meeting recording | Yes |
| `VEXA_BASE_URL` | Vexa API base URL | Yes |
| `OPENAI_API_KEY` | OpenAI API key for task extraction | Yes |
| `SECRET_KEY` | Secret key for JWT tokens | Yes |
| `CORS_ORIGINS` | Allowed CORS origins | Yes |

## Development

### Adding New Features

1. **Backend**: Add new routes in `app/api/routes/`
2. **Frontend**: Add new components in `src/components/` or pages in `src/pages/`
3. **Database**: Update models in `app/models/database.py`
4. **API Client**: Update API calls in `src/services/api.js`

### Testing

Run the backend tests:
```bash
cd backend
pytest
```

Run the frontend tests:
```bash
cd frontend
npm test
```

## Production Deployment

### Backend
- Use a production ASGI server like `gunicorn` with `uvicorn` workers
- Use a production database (PostgreSQL recommended)
- Set up proper environment variables
- Configure SSL/HTTPS

### Frontend
- Build the production bundle: `npm run build`
- Serve static files with a web server (nginx, Apache)
- Configure proper API URLs

## Troubleshooting

### Common Issues

1. **Bot not joining meeting**: Check Vexa API key and meeting URL format
2. **Task extraction failing**: Verify OpenAI API key and model availability
3. **CORS errors**: Ensure CORS_ORIGINS includes frontend URL
4. **Database errors**: Check database connection and permissions

### Logs

- Backend logs are available in the console when running with `--reload`
- Check browser console for frontend errors
- API documentation at `/docs` shows request/response formats

## License

This project is licensed under the MIT License.

## Support

<<<<<<< HEAD
For support, please check the documentation or create an issue in the project repository.
=======
For support, please check the documentation or create an issue in the project repository.
>>>>>>> 9b8fc4dd38cd402c6e31449910ff227e285bc971
