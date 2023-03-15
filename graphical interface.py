
import tkinter as tk

def print_selection():
    print(var1.get())
    print(var2.get())
    print(var3.get())

root = tk.Tk()
# create an input frame for the video link


# Input frame for video link (url)
input_frame = tk.LabelFrame(root, text="Video link (URL)", width=300, height=50)
entry = tk.Entry(input_frame, width=75).pack()
input_frame.pack(padx=10, pady=10)

var1 = tk.StringVar(value="Video quality")
var2 = tk.StringVar(value="Format video")
var3 = tk.StringVar(value="Format audio")
video_quality = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
menu_video_quality = tk.OptionMenu(root, var1, *video_quality)
menu_video_quality.pack()
format_video = ["mkv", "mp4", "wmv", "avi"]
menu_format_video = tk.OptionMenu(root, var2, *format_video)
menu_format_video.pack()
format_audio = ["mp3", "wav", "flac", "ac3", "wma"]
menu_format_audio = tk.OptionMenu(root, var3, *format_audio)
menu_format_audio.pack()

button = tk.Button(root, text="Download", command=print_selection, bg="green", bd=5)
button.pack()

root.mainloop()