import streamlit as st
from gtts import gTTS
import tempfile
import os
import time

st.title("Text + Audio + Images → Simple Video 🎬 (Pure Python)")

# رفع الملفات
images = st.file_uploader("Upload Images (optional)", accept_multiple_files=True, type=["jpg","png","jpeg"])
audio_file = st.file_uploader("Upload Audio (optional)", type=["mp3","wav"])
script = st.text_area("Write your script here (optional)")

if st.button("Generate"):
    if not (images or audio_file or script):
        st.warning("Please provide at least an image, audio, or script!")
    else:
        temp_dir = tempfile.mkdtemp()

        # تحويل النص لصوت لو فيه script
        if script:
            tts_path = os.path.join(temp_dir, "tts_audio.mp3")
            tts = gTTS(text=script, lang='en')  # ممكن تغير 'en' لـ 'ar'
            tts.save(tts_path)
            st.audio(tts_path)

        # تشغيل الصوت المرفوع لو موجود
        if audio_file:
            audio_path = os.path.join(temp_dir, audio_file.name)
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())
            st.audio(audio_path)

        # عرض الصور كفيديو بسيط
        if images:
            st.subheader("Images Video Preview")
            for img in images:
                st.image(img, use_column_width=True)
                time.sleep(2)  # مدة عرض كل صورة بالثواني
