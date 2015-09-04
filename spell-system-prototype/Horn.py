__author__ = 'thecomet'

from SpellBase import SpellBase
from SpellLabel import SpellLabel
import pygame


class Horn(SpellBase):

    def __init__(self, position):
        self.color = (255, 180, 255)
        super(Horn, self).__init__("Horn", self.color, position)
        self.is_draggable = False

        self.__num_supported_links = 2
        self.__power_label = SpellLabel(self, '0W', (-230, 0))
        self.update_power()

    def draw(self, surface):
        super(Horn, self).draw(surface)
        pygame.draw.circle(surface, self.color, (self.position[0] - 32, self.position[1]), 30, 1)
        pygame.draw.circle(surface, self.color, (self.position[0] - 70, self.position[1]), 40, 1)
        pygame.draw.circle(surface, (0, 0, 0), (self.position[0] - 32, self.position[1]), 29)
        pygame.draw.circle(surface, (0, 0, 0), (self.position[0] - 70, self.position[1]), 39)
        pygame.draw.circle(surface, (0, 0, 0), self.position, 19)
        self.__power_label.draw(surface)

    def create_instance(self):
        raise RuntimeError("Can't create instances of horns!")

    def calculate_local_power_requirement(self):
        return 0.0

    def calculate_total_power_requirement(self):
        power = super(Horn, self).calculate_total_power_requirement()
        return power / self.efficiency

    def update_power(self):
        power = self.calculate_total_power_requirement()
        self.__power_label.text = '{0:.1f} W'.format(power)

    @property
    def total_links_in(self):
        return 0

    @property
    def total_links_out(self):
        return self.__num_supported_links

    @property
    def efficiency(self):
        return 0.90

    @property
    def heat_dissipation(self):
        return 0.05
