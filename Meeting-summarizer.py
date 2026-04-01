from moviepy import VideoFileClip
from groq import Groq
import base64

# 1. Setup Groq
client = Groq(api_key="")

# 2. Grab a screenshot from the video
print("🎬 Grabbing a screenshot at the 2-second mark...")
video = VideoFileClip("my_video.mp4")
video.save_frame("screenshot.jpg", t=2) # Takes a picture at 2 seconds

# 3. Convert the picture into code (Base64) so the AI can read it
print("⚙️ Converting image for the AI...")
with open("screenshot.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# 4. Send to Groq's Vision Brain
completion = client.chat.completions.create(
    model="llama-3.2-90b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "You are a site inspector. Describe exactly what you see happening in this construction site image."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ]
)

print("\n✨ AI VISION REPORT:")
print("-" * 40)
print(completion.choices[0].message.content)
print("-" * 40)
