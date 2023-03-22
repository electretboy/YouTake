from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
from pytube.cli import on_progress


def print_selection(url, vid_qual, vid_format, aud_format):
    yt = YouTube(url, on_progress_callback=on_progress)
    # Get the stream with the resolution required by the user
    stream = yt.streams.filter(res=vid_qual, file_extension="mp4").first()
    # Download the video to the current working directory
    stream.download()
    print("Video downloaded successfully !")
    if vid_format != "mp4":
        clip = VideoFileClip(stream)
        output_file = f"{stream.split('.')[0]}.{vid_format}"
        clip.write_videofile(output_file)


# Enter the YouTube video URL
url = input("Enter the YouTube video link (URL): ")
print("2160p, 1440p, 1080p, 720p, 480p, 360p, 240p, 144p")
while True:
    vid_quality = input("Choose the quality from the list above :")
    if vid_quality in ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]:
        break
    else:
        print("Wrong quality : choose one from above")
print()

print("mkv, mp4, wmv, avi")
while True:
    vid_format = input("Choose the quality from the list above :")
    if vid_format in ["mkv", "mp4", "wmv", "avi"]:
        break
    else:
        print("Wrong format : choose one from above")
print()

print("mp3, wav, flac, ac3, wma")
while True:
    aud_format = input("Choose the format from the list above :")
    if aud_format in ["mp3", "wav", "flac", "ac3", "wma"]:
        break
    else:
        print("Wrong format : choose one from above")

# Download the video to the current working directory
print_selection(url, vid_quality, vid_format, aud_format)
input("Press the <ENTER> key to close...")
