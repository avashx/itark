# Troubleshooting Guide - AI Vision Assistant

This guide helps resolve common issues you might encounter while setting up or running the AI Vision Assistant.

## 🔧 Installation Issues

### Python Not Found

```bash
# On macOS with Homebrew
brew install python3

# On Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# On Windows
# Download from https://www.python.org/downloads/
```

### pip Installation Failures

**On macOS:**

```bash
# If you get SSL errors
/Applications/Python\ 3.x/Install\ Certificates.command

# If you get permission errors
pip3 install --user package_name
```

**On Linux:**

```bash
# Missing development headers
sudo apt-get install python3-dev python3-setuptools

# For audio packages
sudo apt-get install portaudio19-dev python3-pyaudio
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
```

**On Windows:**

```batch
# Run Command Prompt as Administrator
# Install Microsoft C++ Build Tools if needed
```

### Specific Package Issues

**OpenCV (cv2):**

```bash
# If import cv2 fails
pip uninstall opencv-python
pip install opencv-python-headless

# On Linux, you might need
sudo apt-get install python3-opencv
```

**PyAudio Issues:**

```bash
# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt-get install python3-pyaudio

# Windows - use precompiled wheel
pip install pipwin
pipwin install pyaudio
```

**Google Generative AI:**

```bash
# Make sure you have the latest version
pip install --upgrade google-generativeai
```

## 🔑 API Key Issues

### Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the generated key

### Setting API Key

**macOS/Linux:**

```bash
# Temporary (current session only)
export GEMINI_API_KEY='your_api_key_here'

# Permanent (add to shell profile)
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc

# For bash users
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**

```batch
# Temporary (current session)
set GEMINI_API_KEY=your_api_key_here

# Permanent (through GUI)
# Windows Key + R -> sysdm.cpl -> Environment Variables
# Add User Variable: GEMINI_API_KEY = your_api_key_here

# Permanent (command line)
setx GEMINI_API_KEY "your_api_key_here"
```

### API Key Validation

```bash
# Test if API key is set
echo $GEMINI_API_KEY  # macOS/Linux
echo %GEMINI_API_KEY%  # Windows

# Run the test script
python3 test_system.py
```

## 📷 Camera Issues

### Camera Not Detected

```python
# Try different camera indices
camera = cv2.VideoCapture(0)  # Built-in camera
camera = cv2.VideoCapture(1)  # USB camera #1
camera = cv2.VideoCapture(2)  # USB camera #2
```

### Permission Issues

**macOS:**

1. System Preferences → Security & Privacy → Privacy
2. Camera → Add Terminal/VS Code/Python
3. Restart the application

**Linux:**

```bash
# Add user to video group
sudo usermod -a -G video $USER
# Log out and log back in

# Check camera permissions
ls -l /dev/video*
```

**Windows:**

1. Settings → Privacy → Camera
2. Allow apps to access camera
3. Allow desktop apps to access camera

### Camera Already in Use

```bash
# Kill processes using camera
# macOS/Linux
lsof /dev/video0
kill -9 <process_id>

# Or restart the camera service
sudo modprobe -r uvcvideo
sudo modprobe uvcvideo
```

## 🎤 Microphone Issues

### Microphone Not Working

**Check System Audio:**

```bash
# macOS - check System Preferences → Sound → Input
# Linux - check audio settings or use alsamixer
# Windows - check Sound settings
```

**Test Microphone:**

```python
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, timeout=5)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
    except:
        print("Could not understand")
```

### Permission Issues

**macOS:**

1. System Preferences → Security & Privacy → Privacy
2. Microphone → Add Terminal/VS Code/Python

**Linux:**

```bash
# Install PulseAudio if needed
sudo apt-get install pulseaudio pulseaudio-utils

# Test microphone
arecord -l  # List audio devices
```

## 🔊 Audio Playback Issues

### No Sound Output

**Check Audio System:**

```python
import pygame
pygame.mixer.init()
print("Audio drivers:", pygame.mixer.get_init())
```

**Test Audio:**

```bash
# macOS/Linux - test system audio
speaker-test -t wav -c 2  # Linux
say "test"  # macOS

# Windows
# Use Windows Sound settings to test
```

### Pygame Audio Issues

```bash
# Reinstall pygame
pip uninstall pygame
pip install pygame

# On Linux, install SDL2
sudo apt-get install libsdl2-mixer-2.0-0
```

## 🌐 Network and API Issues

### Internet Connection

```bash
# Test basic connectivity
ping google.com

# Test HTTPS (for API calls)
curl -I https://generativelanguage.googleapis.com
```

### API Rate Limits

- Gemini free tier: 15 requests per minute
- Monitor usage in the app status bar
- Wait before retrying if you hit limits

### Firewall Issues

```bash
# Check if Python can access internet
python3 -c "import urllib.request; print('OK' if urllib.request.urlopen('https://google.com') else 'FAIL')"
```

## 🖥️ Performance Issues

### High CPU Usage

- Reduce camera FPS in code
- Increase description interval
- Resize images more aggressively

### Memory Issues

```python
# Monitor memory usage
import psutil
print(f"Memory usage: {psutil.virtual_memory().percent}%")
```

### Slow Response Times

- Check internet speed
- Use smaller images for AI processing
- Consider local AI models for faster processing

## 🐛 Application-Specific Issues

### GUI Not Showing

```bash
# On Linux, install tkinter
sudo apt-get install python3-tk

# On macOS, ensure Python has GUI support
# Use Python from python.org, not system Python
```

### Threading Issues

- Close all camera applications before running
- Restart the application if threads become unresponsive
- Check system resource usage

### Log Files

Check `ai_vision_assistant.log` for detailed error information:

```bash
tail -f ai_vision_assistant.log  # Watch logs in real-time
```

## 📱 Platform-Specific Notes

### macOS

- Use Python from python.org, not system Python
- Grant all necessary permissions in System Preferences
- Use Homebrew for system dependencies

### Linux

- Install system packages for audio/video
- Check user permissions for devices
- Some distributions need additional codecs

### Windows

- Run Command Prompt as Administrator for installations
- Use Windows Store Python or python.org installer
- Install Visual C++ Build Tools if needed

## 🔄 Reset and Clean Installation

If all else fails, try a clean installation:

```bash
# Remove virtual environment
rm -rf ai_vision_env

# Clear pip cache
pip cache purge

# Start fresh
python3 -m venv ai_vision_env
source ai_vision_env/bin/activate  # or ai_vision_env\Scripts\activate.bat on Windows
pip install --upgrade pip
pip install -r requirements.txt
```

## 📞 Getting Help

1. **Check logs:** `ai_vision_assistant.log`
2. **Run test script:** `python3 test_system.py`
3. **Test simple example:** `python3 simple_example.py`
4. **Verify environment:** Check all environment variables
5. **System diagnostics:** Check camera, microphone, speakers separately

## 🎯 Quick Fixes Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] GEMINI_API_KEY environment variable set
- [ ] Camera permissions granted
- [ ] Microphone permissions granted
- [ ] Internet connection working
- [ ] No other apps using camera/microphone
- [ ] Audio output working (test with music/videos)

Most issues are related to permissions, missing dependencies, or API configuration. Follow this guide step by step to resolve them!
