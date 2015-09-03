__author__ = 'thecomet'

from SpellBase import SpellBase
import pygame


class Horn(SpellBase):

    def __init__(self, position):
        self.color = (255, 180, 255)
        super(Horn, self).__init__("Horn", self.color, position)
        self.is_draggable = False

        self.__num_supported_links = 1

    def draw(self, surface):
        super(Horn, self).draw(surface)
        pygame.draw.circle(surface, self.color, (self.position[0] - 32, self.position[1]), 30, 1)
        pygame.draw.circle(surface, self.color, (self.position[0] - 70, self.position[1]), 40, 1)
        pygame.draw.circle(surface, (0, 0, 0), (self.position[0] - 32, self.position[1]), 29)
        pygame.draw.circle(surface, (0, 0, 0), (self.position[0] - 70, self.position[1]), 39)
        pygame.draw.circle(surface, (0, 0, 0), self.position, 19)

    def create_instance(self):
        raise RuntimeError("Can't create instances of horns!")

    def calculate_local_energy_requirement(self):
        return 0

    @property
    def total_links_in(self):
        return 0

    @property
    def total_links_out(self):
        return self.__num_supported_links
