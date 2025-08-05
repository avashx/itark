#!/bin/bash

# Quick Setup Script for AI Vision Assistant
# This script sets up your API key and tests the system

echo "🚀 AI Vision Assistant - Quick Setup"
echo "===================================="

# Set the API key
export GEMINI_API_KEY='AIzaSyDPYaqGAFqrySgKGyI-BUKYW6NEulelyu4'
echo "✅ API key set for this session"

# Activate virtual environment
source ai_vision_env/bin/activate
echo "✅ Virtual environment activated"

# Test the system
echo ""
echo "🧪 Running system test..."
python3 test_system.py

echo ""
echo "🎯 Setup Complete!"
echo "=================="
echo ""
echo "To run the AI Vision Assistant:"
echo "1. Run: source run_assistant.sh"
echo "   OR"
echo "2. Manual steps:"
echo "   source ai_vision_env/bin/activate"
echo "   python3 ai_vision_assistant.py"
echo ""
echo "📝 Next steps:"
echo "- Grant camera access: System Preferences > Security & Privacy > Camera"
echo "- Grant microphone access: System Preferences > Security & Privacy > Microphone" 
echo "- Add Terminal to both lists and enable permissions"
echo ""
echo "🔧 For testing without camera, run: python3 simple_example.py"
