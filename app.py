import streamlit as st
import os
import tempfile

st.title("Simple Video Generator 🎬")

images = st.file_uploader("Upload Images", accept_multiple_files=True)
audio = st.file_uploader("Upload Audio")

if st.button("Generate"):
    if images and audio:
        temp_dir = tempfile.mkdtemp()

        image_paths = []
        for i, img in enumerate(images):
            path = os.path.join(temp_dir, f"{i}.jpg")
            with open(path, "wb") as f:
                f.write(img.read())
            image_paths.append(path)

        audio_path = os.path.join(temp_dir, "audio.mp3")
        with open(audio_path, "wb") as f:
            f.write(audio.read())

        # create file list
        list_file = os.path.join(temp_dir, "images.txt")
        with open(list_file, "w") as f:
            for path in image_paths:
                f.write(f"file '{path}'\n")
                f.write("duration 2\n")

        output = os.path.join(temp_dir, "output.mp4")

        os.system(f"ffmpeg -f concat -safe 0 -i {list_file} -i {audio_path} -c:v libx264 -c:a aac -shortest {output}")

        st.video(output)
