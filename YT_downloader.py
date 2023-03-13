
from pytube import YouTube
# Enter the YouTube video URL
url = input("Enter the YouTube video link: ")
yt = YouTube(url)
# Get the first stream with the highest resolution
stream = yt.streams.get_highest_resolution()
# Download the video to the current working directory
stream.download()
print("Video downloaded successfully !")