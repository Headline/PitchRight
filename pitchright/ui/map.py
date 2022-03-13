import pygame as pygame
import math
from pitchright.ui.menu import draw_text


def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min


class Map:
    def __init__(self, game):
        self.game = game
        self.y_boundary_offset = 0
        self.info_font = pygame.font.Font("res/HallwayRegular-KxM7.ttf", 48)

        self.transposition = 0
        # average human vocal range is 2 octaves = 24 notes = 12 ledger lines
        self.dy = self.game.height // 12

    def reset(self):
        self.y_boundary_offset = 0

    def set_transposition(self, transposition):
        self.transposition = transposition

    def draw(self, blurred=False):
        if not blurred:
            draw_text(self.info_font, self.game.surface, "{:+}".format(self.transposition), 40, abs(self.y_boundary_offset)+40, (255, 255, 255))

        # vertical line
        pygame.draw.line(self.game.surface, (255,100,100), (self.game.width/2, 0), (self.game.width/2, self.game.surface.get_rect().height), 1)

        # Draw full range piano range (88//2)
        for line in range(0, 44):
            y = line * self.dy + self.dy/2
            pygame.draw.line(self.game.surface, (255,255,255), (0, y), (self.game.width, y), 2)

    """
        Scale incoming pitch to where the pitch should be relative to 88 key piano
    """
    def relative_pitch_to_y(self, relative_pitch):
        return (self.dy/2) * relative_pitch

    def pitch_to_y(self, pitch, user_pitch):
        # map boundries
        high = math.log10(4186) # highest supported note of C8
        low = math.log10(27.5) # lowest supported note of A0

        log_pitch = math.log10(pitch)
        scaled_y = scale_number(log_pitch, 0, self.game.surface.get_rect().height, high, low) # 88 key piano
        scaled_y -= (self.dy/2) * self.transposition * 12 # 12 notes

        if user_pitch:
            if abs(self.y_boundary_offset) + (.15 * self.game.height) > scaled_y:
                self.y_boundary_offset += 5
            if abs(self.y_boundary_offset) + (.85 * self.game.height) < scaled_y:
                self.y_boundary_offset -= 5

        return scaled_y

    def set_to_pitch(self, pitch_mean):
        y = self.pitch_to_y(pitch_mean, False)
        self.y_boundary_offset -= y + self.game.height
