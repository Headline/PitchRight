import os
import hashlib
import shutil
import json

from types import SimpleNamespace

def hash_file(filename):
    h = hashlib.sha1()
    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()


class SongInfo:
    def __init__(self, title, file_hash):
        self.hash = file_hash
        self.title = title
        self.version = '1'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Song:
    def __init__(self, path, create=True):
        if create:
            song_hash = Song.get_hash(path)

            sub_path = os.path.join('songs', song_hash)

            self.info = SongInfo(os.path.splitext(path)[0], song_hash)
            self.original_path = os.path.join(sub_path, 'original.mp3')

            if not os.path.exists('songs'):
                os.mkdir('songs')
            os.mkdir(sub_path)
            shutil.copy(path, self.original_path)

            with open(os.path.join(sub_path, 'song_info.json'), 'w') as outfile:
                json.dump(self.info.to_json(), outfile)

            self.vocals_path = os.path.join(sub_path, 'vocals.wav')
            self.instrumental_path = os.path.join(sub_path, 'accompaniment.wav')

        else:
            with open(os.path.join(path, 'song_info.json')) as infile:
                self.info = json.loads(json.load(infile), object_hook=lambda d: SimpleNamespace(**d))
            self.original_path = os.path.join(path, 'original.mp3')

            self.vocals_path = os.path.join(path, 'vocals.wav')
            self.instrumental_path = os.path.join(path, 'accompaniment.wav')

        # Download Properties
        self.download_progress = 0
        self.separating = False

        # UI Click Box
        self.angle = 0
        self.click_box = (0, 0, 0, 0)
        self.loading_angle = 0

    @staticmethod
    def load_song():
        def __str__(self):
            return self.info.title + " | " + self.vocals_path + " | " + self.instrumental_path

    @staticmethod
    def get_hash(path):
        return str(hash_file(path))



class SongLibrary:
    def __init__(self):
        self.songs = []
        self.refresh()

    def add(self, song):
        self.songs.append(song)

    def refresh(self):
        self.songs.clear()
        for root, dirs, files, in os.walk("songs/"):
            for song_dir in dirs:
                song = Song(os.path.join('songs', song_dir), False)
                self.songs.append(song)

