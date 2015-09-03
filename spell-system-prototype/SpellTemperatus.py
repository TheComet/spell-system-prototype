__author__ = 'thecomet'

from SpellBase import SpellBase


class SpellTemperatus(SpellBase):

    def __init__(self, position):
        self.color = (255, 40, 40)
        super(SpellTemperatus, self).__init__("Temperatus", self.color, position)

    @property
    def total_links_out(self):
        return 3

    @property
    def total_links_in(self):
        return 1

    def create_instance(self):
        return SpellTemperatus(self.position)

    def calculate_local_energy_requirement(self):
        return 0
