import streamlit as st
import os
import tempfile
import subprocess
from gtts import gTTS  # لتحويل النص لصوت

st.title("Text-to-Video Generator 🎬")

# رفع الصور (اختياري)
images = st.file_uploader("Upload Images (optional)", accept_multiple_files=True, type=["jpg","png","jpeg"])

# إدخال النص
script = st.text_area("Write your script here:")

if st.button("Generate Video"):
    if script or images:
        temp_dir = tempfile.mkdtemp()

        # تحويل النص لصوت
        audio_path = os.path.join(temp_dir, "audio.mp3")
        tts = gTTS(text=script, lang='en')  # ممكن تغير 'en' لـ 'ar' للعربي
        tts.save(audio_path)

        # حفظ الصور
        image_paths = []
        if images:
            for i, img in enumerate(images):
                ext = os.path.splitext(img.name)[1]
                path = os.path.join(temp_dir, f"{i}{ext}")
                with open(path, "wb") as f:
                    f.write(img.read())
                image_paths.append(path)
        else:
            st.warning("No images uploaded, video will only play audio.")

        # إنشاء ملف قائمة الصور لـ FFmpeg
        list_file = os.path.join(temp_dir, "images.txt")
        with open(list_file, "w") as f:
            for path in image_paths:
                f.write(f"file '{path}'\n")
                f.write("duration 2\n")
            if image_paths:
                f.write(f"file '{image_paths[-1]}'\n")

        output = os.path.join(temp_dir, "output.mp4")

        # تشغيل FFmpeg
        try:
            if image_paths:
                subprocess.run(
                    ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file, "-i", audio_path,
                     "-c:v", "libx264", "-c:a", "aac", "-shortest", output],
                    check=True
                )
                st.success("Video generated successfully! 🎉")
                st.video(output)
            else:
                st.audio(audio_path)  # لو مفيش صور، يعرض بس الصوت
        except subprocess.CalledProcessError:
            st.error("Error generating video. Make sure FFmpeg is installed and in PATH.")
    else:
        st.warning("Please enter a script or upload images first!")
