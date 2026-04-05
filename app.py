import streamlit as st
import os
import tempfile
import subprocess  # أفضل من os.system

st.title("Simple Video Generator 🎬")

# رفع الملفات
images = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg","png","jpeg"])
audio = st.file_uploader("Upload Audio", type=["mp3","wav"])

if st.button("Generate"):
    if images and audio:
        temp_dir = tempfile.mkdtemp()

        # حفظ الصور مؤقتًا
        image_paths = []
        for i, img in enumerate(images):
            ext = os.path.splitext(img.name)[1]  # يخلي الامتداد الأصلي
            path = os.path.join(temp_dir, f"{i}{ext}")
            with open(path, "wb") as f:
                f.write(img.read())
            image_paths.append(path)

        # حفظ الصوت مؤقتًا
        audio_ext = os.path.splitext(audio.name)[1]
        audio_path = os.path.join(temp_dir, f"audio{audio_ext}")
        with open(audio_path, "wb") as f:
            f.write(audio.read())

        # إنشاء ملف قائمة الصور لـ FFmpeg
        list_file = os.path.join(temp_dir, "images.txt")
        with open(list_file, "w") as f:
            for path in image_paths:
                f.write(f"file '{path}'\n")
                f.write("duration 2\n")
            # إعادة كتابة الصورة الأخيرة لضمان طول الفيديو
            f.write(f"file '{image_paths[-1]}'\n")

        output = os.path.join(temp_dir, "output.mp4")

        # تشغيل FFmpeg بطريقة أكثر أمانًا
        try:
            subprocess.run(
                ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file, "-i", audio_path,
                 "-c:v", "libx264", "-c:a", "aac", "-shortest", output],
                check=True
            )
            st.success("Video generated successfully! 🎉")
            st.video(output)
        except subprocess.CalledProcessError:
            st.error("Error generating video. Make sure FFmpeg is installed and in PATH.")
    else:
        st.warning("Please upload both images and audio first!")
