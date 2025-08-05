#!/usr/bin/env python3
"""
AI Vision Assistant Test Script
Verifies that all dependencies are properly installed and working.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing imports...")
    
    tests = [
        ("cv2", "OpenCV"),
        ("google.generativeai", "Google Generative AI"),
        ("gtts", "Google Text-to-Speech"), 
        ("speech_recognition", "Speech Recognition"),
        ("pyttsx3", "pyttsx3 TTS"),
        ("pygame", "Pygame"),
        ("PIL", "Pillow"),
        ("tkinter", "Tkinter GUI"),
        ("numpy", "NumPy")
    ]
    
    failed = []
    
    for module, name in tests:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed.append(name)
    
    return failed

def test_camera():
    """Test camera access."""
    print("\n📷 Testing camera access...")
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            ret, frame = camera.read()
            if ret:
                print("✅ Camera working - captured frame")
                print(f"   Frame shape: {frame.shape}")
            else:
                print("❌ Camera opened but cannot capture frames")
            camera.release()
        else:
            print("❌ Cannot open camera")
    except Exception as e:
        print(f"❌ Camera test failed: {e}")

def test_microphone():
    """Test microphone access."""
    print("\n🎤 Testing microphone access...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("✅ Microphone accessible")
            print("   Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone calibrated")
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")

def test_audio_playback():
    """Test audio playback."""
    print("\n🔊 Testing audio playback...")
    try:
        import pygame
        pygame.mixer.init()
        print("✅ Pygame audio system initialized")
        pygame.mixer.quit()
    except Exception as e:
        print(f"❌ Audio playback test failed: {e}")

def test_tts():
    """Test text-to-speech."""
    print("\n🗣️ Testing text-to-speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"✅ pyttsx3 TTS initialized with {len(voices)} voices")
        engine.stop()
    except Exception as e:
        print(f"❌ TTS test failed: {e}")

def test_api_key():
    """Test API key configuration."""
    print("\n🔑 Testing API key...")
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ GEMINI_API_KEY environment variable is set")
        if len(api_key) > 20:
            print(f"   Key length: {len(api_key)} characters")
        else:
            print("⚠️  API key seems too short - please verify")
    else:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("   Please set it with: export GEMINI_API_KEY='your_key_here'")

def test_ai_connection():
    """Test AI model connection."""
    print("\n🤖 Testing AI model connection...")
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Cannot test AI - no API key")
        return
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test
        response = model.generate_content("Say 'Hello, AI Vision Assistant test successful!'")
        print("✅ AI model connection successful")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ AI model test failed: {e}")

def main():
    """Run all tests."""
    print("🔍 AI Vision Assistant - System Test")
    print("=" * 40)
    
    # Test imports
    failed_imports = test_imports()
    
    if failed_imports:
        print(f"\n❌ Some imports failed: {', '.join(failed_imports)}")
        print("Please install missing dependencies with:")
        print("pip install -r requirements.txt")
        return False
    
    # Test hardware
    test_camera()
    test_microphone() 
    test_audio_playback()
    test_tts()
    
    # Test API
    test_api_key()
    test_ai_connection()
    
    print("\n" + "=" * 40)
    print("🎯 Test completed!")
    print("\nIf all tests passed, you can run the main application:")
    print("python3 ai_vision_assistant.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test script error: {e}")
        sys.exit(1)
