__author__ = 'thecomet'


import pygame
from Updateable import Updateable


class SpellLabel(Updateable):

    def __init__(self, spell, text):
        self.__spell = spell
        self.__text = None
        self.__label = None
        self.__label_offset = None
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        font = pygame.font.SysFont('monospace', 12)
        font_size = font.size(text)
        self.__label = font.render(text, 1, (255, 255, 255))
        self.__label_offset = (-int(font_size[0] / 2), -font_size[1])

    def draw(self, surface):
        surface.blit(self.__label, self.__get_label_position())

    def __get_label_position(self):
        return (self.__spell.circle.position[0] + self.__label_offset[0],
                self.__spell.circle.position[1] + self.__label_offset[1] - self.__spell.circle.radius)
