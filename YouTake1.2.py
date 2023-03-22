from pytube import YouTube
from pytube.cli import on_progress
import tkinter as tk
from moviepy.editor import *

def print_selection():
    print(vid_qual.get())
    print(vid_form.get())
    print(aud_qual.get())
    print(entry.get())
    # Retrieve the value entered by the user in the entry widget
    url = entry.get()
    yt = YouTube(url, on_progress_callback=on_progress)
    # Get the stream with the resolution required by the user
    stream = yt.streams.filter(res=vid_qual.get(), file_extension="mp4").first()
    # Download the video to the current working directory
    stream.download()
    print("Video downloaded successfully !")
    if vid_form.get() != "mp4":
        clip = VideoFileClip(stream)
        output_file = f"{stream.split('.')[0]}.{vid_form.get()}"
        clip.write_videofile(output_file)

video_quality = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
video_format = ["mkv", "mp4", "wmv", "avi"]
audio_format = ["mp3", "wav", "flac", "ac3", "wma"]

root = tk.Tk()
root.title("YouTake, YouTube videos and musics downloader")
# Input frame for video link (url)
input_frame = tk.LabelFrame(root, text="Video link (URL)", width=300, height=50)
entry = tk.Entry(input_frame,width=75)
entry.pack()
input_frame.pack(padx=10, pady=10)

vid_qual = tk.StringVar(value="Video quality")
vid_form = tk.StringVar(value="Video format")
aud_qual = tk.StringVar(value="Audio format")

menu_video_quality = tk.OptionMenu(root, vid_qual, *video_quality).pack(padx=10, pady=10)
menu_video_format = tk.OptionMenu(root, vid_form, *video_format).pack()
menu_audio_format = tk.OptionMenu(root, aud_qual, *audio_format).pack(padx=10, pady=10)

button = tk.Button(root, text="Download", command=print_selection, bg="green", bd=5).pack(side="bottom", padx=10, pady=10)

root.mainloop()
