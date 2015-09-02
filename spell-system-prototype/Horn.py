__author__ = 'thecomet'

from SpellBase import SpellBase
import pygame


class Horn(SpellBase):

    def __init__(self, position):
        super(Horn, self).__init__("Horn", (200, 255, 255), position)
        self.is_draggable = False

    def draw(self, surface):
        super(Horn, self).draw(surface)
        pygame.draw.circle(surface, (255, 255, 255), (self.position[0] - 32, self.position[1]), 30, 1)
        pygame.draw.circle(surface, (255, 255, 255), (self.position[0] - 70, self.position[1]), 40, 1)
        pygame.draw.circle(surface, (0, 0, 0), (self.position[0] - 32, self.position[1]), 29)
        pygame.draw.circle(surface, (0, 0, 0), (self.position[0] - 70, self.position[1]), 39)
        pygame.draw.circle(surface, (0, 0, 0), self.position, 19)
