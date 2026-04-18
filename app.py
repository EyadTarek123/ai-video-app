import streamlit as st
from gtts import gTTS
import tempfile
import os
from PIL import Image

st.title("🎬 AI Video Generator Pro")

# Inputs
images = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg","png","jpeg"])
audio_file = st.file_uploader("Upload Audio (optional)", type=["mp3","wav"])
script = st.text_area("Write Script")
gesture_prompt = st.text_area("🤖 Hand Gesture Prompt (for AI animation)")

duration = st.slider("Video Duration (sec)", 5, 180, 30)

if st.button("Generate"):
    temp_dir = tempfile.mkdtemp()

    # 🔊 Audio (script → voice)
    audio_path = None
    if script:
        audio_path = os.path.join(temp_dir, "voice.mp3")
        tts = gTTS(script, lang="ar")
        tts.save(audio_path)
        st.audio(audio_path)

    # 🎧 Uploaded audio
    if audio_file:
        uploaded_audio = os.path.join(temp_dir, audio_file.name)
        with open(uploaded_audio, "wb") as f:
            f.write(audio_file.read())
        st.audio(uploaded_audio)

    # 🖼️ "Animated-style preview"
    if images:
        st.subheader("🎞️ Video Preview (Simulated Animation)")

        img_duration = max(1, duration // len(images))

        for i, img in enumerate(images):
            st.image(img, use_column_width=True)

            # 👇 fake animation effect (important fix)
            st.markdown(f"🎬 Frame {i+1}/{len(images)}")
            st.markdown(f"⏱ Duration: {img_duration}s")

    # 🤖 Gesture Prompt
    if gesture_prompt:
        st.subheader("🖐 AI Gesture Prompt")
        st.info(gesture_prompt)

    st.success("✅ Ready (Preview Mode)")
