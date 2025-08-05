#!/bin/bash

# Launch AI Vision Assistant
# This script activates the environment and starts the application

echo "🤖 Starting AI Vision Assistant..."

# Set the API key
export GEMINI_API_KEY='AIzaSyDPYaqGAFqrySgKGyI-BUKYW6NEulelyu4'

# Activate virtual environment
source ai_vision_env/bin/activate

# Run the application
python3 ai_vision_assistant.py
