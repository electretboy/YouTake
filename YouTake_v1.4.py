import os
import threading
import urllib.request

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton, QFileDialog, QMenu, QAction
from moviepy.editor import VideoFileClip
from pytube import YouTube


class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Clear URL input field
        self.url_input.clear()

    def initUI(self):
        # Create GUI elements
        self.url_label = QLabel('YouTube URL:')
        self.url_input = QLineEdit()
        self.url_input.returnPressed.connect(self.update_thumbnail)
        self.format_label = QLabel('Output Format:')
        self.format_input = QComboBox()
        self.format_input.addItems(['mp4', 'mkv', 'wmv', 'avi', 'mp3', 'wav', 'flac', 'ac3', 'wma'])
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet('QProgressBar {background-color: #C0C0C0; border: 1px solid grey; border-radius: 5px; text-align: center;} QProgressBar::chunk {background-color: #FFA500; width: 10px;}')
        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.download_video)
        self.thumbnail_label = QLabel()

        # Create layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.url_label)
        hbox.addWidget(self.url_input)
        vbox.addLayout(hbox)
        vbox.addWidget(self.thumbnail_label)
        vbox.addWidget(self.format_label)
        vbox.addWidget(self.format_input)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.download_button)
        self.setLayout(vbox)

        # Set window properties
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 400, 300)
        self.show()

    def download_video(self):
        # Get user input
        url = self.url_input.text()
        format = self.format_input.currentText()

        # Get download destination from user
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "All Files (*);;Video Files (*.mp4 *.mkv *.avi);;Audio Files (*.mp3 *.wav *.flac *.ac3 *.wma)", options=options)
        if not file_name:
            return

        # Get directory path from file name
        directory = os.path.dirname(file_name)

        # Download video in separate thread
        t = threading.Thread(target=self.download_with_thread, args=(url, format, file_name, directory))
        t.start()

    def download_with_thread(self, url, format, file_name, directory):
        # Download video
        yt = YouTube(url, on_progress_callback=self.update_progress_bar)
        if format in ['mp4', 'mkv', 'wmv', 'avi']:
            stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            stream.download(output_path=directory, filename=stream.default_filename)

            # Download audio stream
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            audio_file_name = f'{stream.default_filename[:-4]}.{audio_stream.subtype}'
            audio_stream.download(output_path=directory, filename=audio_file_name)

            # Merge video and audio streams
            video_file_path = os.path.join(directory, stream.default_filename)
            audio_file_path = os.path.join(directory, audio_file_name)
            output_file_path = os.path.join(directory, f'{yt.title}.{format}')
            os.system(f'ffmpeg -i "{video_file_path}" -i "{audio_file_path}" -c:v copy -c:a copy "{output_file_path}"')

            # Delete temporary files
            os.remove(video_file_path)
            os.remove(audio_file_path)

        elif format in ['mp3', 'wav', 'flac', 'ac3', 'wma']:
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            stream.download(output_path=directory, filename=stream.default_filename)

            # Convert audio if necessary
            if format != 'mp3':
                clip = VideoFileClip(os.path.join(directory, stream.default_filename))
                output_file = os.path.join(directory, f'{yt.title}.{format}')
                clip.audio.write_audiofile(output_file)

        # Set progress bar to green
        self.progress_bar.setValue(100)
        self.progress_bar.setStyleSheet('QProgressBar {background-color: #C0C0C0; border: 1px solid grey; border-radius: 5px; text-align: center;} QProgressBar::chunk {background-color: #00FF00; width: 10px;}')

        # Clear URL input field
        self.url_input.clear()

    def update_progress_bar(self, stream, chunk, bytes_remaining):
        # Calculate download progress
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percent = bytes_downloaded / total_size * 100

        # Update progress bar
        self.progress_bar.setValue(int(percent))

        # Change progress bar color based on download progress
        if percent < 100:
            self.progress_bar.setStyleSheet('QProgressBar {background-color: #C0C0C0; border: 1px solid grey; border-radius: 5px; text-align: center;} QProgressBar::chunk {background-color: #FFA500; width: 10px;}')
        else:
            self.progress_bar.setStyleSheet('QProgressBar {background-color: #C0C0C0; border: 1px solid grey; border-radius: 5px; text-align: center;} QProgressBar::chunk {background-color: #00FF00; width: 10px;}')

    def update_thumbnail(self):
        # Get video ID from URL
        url = self.url_input.text()
        video_id = YouTube(url).video_id

        # Download thumbnail image
        thumbnail_url = f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
        data = urllib.request.urlopen(thumbnail_url).read()

        # Display thumbnail image
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.thumbnail_label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication([])
    downloader = Downloader()

    app.exec_()