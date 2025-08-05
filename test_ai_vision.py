#!/usr/bin/env python3
"""
AI Vision Test with Sample Image
Tests AI functionality without needing camera access.
"""

import base64
import io
import os
from PIL import Image, ImageDraw
import google.generativeai as genai
import numpy as np

def create_test_image():
    """Create a simple test image to analyze."""
    print("🎨 Creating test image...")
    
    # Create a simple test image
    img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw some simple objects
    draw.rectangle([50, 50, 150, 100], fill='red', outline='black')
    draw.ellipse([200, 80, 300, 180], fill='yellow', outline='black')
    draw.rectangle([100, 200, 300, 250], fill='green', outline='black')
    
    # Add some text
    draw.text((20, 20), "Test Scene", fill='black')
    
    print("✅ Test image created")
    return img

def prepare_image_for_ai(pil_image):
    """Convert PIL image to base64 for AI processing."""
    print("🔄 Preparing image for AI...")
    
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
- Objects and shapes present
- Colors and their arrangement
- Any text or symbols
- The overall composition
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

def save_image(pil_image, filename="test_image.jpg"):
    """Save the test image for reference."""
    pil_image.save(filename)
    print(f"💾 Image saved as {filename}")

def main():
    """Main function for the AI test."""
    print("🔍 AI Vision Test (No Camera Required)")
    print("=" * 40)
    
    # Check API key
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ Please set GEMINI_API_KEY environment variable")
        print("Example: export GEMINI_API_KEY='your_api_key_here'")
        return
    
    # Create test image
    test_image = create_test_image()
    
    # Save image for reference
    save_image(test_image)
    
    # Prepare for AI
    image_data = prepare_image_for_ai(test_image)
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
    
    print(f"\n✅ Test completed successfully!")
    print(f"📁 Check 'test_image.jpg' to see what the AI analyzed")
    print("\n🎉 Your AI Vision system is working perfectly!")
    print("📸 To use with camera, grant permissions in System Preferences")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
