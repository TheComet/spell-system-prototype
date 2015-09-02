__author__ = 'thecomet'

from Updateable import Updateable
from Spell import Spell


class SpellCraftingManager(Updateable):

    def __init__(self):
        self.updatable_items = list()
        self.create_spell_template("Spell", (400, 300))

    def create_spell_template(self, name, position):
        self.updatable_items.append(Spell(name, position))

    def process_event(self, event):
        for item in self.updatable_items:
            item.process_event(event)

    def update(self, time_step):
        for item in self.updatable_items:
            item.update(time_step)

    def draw(self, surface):
        for item in self.updatable_items:
            item.draw(surface)
