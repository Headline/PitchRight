import pygame as pygame
from PIL import Image, ImageFilter

from pitchright.ui.song_select_menu import SongSelectMenu
from pitchright.ui.common import draw_button, draw_text


class MutiplayerMenu:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width/4
        self.surface = pygame.surface.Surface((self.width, self.game.height), pygame.SRCALPHA, 32)
        self.item_font = pygame.font.Font("res/OpenSans-Regular.ttf", 28)
        self.info_font = pygame.font.Font("res/OpenSans-Regular.ttf", 24)
        self.create_lobby_button = None
        self.join_lobby_button = None
        self.song_menu = SongSelectMenu(game)
        self.open = True
        self.song_select_menu_open = False
        self.angle = -1

    def close_menu(self):
        self.open = False

    def draw(self, mx, my):

        self.surface.fill((16, 16, 16))
        self.create_lobby_button = draw_button(self.surface, self.item_font, "Create lobby", self.width / 1.35,
                                               self.game.height / 10, mx, my, color=(54, 54, 54, 255),
                                               color_highlight=(75, 75, 75, 255))
        self.join_lobby_button = draw_button(self.surface, self.item_font, "Join lobby", self.width / 4,
                                               self.game.height / 10, mx, my, color=(54, 54, 54, 255),
                                               color_highlight=(75, 75, 75, 255))

        self.game.surface.blit(self.surface, (0, 0))


    def on_create_lobby(self):
        print("Create lobby")

    def on_click(self, mx, my):
        if self.create_lobby_button.collidepoint((mx, my)):
            self.on_create_lobby()

