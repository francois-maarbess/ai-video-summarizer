import streamlit as st
from groq import Groq
import os
import base64
from moviepy import VideoFileClip

st.set_page_config(page_title="AI Video Summarizer", page_icon="🎬")
st.title("🎬 Universal AI Video Summarizer")
st.markdown("Upload any video. AI will watch multiple moments to give you a full summary.")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")

uploaded_file = st.file_uploader("Upload video (.mp4)", type=["mp4"])

if uploaded_file and api_key:
    client = Groq(api_key=api_key)
    
    if st.button("Summarize Video 🚀"):
        with st.spinner("🎞️ Analyzing video sequence..."):
            try:
                # 1. Save and Load Video
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                video = VideoFileClip("temp_video.mp4")
                
                # 2. Extract 4 frames across the video duration
                duration = video.duration
                timestamps = [duration * 0.2, duration * 0.4, duration * 0.6, duration * 0.8]
                base64_frames = []
                
                cols = st.columns(4) # Show the frames we picked
                for i, t in enumerate(timestamps):
                    fname = f"frame_{i}.jpg"
                    video.save_frame(fname, t=t)
                    with open(fname, "rb") as f:
                        base64_frames.append(base64.b64encode(f.read()).decode('utf-8'))
                    cols[i].image(fname, caption=f"{int(t)}s")

                # 3. Build the Multimodal Prompt
                # We send a list containing the text instruction + all 4 images
                content_list = [{"type": "text", "text": "These are 4 chronological frames from a video. Please summarize what is happening across the entire video sequence."}]
                for b64 in base64_frames:
                    content_list.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                    })

                # 4. Call the Llama 4 Vision Model
                completion = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[{"role": "user", "content": content_list}]
                )
                
                st.success("Analysis Complete!")
                st.subheader("📝 Video Summary")
                st.write(completion.choices[0].message.content)

                # Cleanup
                video.close()
                for i in range(4): os.remove(f"frame_{i}.jpg")
                os.remove("temp_video.mp4")

            except Exception as e:
                st.error(f"Error: {e}")