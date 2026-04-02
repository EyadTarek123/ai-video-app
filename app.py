import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio
import tempfile
import os
from datetime import datetime
from typing import Optional

FREE_TRIALS = 5

def initialize_session_state():
    if 'tries_left' not in st.session_state:
        st.session_state.tries_left = FREE_TRIALS
    if 'last_generated' not in st.session_state:
        st.session_state.last_generated = None

class VideoGenerator:
    @staticmethod
    def create_frame(text: str, frame_num: int, total_frames: int, width: int = 640, height: int = 480) -> np.ndarray:
        bg_color = (50, 100, 150 + (frame_num % 50))
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        text_to_show = text[:50]
        bbox = draw.textbbox((0, 0), text_to_show, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        draw.text(position, text_to_show, fill=(255, 255, 255), font=font)
        return np.array(img)
    
    @staticmethod
    def generate_video(text: str, duration: int = 3, fps: int = 8, output_path: Optional[str] = None) -> str:
        try:
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                output_path = temp_file.name
                temp_file.close()
            
            total_frames = duration * fps
            frames = []
            
            for i in range(total_frames):
                frame = VideoGenerator.create_frame(text, i, total_frames)
                frames.append(frame)
            
            imageio.mimsave(output_path, frames, fps=fps, codec='libx264')
            return output_path
        except Exception as e:
            raise RuntimeError(f"فشل توليد الفيديو: {str(e)}")

def main():
    st.set_page_config(page_title="AI Video Generator Pro", page_icon="🎥", layout="centered")
    initialize_session_state()
    
    st.title("🎬 AI Video Generator Pro")
    st.markdown("---")
    
    remaining = st.session_state.tries_left
    if remaining > 0:
        st.info(f"🎬 المحاولات المتبقية: {remaining} من {FREE_TRIALS}")
    else:
        st.warning("⚠️ لقد انتهت محاولاتك المجانية.")
    
    user_text = st.text_area("📝 أدخل السكربت الخاص بك:", height=150)
    
    if st.button("🎥 توليد الفيديو", type="primary"):
        if not user_text.strip():
            st.error("❌ الرجاء إدخال النص أولاً.")
            return
        
        if st.session_state.tries_left > 0:
            try:
                video_path = VideoGenerator.generate_video(user_text, duration=3, fps=8)
                st.success("✅ تم توليد الفيديو بنجاح!")
                
                with open(video_path, 'rb') as f:
                    video_bytes = f.read()
                st.video(video_bytes)
                
                with open(video_path, "rb") as f:
                    st.download_button(
                        label="📥 تحميل الفيديو",
                        data=f,
                        file_name=f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                        mime="video/mp4"
                    )
                
                st.session_state.tries_left -= 1
                
                if os.path.exists(video_path):
                    os.unlink(video_path)
            except Exception as e:
                st.error(f"❌ حدث خطأ: {str(e)}")
        else:
            st.warning("⚠️ انتهت المحاولات المجانية.")

if __name__ == "__main__":
    main()
