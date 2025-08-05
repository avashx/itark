#!/usr/bin/env python3
"""
Simple AI Vision Example
A minimal example showing how to capture an image and get AI description.
Use this to test your setup before running the full application.
"""

import cv2
import base64
import io
import os
from PIL import Image
import google.generativeai as genai

def capture_image():
    """Capture a single image from the camera."""
    print("📷 Capturing image from camera...")
    
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("❌ Cannot access camera")
        return None
    
    # Capture frame
    ret, frame = camera.read()
    camera.release()
    
    if not ret:
        print("❌ Failed to capture image")
        return None
    
    print("✅ Image captured successfully")
    return frame

def prepare_image_for_ai(frame):
    """Convert image to base64 for AI processing."""
    print("🔄 Preparing image for AI...")
    
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(frame_rgb)
    
    # Resize if too large
    width, height = pil_image.size
    if width > 800:
        scale = 800 / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Convert to base64
    buffer = io.BytesIO()
    pil_image.save(buffer, format='JPEG', quality=85)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    print("✅ Image prepared for AI processing")
    return image_base64

def analyze_with_ai(image_data):
    """Analyze image using Gemini AI."""
    print("🤖 Analyzing image with AI...")
    
    try:
        # Initialize Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not set")
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prepare prompt
        prompt = """Describe what you see in this image in detail. Focus on:
- Objects and people present
- The environment and setting
- Colors, lighting, and atmosphere
- Spatial relationships
Keep the description conversational and helpful."""
        
        # Prepare image for Gemini
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_data
        }
        
        # Generate description
        response = model.generate_content([prompt, image_part])
        
        print("✅ AI analysis complete")
        return response.text
        
    except Exception as e:
        print(f"❌ AI analysis failed: {e}")
        return None

def save_image(frame, filename="captured_image.jpg"):
    """Save the captured image for reference."""
    cv2.imwrite(filename, frame)
    print(f"💾 Image saved as {filename}")

def main():
    """Main function for the simple example."""
    print("🔍 AI Vision Simple Example")
    print("=" * 30)
    
    # Check API key
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ Please set GEMINI_API_KEY environment variable")
        print("Example: export GEMINI_API_KEY='your_api_key_here'")
        return
    
    # Capture image
    frame = capture_image()
    if frame is None:
        return
    
    # Save image for reference
    save_image(frame)
    
    # Prepare for AI
    image_data = prepare_image_for_ai(frame)
    if image_data is None:
        return
    
    # Analyze with AI
    description = analyze_with_ai(image_data)
    if description is None:
        return
    
    # Display results
    print("\n" + "=" * 50)
    print("🎯 AI DESCRIPTION:")
    print("=" * 50)
    print(description)
    print("=" * 50)
    
    print(f"\n✅ Example completed successfully!")
    print(f"📁 Check 'captured_image.jpg' to see what the AI analyzed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
