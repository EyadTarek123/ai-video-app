import streamlit as st
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import tempfile

st.title("AI Video Generator 🎬")

images = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
audio_file = st.file_uploader("Upload Audio", type=["mp3"])

if st.button("Generate Video"):
    if images and audio_file:
        temp_audio = tempfile.NamedTemporaryFile(delete=False)
        temp_audio.write(audio_file.read())
        audio = AudioFileClip(temp_audio.name)

        duration_per_image = audio.duration / len(images)

        clips = []
        for img in images:
            temp_img = tempfile.NamedTemporaryFile(delete=False)
            temp_img.write(img.read())

            clip = ImageClip(temp_img.name).set_duration(duration_per_image)
            clip = clip.resize(lambda t: 1 + 0.02*t)
            clips.append(clip)

        final = concatenate_videoclips(clips)
        final = final.set_audio(audio)

        output_path = "output.mp4"
        final.write_videofile(output_path, fps=24)

        st.success("Video Generated!")
        st.video(output_path)
    else:
        st.error("Upload images and audio first!")
