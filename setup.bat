@echo off
REM AI Vision Assistant Setup Script for Windows
REM This script sets up the environment for the AI Vision Assistant

echo 🤖 AI Vision Assistant Setup (Windows)
echo ==========================================

REM Check if Python 3 is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv ai_vision_env

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call ai_vision_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing Python packages...
pip install -r requirements.txt

REM Check for API key
echo.
echo 🔑 API Key Setup
echo ===============

if "%GEMINI_API_KEY%"=="" (
    echo ❌ GEMINI_API_KEY environment variable not set!
    echo.
    echo To get your Gemini API key:
    echo 1. Go to https://makersuite.google.com/app/apikey
    echo 2. Create a new API key
    echo 3. Set the environment variable in Windows:
    echo    - Press Win+R, type "sysdm.cpl", press Enter
    echo    - Click "Environment Variables"
    echo    - Add new user variable: GEMINI_API_KEY = your_api_key_here
    echo.
    echo Or set temporarily for this session:
    echo    set GEMINI_API_KEY=your_api_key_here
) else (
    echo ✅ GEMINI_API_KEY is set
)

echo.
echo 🎯 Setup Complete!
echo ==================
echo.
echo To run the AI Vision Assistant:
echo 1. Activate the virtual environment: ai_vision_env\Scripts\activate.bat
echo 2. Set your API key (if not already set): set GEMINI_API_KEY=your_key
echo 3. Run the application: python ai_vision_assistant.py
echo.
echo Troubleshooting:
echo - Make sure your webcam is connected and working
echo - Ensure microphone permissions are granted
echo - Check that speakers/headphones are connected for audio output
echo.
echo Keyboard shortcuts:
echo - Space: Start/stop voice listening
echo - Enter: Ask typed question
echo.
pause
