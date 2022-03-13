import os
import threading

import ffmpeg
import youtube_dl

from pitchright.audio.song import Song


class YoutubeDownloader:
    def __init__(self, url, audio_manager, menu):
        self.url = url
        self.audio_manager = audio_manager
        self.menu = menu
        self.thread = None
        self.lock = threading.Lock()
        self.download_percentage = 0
        self.file_name = 'Unknown Download'

    @staticmethod
    def convert_mp3(filename, out_name):
        out_stream = ffmpeg.input(filename)
        out_stream = ffmpeg.output(out_stream, out_name, acodec='libmp3lame', audio_bitrate='320k')
        out_stream = ffmpeg.overwrite_output(out_stream)
        ffmpeg.run(out_stream)

    def get_progress(self):
        return self.download_percentage

    def download_hook(self, d):
        self.file_name = os.path.splitext(d['filename'])[0]
        if d['status'] == 'finished':
            file_name_ext = d['filename']

            mp3_name = self.file_name + '.mp3'
            YoutubeDownloader.convert_mp3(file_name_ext, mp3_name)
            os.remove(file_name_ext)
            song = Song(mp3_name)
            song.separating = True
            self.audio_manager.library.add(song)
            self.audio_manager.separate_tracks(song, False)
            self.menu.downloads = list(filter(lambda download: download.download_percentage < 1, self.menu.downloads))
            self.audio_manager.library.refresh()
        else:
            self.lock.acquire()
            self.download_percentage = d['downloaded_bytes']/d['total_bytes']
            self.lock.release()


    def _download(self):
        opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'prefer_ffmpeg': True,
            'noplaylist': True,
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [self.download_hook],

        }
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([self.url])

    def download(self):
        self.thread = threading.Thread(target=self._download, args=())
        self.thread.start()
