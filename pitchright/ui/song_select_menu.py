import multiprocessing

import pygame as pygame
import tkinter as tk
from tkinter import filedialog

import win32clipboard
from urllib.parse import urlparse

from pitchright.ui.common import draw_button

from pitchright.audio.youtube_downloader import YoutubeDownloader
from pitchright.audio.manager import AudioManager


class SongSelectMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("res/OpenSans-Regular.ttf", 14)
        self.width = self.game.width / 4
        self.height = self.game.height
        self.screen = self.game.surface
        self.x_offset = self.game.width - self.width
        self.add_song = None
        self.import_youtube = None
        self.info_panel_height = self.height / 10
        self.surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.downloads = []
        self.loading_image = pygame.transform.smoothscale(pygame.image.load("res/loading.jpg"), (50, 50))


    def on_click(self, mx, my):
        if self.add_song.collidepoint((mx - self.x_offset, my)):
            self.on_add_song()
        elif self.import_youtube.collidepoint((mx - self.x_offset, my)):
            self.import_from_clipboard()
        else:
            for song in self.game.audio.library.songs:
                if song.click_box.collidepoint((mx - self.x_offset, my)):
                    self.game.audio.separate_tracks(song, True)

    def import_from_clipboard(self):
        win32clipboard.OpenClipboard()
        youtube_link = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        parse = urlparse(youtube_link)
        url = str(parse.hostname).replace('www.', '')
        if url != 'youtube.com' and url != 'youtu.be':
            print("Invalid hostname: '" + url + "'")
            # TODO: error message
            return

        downloader = YoutubeDownloader(youtube_link, self.game.audio, self)
        downloader.download()
        self.downloads.append(downloader)

    @staticmethod
    def on_add_song():
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
        if len(path) != 0:
            AudioManager.separate_tracks(path, False)

    def draw(self, mx, my):
        pygame.draw.rect(self.surface, (0, 0, 0, 155), (0, 0, self.width, self.height))

        self.draw_info_panel(mx, my)
        self.draw_song_panel(mx, my)
        self.screen.blit(self.surface, (self.x_offset, 0))

    def draw_song_panel(self, mx, my):
        pygame.draw.rect(self.surface, (25, 25, 25, 255),
                         (0, self.info_panel_height, self.width, self.game.height - self.info_panel_height))

        current_y = self.info_panel_height

        for song in self.game.audio.library.songs:
            song.click_box = self.draw_song(song, mx, my, current_y)
            current_y += 75

        for download in self.downloads:
            self.draw_download(download.file_name, mx, my, current_y, download.get_progress())
            current_y += 75


    def draw_download(self, title, mx, my, y_offset, download_progress):
        box_height = 50
        background = pygame.Rect(0, y_offset, self.width, box_height)
        color = (45, 45, 45, 255)
        if background.collidepoint(mx - self.x_offset, my):
            color = (75, 75, 75, 255)
        pygame.draw.rect(self.surface, color, background)
        loading_bar = pygame.Rect(0, y_offset + box_height-3, download_progress * self.width, 3)
        pygame.draw.rect(self.surface, (64,224,208), loading_bar)
        text_obj = self.font.render(title, True, (255, 255, 255))

        self.surface.blit(text_obj, (25, y_offset + (box_height // 2)))
        return background

    def draw_song(self, song, mx, my, y_offset):
        box_height = 50
        background = pygame.Rect(0, y_offset, self.width, box_height)
        color = (45, 45, 45, 255)
        if background.collidepoint(mx - self.x_offset, my):
            color = (75, 75, 75, 255)
        pygame.draw.rect(self.surface, color, background)
        textobj = self.font.render(song.info.title, True, (255, 255, 255))
        self.surface.blit(textobj, (25, y_offset + (box_height // 2)))
        if song.separating:
            self.draw_loading(song, y_offset)
        return background

    def draw_loading(self, song, y_offset):
        orig_rect = self.loading_image.get_rect()
        rot_image = pygame.transform.rotate(self.loading_image, song.angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()

        self.surface.blit(rot_image, (52, y_offset+25))

    def draw_info_panel(self, mx, my):
        pygame.draw.rect(self.surface, (25, 25, 25, 255), (0, 0, self.width, self.info_panel_height))
        self.add_song = draw_button(self.surface, self.font, "Add Song", self.width / 6, self.info_panel_height / 2, mx,
                                    my, self.x_offset, (54, 54, 54, 255), (75, 75, 75, 255))
        self.import_youtube = draw_button(self.surface, self.font, "Import YouTube Video From Clipboard",
                                          self.width / 1.5, self.info_panel_height / 2, mx, my, self.x_offset,
                                          (54, 54, 54, 255), (75, 75, 75, 255))
