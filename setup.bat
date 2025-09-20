@echo off
echo Setting up Meeting Notes Processor...

echo.
echo Creating Python virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installing Node.js dependencies...
cd ..\frontend
npm install

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Configure your .env file in the backend directory with your API keys
echo 2. Run start-dev.bat to start both servers
echo.
echo Required environment variables:
echo - VEXA_API_KEY: Your Vexa API key
echo - OPENAI_API_KEY: Your OpenAI API key
echo - SECRET_KEY: A secret key for JWT tokens
echo.
pause