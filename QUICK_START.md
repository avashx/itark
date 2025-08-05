# 🤖 AI Vision Assistant - Complete Installation Guide

## 📋 Quick Start Summary

Your AI Vision Assistant is ready! Follow these final steps to get it running:

### 1. ✅ API Key Already Configured

Your Gemini API key has been set up and configured!

**API Key Status**: ✅ Active and working
**AI Connection**: ✅ Successfully tested

The API key has been added to your shell profile and will persist across sessions.

### 2. 📹 Grant Camera Access

On macOS, you'll need to grant camera access:

1. **System Preferences** → **Security & Privacy** → **Privacy** → **Camera**
2. Add **Terminal** (or your terminal app) to the list
3. Check the box to enable camera access
4. Restart your terminal

### 3. 🎤 Grant Microphone Access

Similarly for microphone:

1. **System Preferences** → **Security & Privacy** → **Privacy** → **Microphone**
2. Add **Terminal** to the list
3. Enable microphone access

### 4. 🚀 Run the Application

**Easy Launch Method:**

```bash
cd /Users/amanvashishth/CODING/itark
./run_assistant.sh
```

**Manual Method:**

```bash
cd /Users/amanvashishth/CODING/itark
source ai_vision_env/bin/activate
python3 ai_vision_assistant.py
```

## 🎮 How to Use

### GUI Controls

- **Start Assistant**: Begin camera capture and AI processing
- **🎤 Listen (Space)**: Activate voice listening mode
- **Auto-describe**: Toggle automatic scene descriptions
- **Interval**: Adjust how often AI analyzes the scene (5-60 seconds, default: 10)
- **Text input**: Type questions and press Enter

### Voice Commands

Press **Space** or click the microphone, then ask:

- "What do you see?"
- "Describe the room"
- "Is there anything dangerous?"
- "What objects are on the table?"
- "How many people are in the image?"

### Keyboard Shortcuts

- **Space**: Toggle voice listening
- **Enter**: Ask typed question

## 🔧 Test Your Setup

Run the test script first:

```bash
source ai_vision_env/bin/activate
python3 test_system.py
```

For a simple camera + AI test:

```bash
source ai_vision_env/bin/activate
python3 simple_example.py
```

## 📁 Project Files

Your complete AI Vision Assistant includes:

- **`ai_vision_assistant.py`** - Main application with GUI
- **`simple_example.py`** - Basic camera + AI test
- **`test_system.py`** - System validation script
- **`requirements.txt`** - Python dependencies
- **`setup.sh`** / **`setup.bat`** - Installation scripts
- **`README.md`** - Complete documentation
- **`TROUBLESHOOTING.md`** - Problem-solving guide
- **`config_template.py`** - Configuration template

## ⚡ Features

- **Real-time AI Vision**: Uses Google Gemini to analyze live camera feed
- **Voice Interaction**: Ask questions using speech, get spoken responses
- **Auto-descriptions**: Continuous scene narration every few seconds
- **GUI Interface**: Easy-to-use interface with live camera view
- **Free APIs**: Uses only free-tier services
- **Cross-platform**: Works on macOS, Windows, and Linux

## 🛠 Troubleshooting

If you encounter issues:

1. **Check logs**: Look at `ai_vision_assistant.log`
2. **Verify setup**: Run `python3 test_system.py`
3. **Test simple**: Run `python3 simple_example.py`
4. **Read guide**: Check `TROUBLESHOOTING.md`

## 🎯 Next Steps

Once working, you can:

1. **Customize prompts** in the code for specific use cases
2. **Adjust settings** like description intervals
3. **Add features** like wake words or multiple cameras
4. **Integrate with robots** or other hardware
5. **Deploy** as a standalone application

## 🌟 Usage Examples

Perfect for:

- **Accessibility**: Visual assistance for navigation
- **Security**: Real-time environment monitoring
- **Education**: Learning about AI and computer vision
- **Robotics**: Foundation for robot vision systems
- **Exploration**: Interactive environment discovery

---

**Happy exploring with your AI Vision Assistant!** 🤖👁️🗣️

For support, check the documentation files or the troubleshooting guide.
