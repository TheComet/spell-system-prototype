__author__ = 'thecomet'


import pygame
import math
from Updateable import Updateable


class SpellLabel(Updateable):

    def __init__(self, spell, text, offset=(0, 0)):
        self.__spell = spell
        self.__original_spell_radius = spell.radius
        self.__text = None
        self.__label = None
        self.__label_offset_local = None
        self.__label_offset = offset
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        font = pygame.font.SysFont('monospace', 12)
        font_size = font.size(text)
        self.__label = font.render(text, 1, (255, 255, 255))
        self.__label_offset_local = (-int(font_size[0] / 2), -font_size[1] / 2)

    def draw(self, surface):
        surface.blit(self.__label, self.__get_label_position())

    def __get_label_position(self):
        expansion = self.__spell.radius / self.__original_spell_radius
        x = self.__label_offset_local[0] + self.__label_offset[0] * expansion
        y = self.__label_offset_local[1] + self.__label_offset[1] * expansion
        return x + self.__spell.position[0], y + self.__spell.position[1]
