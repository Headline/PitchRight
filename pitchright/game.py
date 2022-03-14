import os

import pygame as pygame
import pygame_gui as pygame_gui

from pitchright.audio.manager import AudioManager, AUDIO_PROCESSING_FINISHED_EVENT
from pitchright.entities import EntityManager
from pitchright.ui.map import Map
from pitchright.ui.menu import MainMenu

class PitchRight:
    def __init__(self, width, height):
        # Setup audio
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()

        # Window / UI settings
        self.loading = False
        self.width = width
        self.height = height
        pygame.display.set_caption('PitchRight')
        self.window = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, (height//12) * 44)) # 44 lines, 88 notes
        self.ui_manager = pygame_gui.UIManager((width, height))

        # Game loop
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Game managers
        self.audio = AudioManager(self)
        self.audio.set_input_stream() # grab audio I/O streams

        self.map = Map(self)
        self.entities = EntityManager(self)
        self.menu = MainMenu(self)

        # Networking
        self.socket = None

    def start(self):
        self.game_loop()

    def game_loop(self):
        while self.is_running:
            self.surface.fill(pygame.Color('#000000'))
            time_delta = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.menu.open:
                            self.is_running = False
                        else:
                            self.map.reset()
                            self.audio.reset()
                            self.entities.reset()
                            self.menu.open = True

                    if event.key == pygame.K_UP:
                        self.map.transposition += 1
                    if event.key == pygame.K_DOWN:
                        self.map.transposition -= 1

                if event.type == AUDIO_PROCESSING_FINISHED_EVENT:
                    if event.subprocess is None or event.subprocess.poll() is not None:
                        event.song.separating = False
                        if event.start:
                            self.audio.load_map(event.song)
                            self.audio.play_instrumental(event.song)
                            self.menu.close_menu()
                            pitch_mean = self.entities.get_pitch_mean()
                            self.map.set_to_pitch(pitch_mean)
                            continue
                    else:
                        event.song.separating = True
                        # requeue event until we can actually handle it
                        pygame.event.post(event)

                self.menu.handle_event(event)

                self.ui_manager.process_events(event)
            self.ui_manager.update(time_delta)

            if self.menu.open:
                mx, my = pygame.mouse.get_pos()
                self.menu.draw_menu(self.surface, mx, my)
            else:
                self.map.draw(False)

                pitch, confidence = self.audio.get_input_pitch()
                if pitch != 0.0 and confidence > .7:
                    self.entities.add_note(pitch)

                self.entities.update()

            self.window.blit(self.surface, (0, self.map.y_boundary_offset), (0, 0, 1920, self.surface.get_height()))
            self.ui_manager.draw_ui(self.window)
            pygame.display.update()

        pygame.quit()
