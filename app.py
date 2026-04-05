import streamlit as st
from gtts import gTTS
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import tempfile
import os

st.title("Text + Audio + Images → Video Generator 🎬")

# رفع الملفات
images = st.file_uploader("Upload Images (optional)", accept_multiple_files=True, type=["jpg","png","jpeg"])
audio_file = st.file_uploader("Upload Audio (optional)", type=["mp3","wav"])
script = st.text_area("Write your script here (optional)")

if st.button("Generate Video"):
    if not (images or audio_file or script):
        st.warning("Please provide at least an image, audio, or script!")
    else:
        temp_dir = tempfile.mkdtemp()

        # إعداد الصوت النهائي
        audio_clips = []

        # إذا فيه سكربت، نحوله لصوت
        if script:
            tts_path = os.path.join(temp_dir, "tts_audio.mp3")
            tts = gTTS(text=script, lang='en')  # ممكن تغير 'en' لـ 'ar'
            tts.save(tts_path)
            audio_clips.append(AudioFileClip(tts_path))

        # إذا فيه صوت مرفوع
        if audio_file:
            audio_path = os.path.join(temp_dir, audio_file.name)
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())
            audio_clips.append(AudioFileClip(audio_path))

        # دمج كل المقاطع الصوتية في مقطع واحد
        if audio_clips:
            final_audio = CompositeAudioClip(audio_clips)
        else:
            final_audio = None

        # إنشاء الفيديو من الصور
        video_clips = []
        if images:
            for img in images:
                img_path = os.path.join(temp_dir, img.name)
                with open(img_path, "wb") as f:
                    f.write(img.read())
                clip = ImageClip(img_path).set_duration(2)  # كل صورة مدتها 2 ثانية
                video_clips.append(clip)

            final_clip = concatenate_videoclips(video_clips)
            if final_audio:
                final_clip = final_clip.set_audio(final_audio)
            output_path = os.path.join(temp_dir, "output.mp4")
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            st.success("Video generated successfully! 🎉")
            st.video(output_path)
        else:
            # لو مفيش صور، بس نعطي الصوت
            if final_audio:
                st.audio(final_audio)
            else:
                st.warning("No media to generate!")
