import streamlit as st
from gtts import gTTS
import tempfile
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

st.title("🎬 AI Video Generator (REAL MP4)")

images = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg","png","jpeg"])
script = st.text_area("Write Script")
audio_file = st.file_uploader("Upload Audio (optional)", type=["mp3","wav"])
duration = st.slider("Video Duration (sec)", 5, 180, 30)

if st.button("Generate Video"):
    if not images:
        st.warning("لازم ترفع صور")
    else:
        temp_dir = tempfile.mkdtemp()

        # 🔊 Create voice if script exists
        audio_path = None
        if script:
            audio_path = os.path.join(temp_dir, "voice.mp3")
            tts = gTTS(script, lang="ar")
            tts.save(audio_path)

        # 🖼️ Create video clips
        clips = []
        per_img = duration / len(images)

        for img in images:
            img_path = os.path.join(temp_dir, img.name)
            with open(img_path, "wb") as f:
                f.write(img.read())

            clip = ImageClip(img_path).set_duration(per_img)
            clips.append(clip)

        video = concatenate_videoclips(clips)

        # 🔊 Add audio
        if audio_path:
            audio = AudioFileClip(audio_path)
            video = video.set_audio(audio)

        output_path = os.path.join(temp_dir, "output.mp4")
        video.write_videofile(output_path, fps=24)

        st.success("✅ Video Created!")
        st.video(output_path)
