# AI Vision Assistant

A real-time desktop application that uses your webcam and AI to describe surroundings with voice interaction capabilities. Think of it as an AI-powered visual assistant that can see through your camera and communicate with you through voice.

## 🌟 Features

- **Real-time Visual Analysis**: Continuously captures webcam feed and analyzes scenes using Google's Gemini AI
- **Voice Interaction**: Ask questions about what the camera sees using voice commands (like Alexa)
- **Text-to-Speech**: AI responses are spoken aloud using natural-sounding speech
- **Auto-Description Mode**: Automatic scene descriptions every few seconds
- **GUI Interface**: User-friendly interface with live camera feed and text logs
- **Free APIs**: Uses only free-tier APIs (Google Gemini, Google Text-to-Speech)
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🎯 Use Cases

- **Accessibility**: Visual assistance for people with visual impairments
- **Navigation**: Real-time environment description for navigation
- **Security**: Monitor surroundings and identify potential hazards
- **Exploration**: Describe new environments and objects
- **Robot Integration**: Foundation for robot vision systems

## 📋 Requirements

- Python 3.8 or higher
- Webcam (built-in or USB)
- Microphone for voice input
- Speakers/headphones for audio output
- Google Gemini API key (free tier available)
- Internet connection for AI processing

## 🚀 Quick Start

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### 2. Clone and Setup

```bash
# Clone or download the files
cd /path/to/ai-vision-assistant

# Run the setup script (on macOS/Linux)
./setup.sh

# Or install manually:
python3 -m venv ai_vision_env
source ai_vision_env/bin/activate
pip install -r requirements.txt
```

### 3. Set Your API Key

```bash
# Set for current session
export GEMINI_API_KEY='your_api_key_here'

# Or add to your shell profile for permanent setup
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Run the Application

```bash
# Activate virtual environment
source ai_vision_env/bin/activate

# Run the application
python3 ai_vision_assistant.py
```

## 🎮 How to Use

### GUI Controls

1. **Start Assistant**: Click to begin camera capture and AI processing
2. **Listen Button (🎤)**: Click or press Space to activate voice listening
3. **Auto-describe**: Toggle automatic scene descriptions
4. **Question Entry**: Type questions and press Enter
5. **Status Bar**: Shows current activity and API usage

### Voice Commands

- Press **Space** or click the microphone button to start listening
- Ask questions like:
  - "What do you see?"
  - "Describe the room"
  - "Is there anything dangerous?"
  - "What objects are on the table?"
  - "How many people are in the image?"

### Keyboard Shortcuts

- **Space**: Toggle voice listening
- **Enter**: Ask typed question

## 🛠 Technical Details

### Architecture

- **Camera Thread**: Captures frames from webcam at ~10 FPS
- **AI Processing Thread**: Analyzes images and generates descriptions
- **Voice Thread**: Handles speech recognition and voice commands
- **Main GUI Thread**: Updates interface and handles user interactions

### AI Model

- Uses Google's Gemini 1.5 Flash model for image analysis
- Optimized prompts for environmental description and safety
- Images resized to 800px width max to reduce API costs
- Base64 encoding for efficient image transmission

### Audio System

- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: Google Text-to-Speech (gTTS) with pygame playback
- **Fallback TTS**: pyttsx3 for offline text-to-speech
- Automatic ambient noise adjustment for better recognition

### Performance Optimizations

- Image resizing before AI processing to reduce costs and latency
- Queue-based frame processing to prevent memory buildup
- Threaded architecture for responsive UI
- Configurable description intervals

## 📦 Dependencies

| Package             | Purpose                              |
| ------------------- | ------------------------------------ |
| opencv-python       | Camera capture and image processing  |
| google-generativeai | Gemini AI model integration          |
| gtts                | Google Text-to-Speech                |
| SpeechRecognition   | Voice input processing               |
| pyttsx3             | Offline text-to-speech fallback      |
| pygame              | Audio playback                       |
| Pillow              | Image manipulation                   |
| pyaudio             | Microphone audio capture             |
| tkinter             | GUI framework (included with Python) |

## ⚙️ Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Adjustable Settings

In the code, you can modify:

- `description_interval`: Time between auto-descriptions (default: 10 seconds, adjustable via GUI)
- Camera resolution: Default 640x480, adjustable in `setup_camera()`
- TTS speaking rate: Default 150 WPM, adjustable in `setup_audio()`
- Image quality: JPEG quality for AI processing (default: 85%)

## 🔧 Troubleshooting

### Common Issues

**Camera not working:**

- Check if camera is connected and not used by another app
- On macOS: Grant camera permissions in System Preferences > Security & Privacy
- Try different camera index in `cv2.VideoCapture(0)` (0, 1, 2, etc.)

**Microphone not working:**

- Grant microphone permissions in system settings
- Check if microphone is working in other applications
- Install pyaudio properly (may need system dependencies)

**Audio playback issues:**

- Check speaker/headphone connections
- Ensure pygame is properly installed
- Try adjusting system volume

**API errors:**

- Verify GEMINI_API_KEY is set correctly
- Check internet connection
- Monitor API usage limits (free tier has daily limits)

### macOS-specific Setup

If you encounter issues with pyaudio on macOS:

```bash
# Install PortAudio first
brew install portaudio

# Then install pyaudio
pip install pyaudio
```

### Linux-specific Setup

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev python3-dev

# Install espeak for pyttsx3
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
```

## 🔒 Privacy and Security

- All AI processing happens through Google's Gemini API
- Images are sent to Google's servers for analysis
- No data is stored locally except in temporary files during TTS
- API key should be kept secure and not shared
- Consider network security when using in sensitive environments

## 📈 API Usage and Costs

- **Gemini API**: Free tier includes generous daily limits
- **Google Speech Recognition**: Free with usage limits
- **Google Text-to-Speech**: Free with usage limits
- Monitor usage in the app's status bar
- For heavy usage, consider paid tiers or alternative models

## 🔄 Future Enhancements

Potential improvements and extensions:

- **Offline AI models**: Local processing using ONNX or similar
- **Robot integration**: ROS compatibility for robotics projects
- **Multi-language support**: Support for different languages
- **Custom wake words**: "Hey Assistant" activation
- **Mobile app**: iOS/Android versions
- **Cloud storage**: Save interesting observations
- **Multiple cameras**: Support for multiple camera inputs
- **Advanced prompts**: Specialized prompts for different scenarios

## 🤝 Contributing

This is a foundation project that can be extended for various use cases:

1. **Fork the repository**
2. **Create feature branches** for new capabilities
3. **Add robust error handling** for production use
4. **Optimize performance** for your specific hardware
5. **Add new AI models** for different capabilities

## 📄 License

This project is provided as-is for educational and personal use. Please respect the terms of service of the APIs used (Google Gemini, Google Speech Recognition, etc.).

## 🆘 Support

If you encounter issues:

1. Check the application logs in `ai_vision_assistant.log`
2. Verify all dependencies are installed correctly
3. Ensure API keys are set properly
4. Test camera and microphone separately
5. Check system permissions for camera and microphone access

## 🎉 Acknowledgments

- Google AI for the Gemini API
- OpenCV community for computer vision tools
- Python community for excellent libraries
- Open source contributors for speech recognition and TTS libraries

---

**Happy exploring with your AI Vision Assistant!** 🤖👁️🗣️
