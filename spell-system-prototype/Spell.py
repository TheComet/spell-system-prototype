__author__ = 'thecomet'

from Updateable import Updateable
from DraggableCircle import DraggableCircle
from SpellLabel import SpellLabel


class Spell(Updateable):

    def __init__(self, name, position):
        self.circle = DraggableCircle((255, 255, 255), position, 20)
        self.label = SpellLabel(self, name)

    def process_event(self, event):
        self.circle.process_event(event)

    def update(self, time_step):
        self.circle.update(time_step)

    def draw(self, surface):
        self.circle.draw(surface)
        self.label.draw(surface)
