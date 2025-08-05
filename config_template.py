# AI Vision Assistant Configuration
# Copy this file to config.py and customize as needed

# Camera settings
CAMERA_INDEX = 0  # 0 for built-in camera, 1, 2, etc. for USB cameras
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# AI processing settings  
DESCRIPTION_INTERVAL = 3  # seconds between auto-descriptions
IMAGE_MAX_WIDTH = 800  # resize images to this width for AI processing
IMAGE_QUALITY = 85  # JPEG quality (1-100)

# Speech settings
TTS_RATE = 150  # words per minute for text-to-speech
VOICE_TIMEOUT = 5  # seconds to wait for voice input
PHRASE_TIME_LIMIT = 10  # max seconds for a single phrase

# GUI settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
VIDEO_DISPLAY_WIDTH = 400
VIDEO_DISPLAY_HEIGHT = 300

# API settings
GEMINI_MODEL = "gemini-1.5-flash"  # AI model to use
MAX_API_CALLS_PER_HOUR = 50  # self-imposed limit to avoid overuse

# Prompts
DEFAULT_PROMPT = """Describe what you see in this image in detail. Focus on:
- Objects and people present
- The environment and setting  
- Any potential hazards or points of interest
- Spatial relationships and layout
- Lighting and atmosphere
Keep the description conversational and helpful for someone who cannot see the image."""

QUESTION_PROMPT_TEMPLATE = "Looking at this image, please answer: {question}. Be descriptive and helpful."

# Audio file settings
TEMP_AUDIO_DIR = "/tmp"  # directory for temporary audio files
AUDIO_FORMAT = "mp3"

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "ai_vision_assistant.log"
MAX_LOG_SIZE_MB = 10

# Development/Debug settings
DEBUG_MODE = False  # enables additional logging and error details
SAVE_DEBUG_IMAGES = False  # save processed images for debugging
DEBUG_IMAGE_DIR = "debug_images"
