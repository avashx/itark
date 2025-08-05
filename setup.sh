#!/bin/bash

# AI Vision Assistant Setup Script
# This script sets up the environment for the AI Vision Assistant

echo "🤖 AI Vision Assistant Setup"
echo "=============================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv ai_vision_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source ai_vision_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python packages..."
pip install -r requirements.txt

# Check for API key
echo ""
echo "🔑 API Key Setup"
echo "==============="

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY environment variable not set!"
    echo ""
    echo "To get your Gemini API key:"
    echo "1. Go to https://makersuite.google.com/app/apikey"
    echo "2. Create a new API key"
    echo "3. Set the environment variable:"
    echo "   export GEMINI_API_KEY='your_api_key_here'"
    echo ""
    echo "You can add this to your ~/.zshrc file to make it permanent:"
    echo "   echo 'export GEMINI_API_KEY=\"your_api_key_here\"' >> ~/.zshrc"
    echo "   source ~/.zshrc"
else
    echo "✅ GEMINI_API_KEY is set"
fi

echo ""
echo "🎯 Setup Complete!"
echo "=================="
echo ""
echo "To run the AI Vision Assistant:"
echo "1. Activate the virtual environment: source ai_vision_env/bin/activate"
echo "2. Set your API key (if not already set): export GEMINI_API_KEY='your_key'"
echo "3. Run the application: python3 ai_vision_assistant.py"
echo ""
echo "Troubleshooting:"
echo "- Make sure your webcam is connected and working"
echo "- Ensure microphone permissions are granted"
echo "- Check that speakers/headphones are connected for audio output"
echo ""
echo "Keyboard shortcuts:"
echo "- Space: Start/stop voice listening"
echo "- Enter: Ask typed question"
echo ""
