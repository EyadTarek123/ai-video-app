import streamlit as st
from gtts import gTTS
import tempfile
import os

st.title("🎬 Simple AI Video Generator")

images = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg","png","jpeg"])
script = st.text_area("Write your script")
duration = st.slider("مدة الفيديو (ثواني)", 5, 180, 30)

if st.button("Generate"):
    if not script:
        st.warning("اكتب script الأول")
    else:
        temp_dir = tempfile.mkdtemp()

        # إنشاء الصوت
        tts_path = os.path.join(temp_dir, "voice.mp3")
        tts = gTTS(text=script, lang='ar')
        tts.save(tts_path)

        st.audio(tts_path)

        # عرض الصور
        if images:
            st.subheader("Preview")
            img_duration = max(1, duration // len(images))

            for img in images:
                st.image(img, use_column_width=True)
                st.write(f"⏱ {img_duration} sec")
