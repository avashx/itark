#!/usr/bin/env python3
"""
AI Vision Assistant - Real-time visual analysis with voice interaction
A desktop application that uses webcam feed and AI to describe surroundings
with voice communication capabilities.
"""

import cv2
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import os
import pygame
import tempfile
from datetime import datetime
import logging
from typing import Optional, Tuple
import queue
import io
from PIL import Image, ImageTk
import base64
import numpy as np

# AI and speech libraries
import google.generativeai as genai
from gtts import gTTS
import speech_recognition as sr
import pyttsx3
import requests
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_vision_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VisionAssistant:
    """Main class for the AI Vision Assistant application."""
    
    def __init__(self):
        """Initialize the Vision Assistant."""
        # Initialize control flags first
        self.is_running = False
        self.is_listening = False
        self.auto_describe = True
        self.last_description_time = 0
        self.description_interval = 10  # seconds (reduced frequency)
        
        # Speech settings
        self.speaking_speed = 1.2  # 1.2x speed (faster)
        self.voice_language = 'en'  # en, hi
        self.voice_accent = 'us'  # us, uk, au, in
        self.use_google_tts_api = True
        self.response_language = 'en'  # Language for AI responses
        
        # Initialize systems
        self.setup_ai()
        self.setup_audio()
        self.setup_camera()
        self.setup_gui()
        
        # Queues for thread communication
        self.image_queue = queue.Queue(maxsize=2)
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()
        
        # Current frame
        self.current_frame = None
        
    def setup_ai(self):
        """Initialize AI models and APIs."""
        try:
            # Check for Gemini API key
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set")
            
            genai.configure(api_key=api_key)
            self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Test the AI connection
            test_response = self.ai_model.generate_content("Test connection")
            logger.info("AI model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI model: {e}")
            messagebox.showerror("AI Setup Error", 
                               f"Failed to initialize AI model.\n"
                               f"Please ensure GEMINI_API_KEY is set.\n"
                               f"Error: {e}")
            self.ai_model = None
    
    def setup_audio(self):
        """Initialize audio components."""
        try:
            # Initialize pygame for audio playback
            pygame.mixer.init()
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 200)  # Faster speaking rate
            
            # Set voice if available
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a female voice or use the first available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Google TTS API setup
            self.google_tts_api_key = "AIzaSyBCBpgFA3Ap4IIR_jkQqH3mNFKEBXCFqSA"
            
            logger.info("Audio systems initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize audio: {e}")
            messagebox.showerror("Audio Setup Error", 
                               f"Failed to initialize audio systems.\n"
                               f"Error: {e}")
    
    def setup_camera(self):
        """Initialize camera."""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise RuntimeError("Cannot access webcam")
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            logger.info("Camera initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            messagebox.showerror("Camera Setup Error", 
                               f"Failed to initialize camera.\n"
                               f"Error: {e}")
            self.camera = None
    
    def setup_gui(self):
        """Create the GUI interface."""
        self.root = tk.Tk()
        self.root.title("AI Vision Assistant")
        self.root.geometry("1000x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create main frames
        self.create_control_frame()
        self.create_video_frame()
        self.create_text_frame()
        self.create_status_frame()
        
        # Bind keyboard shortcuts
        self.root.bind('<space>', lambda e: self.toggle_listening())
        self.root.bind('<Return>', lambda e: self.ask_question())
        
    def create_control_frame(self):
        """Create control buttons frame."""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, padx=10, fill='x')
        
        # Start/Stop button
        self.start_button = ttk.Button(
            control_frame, 
            text="Start Assistant", 
            command=self.toggle_assistant
        )
        self.start_button.pack(side='left', padx=5)
        
        # Voice control button
        self.voice_button = ttk.Button(
            control_frame, 
            text="🎤 Listen (Space)", 
            command=self.toggle_listening
        )
        self.voice_button.pack(side='left', padx=5)
        
        # Auto-describe toggle
        self.auto_var = tk.BooleanVar(value=True)
        self.auto_check = ttk.Checkbutton(
            control_frame, 
            text="Auto-describe", 
            variable=self.auto_var,
            command=self.toggle_auto_describe
        )
        self.auto_check.pack(side='left', padx=5)
        
        # Interval setting
        interval_frame = ttk.Frame(control_frame)
        interval_frame.pack(side='left', padx=5)
        
        ttk.Label(interval_frame, text="Interval:").pack(side='left')
        self.interval_var = tk.StringVar(value=str(self.description_interval))
        self.interval_spinbox = ttk.Spinbox(
            interval_frame,
            from_=5, 
            to=60,
            width=4,
            textvariable=self.interval_var,
            command=self.update_interval
        )
        self.interval_spinbox.pack(side='left', padx=2)
        ttk.Label(interval_frame, text="sec").pack(side='left')
        
        # Voice settings
        voice_frame = ttk.Frame(control_frame)
        voice_frame.pack(side='left', padx=5)
        
        # Language selection
        ttk.Label(voice_frame, text="Lang:").pack(side='left')
        self.language_var = tk.StringVar(value=self.response_language)
        self.language_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.language_var,
            values=['en', 'hi'],
            width=3,
            state='readonly'
        )
        self.language_combo.pack(side='left', padx=2)
        self.language_combo.bind('<<ComboboxSelected>>', self.update_response_language)
        
        # Voice accent selection
        ttk.Label(voice_frame, text="Voice:").pack(side='left')
        self.voice_var = tk.StringVar(value=self.voice_accent)
        self.voice_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            values=['us', 'uk', 'au', 'in'],
            width=4,
            state='readonly'
        )
        self.voice_combo.pack(side='left', padx=2)
        self.voice_combo.bind('<<ComboboxSelected>>', self.update_voice_accent)
        
        # Speed control
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(side='left', padx=5)
        
        ttk.Label(speed_frame, text="Speed:").pack(side='left')
        self.speed_var = tk.StringVar(value=str(self.speaking_speed))
        self.speed_spinbox = ttk.Spinbox(
            speed_frame,
            from_=0.5,
            to=2.0,
            increment=0.1,
            width=4,
            textvariable=self.speed_var,
            command=self.update_speaking_speed
        )
        self.speed_spinbox.pack(side='left', padx=2)
        ttk.Label(speed_frame, text="x").pack(side='left')
        
        # TTS Quality toggle
        self.tts_quality_var = tk.BooleanVar(value=self.use_google_tts_api)
        self.tts_quality_check = ttk.Checkbutton(
            control_frame,
            text="HD Voice",
            variable=self.tts_quality_var,
            command=self.toggle_tts_quality
        )
        self.tts_quality_check.pack(side='left', padx=5)
        
        # Question entry
        self.question_var = tk.StringVar()
        self.question_entry = ttk.Entry(
            control_frame, 
            textvariable=self.question_var,
            width=30
        )
        self.question_entry.pack(side='left', padx=5, fill='x', expand=True)
        self.question_entry.bind('<Return>', lambda e: self.ask_question())
        
        # Ask button
        self.ask_button = ttk.Button(
            control_frame, 
            text="Ask (Enter)", 
            command=self.ask_question
        )
        self.ask_button.pack(side='right', padx=5)
    
    def create_video_frame(self):
        """Create video display frame."""
        video_frame = ttk.LabelFrame(self.root, text="Camera Feed")
        video_frame.pack(pady=5, padx=10, fill='both', expand=True)
        
        self.video_label = ttk.Label(video_frame)
        self.video_label.pack(pady=10)
    
    def create_text_frame(self):
        """Create text log frame."""
        text_frame = ttk.LabelFrame(self.root, text="AI Descriptions")
        text_frame.pack(pady=5, padx=10, fill='both', expand=True)
        
        self.text_log = scrolledtext.ScrolledText(
            text_frame, 
            height=8, 
            wrap=tk.WORD,
            state='disabled'
        )
        self.text_log.pack(pady=5, padx=5, fill='both', expand=True)
    
    def create_status_frame(self):
        """Create status bar."""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side='left')
        
        # API usage counter
        self.api_count_var = tk.StringVar(value="API calls: 0")
        self.api_label = ttk.Label(status_frame, textvariable=self.api_count_var)
        self.api_label.pack(side='right')
        
        self.api_call_count = 0
    
    def update_status(self, message: str):
        """Update status bar."""
        self.status_var.set(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update_idletasks()
    
    def log_text(self, text: str, prefix: str = ""):
        """Add text to the log display."""
        self.text_log.config(state='normal')
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.text_log.insert(tk.END, f"[{timestamp}] {prefix}{text}\n\n")
        self.text_log.see(tk.END)
        self.text_log.config(state='disabled')
        self.root.update_idletasks()
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """Capture a frame from the camera."""
        if not self.camera or not self.camera.isOpened():
            return None
        
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None
    
    def prepare_image_for_ai(self, frame: np.ndarray) -> str:
        """Prepare image for AI analysis by converting to base64."""
        try:
            # Resize image to reduce API costs
            height, width = frame.shape[:2]
            if width > 800:
                scale = 800 / width
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Convert to base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=85)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Error preparing image for AI: {e}")
            return None
    
    def analyze_image_with_ai(self, image_data: str, question: str = None) -> str:
        """Analyze image using AI model."""
        if not self.ai_model:
            return "AI model not available"
        
        try:
            # Prepare the prompt based on language
            if self.response_language == 'hi':
                if question:
                    prompt = f"इस छवि को देखते हुए, कृपया उत्तर दें: {question}। विस्तार से और सहायक तरीके से बताएं।"
                else:
                    prompt = """इस छवि में आप जो कुछ देख रहे हैं उसका विस्तार से वर्णन करें। इन बातों पर ध्यान दें:
- मौजूद वस्तुएं और लोग
- वातावरण और परिवेश
- कोई संभावित खतरे या रुचि के बिंदु
- स्थानिक संबंध और लेआउट
- प्रकाश और माहौल
वर्णन को बातचीत के अंदाज में और उस व्यक्ति के लिए सहायक बनाएं जो छवि नहीं देख सकता।"""
            else:
                if question:
                    prompt = f"Looking at this image, please answer: {question}. Be descriptive and helpful."
                else:
                    prompt = """Describe what you see in this image in detail. Focus on:
- Objects and people present
- The environment and setting
- Any potential hazards or points of interest
- Spatial relationships and layout
- Lighting and atmosphere
Keep the description conversational and helpful for someone who cannot see the image."""
            
            # Add language instruction
            if self.response_language == 'hi':
                prompt += "\n\nकृपया अपना उत्तर हिंदी में दें।"
            else:
                prompt += "\n\nPlease respond in English."
            
            # Prepare image for Gemini
            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                }
            ]
            
            # Generate response
            response = self.ai_model.generate_content([prompt, image_parts[0]])
            
            self.api_call_count += 1
            self.api_count_var.set(f"API calls: {self.api_call_count}")
            
            return response.text
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            error_msg = "छवि विश्लेषण में त्रुटि" if self.response_language == 'hi' else "Error analyzing image"
            return f"{error_msg}: {str(e)}"
    
    def speak_text(self, text: str):
        """Convert text to speech and play it."""
        try:
            # Try Google Cloud TTS API first for better quality
            if self.use_google_tts_api and self.google_tts_api_key:
                success = self.speak_with_google_cloud_tts(text)
                if success:
                    return
            
            # Fallback to gTTS with accent and speed
            self.speak_with_gtts(text)
                
        except Exception as e:
            logger.error(f"TTS error: {e}")
            # Final fallback to pyttsx3
            self.speak_with_pyttsx3(text)
    
    def speak_with_google_cloud_tts(self, text: str) -> bool:
        """Use Google Cloud Text-to-Speech API for high-quality speech."""
        try:
            # Voice name mapping for different languages and accents
            if self.voice_language == 'hi':
                voice_names = {
                    'us': 'hi-IN-Neural2-A',  # Hindi voice
                    'uk': 'hi-IN-Neural2-B',  # Alternative Hindi voice
                    'au': 'hi-IN-Neural2-C',  # Alternative Hindi voice
                    'in': 'hi-IN-Neural2-D'   # Alternative Hindi voice
                }
                language_code = "hi-IN"
            else:
                voice_names = {
                    'us': 'en-US-Neural2-F',  # Female US voice
                    'uk': 'en-GB-Neural2-F',  # Female UK voice
                    'au': 'en-AU-Neural2-F',  # Female AU voice
                    'in': 'en-IN-Neural2-F'   # Female IN voice
                }
                language_code = "en-US"
            
            voice_name = voice_names.get(self.voice_accent, voice_names['us'])
            
            # Prepare request
            url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.google_tts_api_key}"
            
            payload = {
                "input": {"text": text},
                "voice": {
                    "languageCode": language_code,
                    "name": voice_name
                },
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "speakingRate": self.speaking_speed,
                    "pitch": 0.0,
                    "volumeGainDb": 0.0
                }
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                audio_data = response.json().get('audioContent')
                if audio_data:
                    # Decode base64 audio
                    import base64
                    audio_bytes = base64.b64decode(audio_data)
                    
                    # Save and play
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                        tmp_file.write(audio_bytes)
                        
                        pygame.mixer.music.load(tmp_file.name)
                        pygame.mixer.music.play()
                        
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                        
                        os.unlink(tmp_file.name)
                    
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Google Cloud TTS error: {e}")
            return False
    
    def speak_with_gtts(self, text: str):
        """Use gTTS as fallback with accent and language support."""
        try:
            # Language and TLD mapping
            if self.voice_language == 'hi':
                # Hindi language - use Indian TLD
                lang = 'hi'
                tld = 'co.in'
            else:
                # English language with accent support
                lang = 'en'
                tld_map = {
                    'us': 'com',
                    'uk': 'co.uk', 
                    'au': 'com.au',
                    'in': 'co.in'
                }
                tld = tld_map.get(self.voice_accent, 'com')
            
            # Use gTTS with language and accent
            tts = gTTS(
                text=text, 
                lang=lang, 
                tld=tld,
                slow=(self.speaking_speed < 1.0)
            )
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                os.unlink(tmp_file.name)
                
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            self.speak_with_pyttsx3(text)
    
    def speak_with_pyttsx3(self, text: str):
        """Final fallback using pyttsx3."""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"pyttsx3 TTS error: {e}")
            self.update_status("Speech synthesis failed")
    
    def listen_for_speech(self) -> Optional[str]:
        """Listen for speech input."""
        try:
            with self.microphone as source:
                self.update_status("Listening for speech...")
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            self.update_status("Processing speech...")
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            return text.lower()
            
        except sr.WaitTimeoutError:
            self.update_status("No speech detected")
            return None
        except sr.UnknownValueError:
            self.update_status("Could not understand speech")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            self.update_status("Speech recognition error")
            return None
    
    def update_video_display(self, frame: np.ndarray):
        """Update the video display with current frame."""
        try:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Resize for display
            display_size = (400, 300)
            pil_image = pil_image.resize(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Update label
            self.video_label.configure(image=photo)
            self.video_label.image = photo  # Keep a reference
            
        except Exception as e:
            logger.error(f"Error updating video display: {e}")
    
    def camera_loop(self):
        """Main camera capture loop."""
        while self.is_running:
            try:
                frame = self.capture_frame()
                if frame is not None:
                    self.current_frame = frame
                    
                    # Update video display
                    self.root.after(0, lambda f=frame: self.update_video_display(f))
                    
                    # Add to processing queue if not full
                    if not self.image_queue.full():
                        self.image_queue.put(frame.copy())
                
                time.sleep(0.1)  # ~10 FPS
                
            except Exception as e:
                logger.error(f"Camera loop error: {e}")
                time.sleep(1)
    
    def ai_processing_loop(self):
        """AI processing loop for automatic descriptions."""
        while self.is_running:
            try:
                if (self.auto_describe and 
                    time.time() - self.last_description_time > self.description_interval):
                    
                    if not self.image_queue.empty():
                        frame = self.image_queue.get()
                        image_data = self.prepare_image_for_ai(frame)
                        
                        if image_data:
                            self.update_status("Analyzing image...")
                            description = self.analyze_image_with_ai(image_data)
                            
                            # Log and speak
                            self.root.after(0, lambda: self.log_text(description, "AUTO: "))
                            
                            # Speak in separate thread to avoid blocking
                            threading.Thread(
                                target=self.speak_text, 
                                args=(description,), 
                                daemon=True
                            ).start()
                            
                            self.last_description_time = time.time()
                            self.update_status("Description complete")
                
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"AI processing loop error: {e}")
                time.sleep(1)
    
    def voice_interaction_loop(self):
        """Voice interaction loop."""
        while self.is_running:
            try:
                if self.is_listening:
                    speech_text = self.listen_for_speech()
                    
                    if speech_text:
                        self.root.after(0, lambda: self.log_text(speech_text, "YOU: "))
                        
                        # Process the speech as a question
                        if self.current_frame is not None:
                            image_data = self.prepare_image_for_ai(self.current_frame)
                            if image_data:
                                response = self.analyze_image_with_ai(image_data, speech_text)
                                self.root.after(0, lambda: self.log_text(response, "AI: "))
                                
                                # Speak response
                                threading.Thread(
                                    target=self.speak_text, 
                                    args=(response,), 
                                    daemon=True
                                ).start()
                    
                    # Auto-stop listening after one interaction
                    self.is_listening = False
                    self.root.after(0, self.update_voice_button)
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Voice interaction error: {e}")
                time.sleep(1)
    
    def toggle_assistant(self):
        """Start or stop the assistant."""
        if not self.is_running:
            self.start_assistant()
        else:
            self.stop_assistant()
    
    def start_assistant(self):
        """Start the assistant."""
        if not self.ai_model or not self.camera:
            messagebox.showerror("Error", "Cannot start - AI model or camera not available")
            return
        
        self.is_running = True
        self.start_button.config(text="Stop Assistant")
        self.update_status("Starting assistant...")
        
        # Start threads
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.ai_thread = threading.Thread(target=self.ai_processing_loop, daemon=True)
        self.voice_thread = threading.Thread(target=self.voice_interaction_loop, daemon=True)
        
        self.camera_thread.start()
        self.ai_thread.start()
        self.voice_thread.start()
        
        self.update_status("Assistant started")
        startup_msg = "AI Vision Assistant शुरू हो गया। आवाज़ से सवाल पूछने के लिए Space दबाएं।" if self.response_language == 'hi' else "AI Vision Assistant started. Press Space to ask questions via voice."
        self.log_text(startup_msg)
    
    def stop_assistant(self):
        """Stop the assistant."""
        self.is_running = False
        self.is_listening = False
        self.start_button.config(text="Start Assistant")
        self.update_status("Stopping assistant...")
        
        # Stop audio
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        self.update_status("Assistant stopped")
        stop_msg = "AI Vision Assistant बंद हो गया।" if self.response_language == 'hi' else "AI Vision Assistant stopped."
        self.log_text(stop_msg)
    
    def toggle_listening(self):
        """Toggle voice listening mode."""
        if not self.is_running:
            messagebox.showwarning("Warning", "Please start the assistant first")
            return
        
        self.is_listening = not self.is_listening
        self.update_voice_button()
        
        if self.is_listening:
            self.update_status("Voice listening activated")
        else:
            self.update_status("Voice listening deactivated")
    
    def update_voice_button(self):
        """Update voice button appearance."""
        if self.is_listening:
            self.voice_button.config(text="🔴 Listening... (Space)")
        else:
            self.voice_button.config(text="🎤 Listen (Space)")
    
    def toggle_auto_describe(self):
        """Toggle automatic description mode."""
        self.auto_describe = self.auto_var.get()
        status = "enabled" if self.auto_describe else "disabled"
        self.update_status(f"Auto-describe {status}")
    
    def update_interval(self):
        """Update the description interval."""
        try:
            new_interval = int(self.interval_var.get())
            if 5 <= new_interval <= 60:
                self.description_interval = new_interval
                self.update_status(f"Analysis interval set to {new_interval} seconds")
            else:
                self.interval_var.set(str(self.description_interval))
                self.update_status("Interval must be between 5-60 seconds")
        except ValueError:
            self.interval_var.set(str(self.description_interval))
            self.update_status("Invalid interval value")
    
    def update_voice_accent(self, event=None):
        """Update the voice accent."""
        self.voice_accent = self.voice_var.get()
        self.update_status(f"Voice accent set to {self.voice_accent.upper()}")
    
    def update_response_language(self, event=None):
        """Update the response language."""
        self.response_language = self.language_var.get()
        self.voice_language = self.response_language  # Update TTS language too
        
        language_names = {'en': 'English', 'hi': 'Hindi'}
        lang_name = language_names.get(self.response_language, 'English')
        self.update_status(f"Response language set to {lang_name}")
    
    def update_speaking_speed(self):
        """Update the speaking speed."""
        try:
            new_speed = float(self.speed_var.get())
            if 0.5 <= new_speed <= 2.0:
                self.speaking_speed = new_speed
                # Update pyttsx3 rate
                rate = int(150 * new_speed)  # Base rate 150 WPM
                self.tts_engine.setProperty('rate', rate)
                self.update_status(f"Speaking speed set to {new_speed}x")
            else:
                self.speed_var.set(str(self.speaking_speed))
                self.update_status("Speed must be between 0.5x-2.0x")
        except ValueError:
            self.speed_var.set(str(self.speaking_speed))
            self.update_status("Invalid speed value")
    
    def toggle_tts_quality(self):
        """Toggle between HD (Google Cloud) and standard TTS."""
        self.use_google_tts_api = self.tts_quality_var.get()
        quality = "HD (Google Cloud)" if self.use_google_tts_api else "Standard (gTTS)"
        self.update_status(f"Voice quality: {quality}")
    
    def ask_question(self):
        """Process typed question."""
        question = self.question_var.get().strip()
        if not question:
            return
        
        if not self.is_running:
            messagebox.showwarning("Warning", "Please start the assistant first")
            return
        
        if self.current_frame is None:
            messagebox.showwarning("Warning", "No camera frame available")
            return
        
        # Clear the entry
        self.question_var.set("")
        
        # Log the question
        self.log_text(question, "YOU: ")
        
        # Process in separate thread
        def process_question():
            try:
                self.update_status("Processing question...")
                image_data = self.prepare_image_for_ai(self.current_frame)
                if image_data:
                    response = self.analyze_image_with_ai(image_data, question)
                    self.root.after(0, lambda: self.log_text(response, "AI: "))
                    
                    # Speak response
                    self.speak_text(response)
                    
                self.update_status("Question processed")
            except Exception as e:
                logger.error(f"Error processing question: {e}")
                self.update_status("Error processing question")
        
        threading.Thread(target=process_question, daemon=True).start()
    
    def on_closing(self):
        """Handle application closing."""
        if self.is_running:
            self.stop_assistant()
        
        # Release camera
        if self.camera:
            self.camera.release()
        
        # Close pygame
        try:
            pygame.mixer.quit()
        except:
            pass
        
        self.root.destroy()
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main function to run the AI Vision Assistant."""
    # Check environment variables
    if not os.getenv('GEMINI_API_KEY'):
        print("ERROR: GEMINI_API_KEY environment variable not set!")
        print("Please set your Gemini API key:")
        print("export GEMINI_API_KEY='your_api_key_here'")
        return
    
    try:
        app = VisionAssistant()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
