import pygame as pygame
import socket
from PIL import Image, ImageFilter

from pitchright.server.packet import PacketFactory, Packet
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
        self.game.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.game.socket.bind(('0.0.0.0', 50001))
        self.game.socket.sendto(PacketFactory.create_lobby(), ('headlinedev.xyz', 2082))
        data = self.game.socket.recv(512)
        p = Packet(data, None)
        print("Create lobby code: " + str(p.get_lobby_code()))

    def on_click(self, mx, my):
        if self.create_lobby_button.collidepoint((mx, my)):
            self.on_create_lobby()

