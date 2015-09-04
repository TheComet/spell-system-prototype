__author__ = 'thecomet'

from SpellBase import SpellBase
from SpellLabel import SpellLabel


class SpellLumen(SpellBase):

    def __init__(self, position):
        self.color = (255, 255, 255)
        super(SpellLumen, self).__init__('Lumen', self.color, position)
        self.__lumen_label = SpellLabel(self, '0', (0, self.radius * 1.3))
        self.__lumen = 0.0

        # set properties
        self.lumen = 3000

    def create_instance(self):
        return SpellLumen(self.position)

    def calculate_local_power_requirement(self):
        # 1 cd = 1 lumen/sr
        # 1 cd = 683 W/sr
        # 1 lumen/sr = 1/683 W/sr
        # 1 lumen = 1/683 W
        return self.__lumen / 683.0

    def draw(self, surface):
        super(SpellLumen, self).draw(surface)
        if self.is_activated:
            self.__lumen_label.draw(surface)

    @property
    def lumen(self):
        return self.__lumen

    @lumen.setter
    def lumen(self, lumen):
        self.__lumen = lumen
        self.__lumen_label.text = '{} lm'.format(int(self.__lumen))

    @property
    def total_links_in(self):
        return 1

    @property
    def total_links_out(self):
        return 0

    @property
    def efficiency(self):
        # Based on the chemical reaction of luciferase with Adenosine triphosphate (ATP) (what fireflies use),
        # the most efficient energy-to-ligth conversion lies somewhere between 80% and 90%.
        # https://en.wikipedia.org/wiki/Luciferase
        return 0.85

    @property
    def heat_dissipation(self):
        # luciferase reactions create almost no heat whatsoever.
        return 0.01
