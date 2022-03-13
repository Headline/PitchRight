import pyaudio
import os
import numpy
import aubio
import pygame.event as pygame_event
import pygame.mixer as pygame_mixer
import subprocess

from pitchright.audio.song import SongLibrary

pDetection = aubio.pitch("yinfast", 2048,
                         2048 // 2, 44100)
# Set unit.
pDetection.set_unit("Hz")
pDetection.set_silence(-30)
AUDIO_PROCESSING_FINISHED_EVENT = pygame_event.custom_type()


class AudioManager:
    def __init__(self, game):
        self.game = game
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        self.library = SongLibrary()
        pygame_mixer.init()

    @staticmethod
    def reset():
        pygame_mixer.quit()
        pygame_mixer.init()

    @staticmethod
    def separate_tracks(song, start):
        if os.path.exists(os.path.join('songs', song.info.hash, 'vocals.wav')):
            pygame_event.post(pygame_event.Event(AUDIO_PROCESSING_FINISHED_EVENT, subprocess=None, song=song, start=start))
        else:
            p = subprocess.Popen(['spleeter_run.exe', song.original_path, song.info.hash])
            pygame_event.post(pygame_event.Event(AUDIO_PROCESSING_FINISHED_EVENT, subprocess=p, song=song, start=start))

    @staticmethod
    def load_vocal_map_buffer(arr, entity_manager):
        d = aubio.pitch("schmitt", 2048, 2048//2, 44100)
        # Set unit.
        d.set_unit("Hz")
        d.set_silence(-30)
        offset = 10
        total_frames = 0
        tick = 0
        arr = arr.sum(axis=1) / 2
        for idx in range(0, len(arr), 1024):
            sl = arr[idx:idx + 1024]
            if len(sl) < 1024:
                break

            pitch = d(sl)[0]
            tick += 1
            if pitch != 0.0 and d.get_confidence() > .85:
                entity_manager.add_note_ticks(pitch, tick+offset)

        entity_manager.generate_vocal_boxes()

    @staticmethod
    def get_tempo_data(path, onsets):
        src = aubio.source(path, 44100, 2048//2, channels=2)
        t = aubio.tempo("default", 2048, 2048//2, 44100)
        t.set_threshold(.1)
        t.set_silence(-30)

        total_frames = 0
        tick = 0
        while True:
            samples, read = src()
            total_frames += read
            if read < 1024:
                break

            if t(samples):
                onsets.append(tick)
            tick += 1
        src.close()


    def load_map(self, song):
        AudioManager.load_vocal_map(song.vocals_path, self.game.entities)

    @staticmethod
    def load_vocal_map(path, entity_manager):
        src = aubio.source(path, 44100, 2048//2, channels=1)

        p = aubio.pitch("yinfast", 2048, 2048//2, 44100)
        # Set unit.
        p.set_unit("Hz")
        p.set_silence(-30)

        total_frames = 0
        tick = 0
        while True:
            samples, read = src()
            total_frames += read
            if read < 1024:
                break

            pitch = p(samples)[0]
            tick += 1
            if pitch != 0.0 and p.get_confidence() > .85:
                entity_manager.add_note_ticks(pitch, tick + 10)
        entity_manager.generate_vocal_boxes()
        src.close()

    def get_devices(self):
        audio_device_count = self.pyaudio.get_device_count()
        output = []
        for x in range(0, audio_device_count):
            device = self.pyaudio.get_device_info_by_index(x)
            output.append(device['name'])

        return output

    def set_input_stream(self):
        self.stream = self.pyaudio.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True,
                                        frames_per_buffer=1024)

    def get_pitch(self, data, detection):
        return detection(data)[0]

    def get_input_pitch(self, detection=pDetection):
        data = self.stream.read(1024)
        samples = numpy.frombuffer(data, dtype=aubio.float_type)
        pitch = detection(samples)[0]
        return pitch, detection.get_confidence()

    @staticmethod
    def play_instrumental(song):
        pygame_mixer.music.load(song.instrumental_path)
        pygame_mixer.music.play()
        pygame_mixer.music.set_volume(.7)

