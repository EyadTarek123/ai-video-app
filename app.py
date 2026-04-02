import streamlit as st
import numpy as np
import cv2
import os
import tempfile
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

FREE_TRIALS = 5

class VideoGenerator:
    @staticmethod
    def generate_video(text: str, duration: int = 5, fps: int = 24, output_path: str = "output.mp4"):
        try:
            width, height = 640, 480
            total_frames = duration * fps
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # لون الخلفية (أزرق جميل)
            background_color = (100, 100, 200)  # BGR
            
            for i in range(total_frames):
                frame = np.ones((height, width, 3), dtype=np.uint8) * background_color
                
                # إضافة نص بالفريم (اختياري)
                if i < fps:  # أول ثانية فقط يظهر النص (عشان ما يبقاش ثابت طول الوقت)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text_short = text[:30]  # أول 30 حرف بس
                    cv2.putText(frame, text_short, (50, height//2), font, 0.7, (255, 255, 255), 2)
                
                out.write(frame)
            
            out.release()
            logging.info(f"Video saved at {output_path}")
            return output_path
        except Exception as e:
            logging.error(f"Error: {e}")
            raise RuntimeError(f"فشل توليد الفيديو: {str(e)}")

# باقي الكود كما هو من التعديل السابق (initialize_session_state، main، إلخ)
