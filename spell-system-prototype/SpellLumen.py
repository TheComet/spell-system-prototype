__author__ = 'thecomet'

from SpellBase import SpellBase


class SpellLumen(SpellBase):

    def __init__(self, position):
        super(SpellLumen, self).__init__('Lumen', (255, 255, 255), position)

    def clone(self):
        return SpellLumen(self.position)
