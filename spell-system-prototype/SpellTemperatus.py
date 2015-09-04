__author__ = 'thecomet'

from SpellBase import SpellBase
from SpellLabel import SpellLabel


class SpellTemperatus(SpellBase):

    def __init__(self, position):
        self.color = (255, 40, 40)
        super(SpellTemperatus, self).__init__("Temperatus", self.color, position)
        self.__ambient_temperature = 293.15
        self.__target_temperature = 293.15
        self.__temperature_label = SpellLabel(self, '{} K'.format(self.__target_temperature), (0, self.radius * 1.3))

    def draw(self, surface):
        super(SpellTemperatus, self).draw(surface)
        if self.is_activated:
            self.__temperature_label.draw(surface)

    def create_instance(self):
        return SpellTemperatus(self.position)

    def calculate_local_power_requirement(self):
        return 0

    @staticmethod
    def __celcius_to_kelvin(celcius):
        return 273.15 + celcius

    @property
    def total_links_out(self):
        return 3

    @property
    def total_links_in(self):
        return 1

    @property
    def efficiency(self):
        return 0.5

    @property
    def heat_dissipation(self):
        return 0.0
