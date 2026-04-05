import tkinter as tk
from tkinter import filedialog
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

images = []
audio_path = ""

def add_images():
    global images
    files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.png")])
    images = list(files)
    print("Images added:", images)

def add_audio():
    global audio_path
    file = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3")])
    audio_path = file
    print("Audio added:", audio_path)

def generate_video():
    if not images or not audio_path:
        print("Add images and audio first!")
        return

    audio = AudioFileClip(audio_path)
    duration_per_image = audio.duration / len(images)

    clips = []
    for img in images:
        clip = ImageClip(img).set_duration(duration_per_image)
        clip = clip.resize(lambda t: 1 + 0.02*t)  # zoom effect
        clips.append(clip)

    final = concatenate_videoclips(clips)
    final = final.set_audio(audio)

    final.write_videofile("output.mp4", fps=24)
    print("Video created!")

# GUI
root = tk.Tk()
root.title("AI Video Generator")

tk.Button(root, text="Add Images", command=add_images).pack(pady=5)
tk.Button(root, text="Add Audio", command=add_audio).pack(pady=5)
tk.Button(root, text="Generate Video", command=generate_video).pack(pady=10)

root.mainloop()
