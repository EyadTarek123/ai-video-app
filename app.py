import streamlit as st
from gtts import gTTS
import tempfile
import os
from pydub import AudioSegment

st.title("🎬 AI Video Generator (Text + Images + Voice)")

# Inputs
images = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg","png","jpeg"])
script = st.text_area("Write your script here")
duration = st.slider("Video Duration (seconds)", 5, 180, 30)  # max 3 minutes

if st.button("Generate Video"):
    if not script:
        st.warning("Please enter a script!")
    else:
        temp_dir = tempfile.mkdtemp()

        # 🔊 Create Voice from script
        tts_path = os.path.join(temp_dir, "voice.mp3")
        tts = gTTS(text=script, lang='ar')  # غيرها لـ 'en' لو عايز
        tts.save(tts_path)

        st.success("Voice generated!")
        st.audio(tts_path)

        # 🎧 Get audio duration
        audio = AudioSegment.from_file(tts_path)
        audio_duration = len(audio) / 1000  # seconds

        # 🖼️ Handle images timing
        if images:
            st.subheader("🎞️ Video Preview")

            # عدد الصور
            num_images = len(images)

            # مدة عرض كل صورة
            img_duration = max(1, duration // num_images)

            for img in images:
                st.image(img, use_column_width=True)
                st.write(f"⏱ Showing for {img_duration} sec")

        # 📊 Info
        st.info(f"""
        🎤 Audio Duration: {round(audio_duration, 2)} sec  
        🎬 Selected Video Duration: {duration} sec  
        🖼️ Images: {len(images) if images else 0}
        """)

        st.success("✅ Done! (Preview mode)")
