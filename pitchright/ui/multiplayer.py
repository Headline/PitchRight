import tkinter.simpledialog
import pygame_textinput
import pygame as pygame
import socket

import pygame_gui
from PIL import Image, ImageFilter
from tkinter import *

from pygame_textinput import TextInputManager

from pitchright.server.packet import PacketFactory, Packet
from pitchright.ui.song_select_menu import SongSelectMenu
from pitchright.ui.common import draw_button, draw_text, InputBox


class MutiplayerMenu:
    def __init__(self, game):
        self.game = game
        self.width = self.game.width/4
        self.surface = pygame.surface.Surface((self.width, self.game.height), pygame.SRCALPHA, 32)
        self.item_font = pygame.font.Font("res/OpenSans-Regular.ttf", 22)
        self.info_font = pygame.font.Font("res/OpenSans-Regular.ttf", 24)
        self.create_lobby_button = None
        self.join_lobby_button = None
        self.song_menu = SongSelectMenu(game)
        self.open = True
        self.song_select_menu_open = False
        self.angle = -1
        self.text_box = InputBox(20, self.game.height / 6, self.width, 90, "code")

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

        pygame.draw.rect(self.surface, (225, 225, 225, 255), pygame.Rect(20, self.game.height/6, self.width, 90))
        self.text_box.update()
        self.text_box.draw(self.surface)
        self.game.surface.blit(self.surface, (0, 0))


    def on_create_lobby(self):
        self.game.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.game.socket.bind(('0.0.0.0', 50001))
        self.game.socket.sendto(PacketFactory.create_lobby(), ('127.0.0.1', 2082))
        data = self.game.socket.recv(512)
        p = Packet(data, None)
        print("Create lobby code: " + str(p.get_lobby_code()))

    def on_click(self, mx, my):
        if self.create_lobby_button.collidepoint((mx, my)):
            self.on_create_lobby()
        elif self.join_lobby_button.collidepoint((mx, my)):
            self.on_join_lobby()

    def on_join_lobby(self):
        self.game.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.game.socket.bind(('0.0.0.0', 50001))
        self.game.socket.sendto(PacketFactory.create_join_packet(code), ('127.0.0.1', 2082))
        data = self.game.socket.recv(512)
        p = Packet(data, None)
        print("Joined lobby code: " + str(p.get_lobby_code()))

    def handle_event(self, event):
        self.text_box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                self.on_click(mx, my)
