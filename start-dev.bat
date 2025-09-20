@echo off
echo Starting Meeting Notes Processor...

echo.
echo Starting Backend Server...
cd backend
start "Backend" cmd /k "venv\Scripts\activate && uvicorn main:app --reload --port 8000"

echo.
echo Starting Frontend Server...
cd ..\frontend
start "Frontend" cmd /k "npm start"

echo.
echo Servers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo API Documentation will be available at: http://localhost:8000/docs
echo.
echo Press any key to close this window...
pause >nul