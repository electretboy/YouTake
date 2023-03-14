
from pytube import YouTube
from pytube.cli import on_progress
# Enter the YouTube video URL
url = input("Enter the YouTube video link (URL): ")
yt = YouTube(url, on_progress_callback=on_progress)
# Get the first stream with the highest resolution
stream = yt.streams.get_highest_resolution()
# Download the video to the current working directory
stream.download()
print("Video downloaded successfully !")
input("Press the <ENTER> key to close...")