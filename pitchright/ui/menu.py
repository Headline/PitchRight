import pygame as pygame
from PIL import Image, ImageFilter

from pitchright.ui.song_select_menu import SongSelectMenu
from pitchright.ui.common import draw_button, draw_text
from pitchright.ui.multiplayer import MutiplayerMenu

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font("res/HallwayRegular-KxM7.ttf", 182)
        self.item_font = pygame.font.Font("res/OpenSans-Regular.ttf", 48)
        self.info_font = pygame.font.Font("res/OpenSans-Regular.ttf", 24)
        self.select_button = None
        self.multiplayer_button = None
        self.song_menu = SongSelectMenu(game)
        self.multiplayer_menu = MutiplayerMenu(game)
        self.open = True
        self.song_select_menu_open = False
        self.multiplayer_menu_open = False
        self.angle = -1

    def close_menu(self):
        self.open = False

    def draw_menu(self, screen, mx, my):
        self.game.map.draw(True)
        self.blur_background(screen)

        draw_text(self.info_font, screen, "Input Vocal Transposition: {:+} Octave".format(self.game.map.transposition),
                  self.game.width / 8 + 45, 20, (255, 255, 255))
        draw_text(self.info_font, screen, "Use Up & Down Arrow Key to Adjust", self.game.width / 8 + 45, 20 + 60,
                  (255, 255, 255))

        draw_text(self.title_font, screen, "PitchRight", self.game.width / 2, self.game.height / 3.5, (255, 255, 255))

        self.select_button = draw_button(screen, self.item_font, "Select Song", self.game.width / 2,
                                         self.game.height / 1.75, mx, my, color=(54, 54, 54, 255),
                                         color_highlight=(75, 75, 75, 255))
        self.multiplayer_button = draw_button(screen, self.item_font, "Multiplayer", self.game.width / 2,
                                         self.game.height / 1.25, mx, my, color=(54, 54, 54, 255),
                                         color_highlight=(75, 75, 75, 255))

        if self.multiplayer_menu_open:
            self.multiplayer_menu.draw(mx, my)
        elif self.song_select_menu_open:
            self.song_menu.draw(mx, my)

    def blur_background(self, screen):
        img = pygame.image.tostring(screen, "RGBA", False)
        blurred = Image.frombuffer("RGBA", (self.game.width, self.game.height), img) \
            .filter(ImageFilter.GaussianBlur(radius=3))

        surface = pygame.image.fromstring(blurred.tobytes(), blurred.size, "RGBA")

        screen.fill((255, 255, 255))
        screen.blit(surface, (0, 0))

    def on_song_select(self):
        self.song_select_menu_open = not self.song_select_menu_open

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if self.song_select_menu_open:
                    self.song_menu.on_click(mx, my)
                elif self.multiplayer_menu_open:
                    self.multiplayer_menu.on_click(mx, my)
                    return

                if self.select_button.collidepoint((mx, my)):
                    self.song_select_menu_open = not self.song_select_menu_open
                elif self.multiplayer_button.collidepoint((mx, my)):
                    self.multiplayer_menu_open = not self.multiplayer_menu_open
