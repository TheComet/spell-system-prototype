__author__ = 'thecomet'

from Updateable import Updateable
from DraggableCircle import DraggableCircle
import pygame


class Spell(Updateable):

    def __init__(self, name, position):
        self.spell_name = name
        self.__spell_circle = DraggableCircle((255, 255, 255), position, 20)

        font = pygame.font.SysFont('monospace', 12)
        font_size = font.size(name)
        self.__spell_label = font.render(name, 1, (255, 255, 255))
        self.__spell_label_offset = (-int(font_size[0] / 2), -font_size[1])

    def process_event(self, event):
        self.__spell_circle.process_event(event)

    def update(self, time_step):
        self.__spell_circle.update(time_step)

    def draw(self, surface):
        self.__spell_circle.draw(surface)
        surface.blit(self.__spell_label, self.__get_spell_label_position())

    def __get_spell_label_position(self):
        return (self.__spell_circle.position[0] + self.__spell_label_offset[0],
                self.__spell_circle.position[1] + self.__spell_label_offset[1] - self.__spell_circle.radius)
