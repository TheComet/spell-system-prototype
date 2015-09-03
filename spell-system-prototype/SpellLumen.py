__author__ = 'thecomet'

from SpellBase import SpellBase


class SpellLumen(SpellBase):

    def __init__(self, position):
        self.color = (255, 255, 255)
        super(SpellLumen, self).__init__('Lumen', self.color, position)

    def create_instance(self):
        return SpellLumen(self.position)

    def calculate_local_energy_requirement(self):
        return 0

    @property
    def total_links_in(self):
        return 1

    @property
    def total_links_out(self):
        return 1
