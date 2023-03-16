from pytube import YouTube
from pytube.cli import on_progress
import tkinter as tk
from moviepy.editor import *

def print_selection():
    print(var1.get())
    print(var2.get())
    print(var3.get())
    print(entry.get())
    # Retrieve the value entered by the user in the entry widget
    url = entry.get()
    yt = YouTube(url, on_progress_callback=on_progress)
    # Get the stream with the resolution required by the user
    stream = yt.streams.filter(res=var1.get(), file_extension="mp4").first()
    # Download the video to the current working directory
    stream.download()
    print("Video downloaded successfully !")
    if var2.get() != "mp4":
        clip = VideoFileClip(stream)
        output_file = f"{stream.split('.')[0]}.{var2.get()}"
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

var1 = tk.StringVar(value="Video quality")
var2 = tk.StringVar(value="Video format")
var3 = tk.StringVar(value="Audio format")

menu_video_quality = tk.OptionMenu(root, var1, *video_quality).pack(padx=10, pady=10)
menu_video_format = tk.OptionMenu(root, var2, *video_format).pack()
menu_audio_format = tk.OptionMenu(root, var3, *audio_format).pack(padx=10, pady=10)

button = tk.Button(root, text="Download", command=print_selection, bg="green", bd=5).pack(side="bottom", padx=10, pady=10)

root.mainloop()
