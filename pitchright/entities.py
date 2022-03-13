import pygame as pygame
import numpy


class Entity:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color


class EntityManager:
    def __init__(self, game):
        self.entities = []
        self.game = game
        self.generated_notes = []
        self.onset_cache = set()

    def reset(self):
        self.entities = []
        self.generated_notes = []
        self.onset_cache = []

    def add_onset(self, tick):
        if tick not in self.onset_cache:
            print("Adding offset : " + str(tick))
            new_rect = pygame.Rect((self.game.width/2) + tick + 5, 0, 2, self.game.height)
            self.entities.append(Entity(new_rect, (255, 255, 255)))
            self.onset_cache.add(tick)

    def add_note(self, pitch):
        y = self.game.map.pitch_to_y(pitch, True)
        new_rect = pygame.Rect(self.game.width/2, y-5, 5, self.game.map.dy/2)
        self.entities.append(Entity(new_rect, (255, 255, 255)))

    def add_note_ticks(self, pitch, ticks_until_note):
        y = self.game.map.pitch_to_y(pitch, False)
        self.generated_notes.append([y, (self.game.width/2) + ticks_until_note+5])

    def get_pitch_mean(self):
        return numpy.array(self.generated_notes).mean(axis=0)[0]

    def generate_vocal_boxes(self):
        notes = numpy.array(self.generated_notes)
        mean = notes.mean(axis=0)[0]
        std_deviation = notes.std(axis=0)[0]
        cutoff = std_deviation
        for entry in notes:
            if entry[0] > mean+cutoff or entry[0] < mean-cutoff:
                continue
            new_rect = pygame.Rect(entry[1], entry[0], 5, self.game.map.dy/2)
            self.entities.append(Entity(new_rect, (100, 100, 255)))

    def update(self):
        # clean old entities
        self.entities = list(filter(lambda ent: ent.rect.x > 0, self.entities))

        for entity in self.entities:
            entity.rect.move_ip(-1, 0)
            if entity.rect.x < self.game.width: # only draw visible
                pygame.draw.rect(self.game.surface, entity.color, entity.rect)
