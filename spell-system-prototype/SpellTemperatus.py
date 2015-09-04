__author__ = 'thecomet'

from SpellBase import SpellBase


class SpellTemperatus(SpellBase):

    def __init__(self, position):
        self.color = (255, 40, 40)
        super(SpellTemperatus, self).__init__("Temperatus", self.color, position)

    def create_instance(self):
        return SpellTemperatus(self.position)

    def calculate_local_power_requirement(self):
        return 0

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
