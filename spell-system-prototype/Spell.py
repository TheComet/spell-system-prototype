__author__ = 'thecomet'

from DraggableCircle import DraggableCircle
from SpellLabel import SpellLabel


class Spell(DraggableCircle):

    class Listener(DraggableCircle.Listener):
        def on_draggable_circle_clicked(self, draggable_circle):
            self.on_spell_clicked(draggable_circle)

        def on_draggable_circle_released(self, draggable_circle):
            self.on_spell_released(draggable_circle)

        def on_spell_clicked(self, spell):
            pass

        def on_spell_released(self, spell):
            pass

    def __init__(self, name, position):
        super(Spell, self).__init__((255, 255, 255), position, 20)
        self.label = SpellLabel(self, name)

    def process_event(self, event):
        super(Spell, self).process_event(event)

    def update(self, time_step):
        super(Spell, self).update(time_step)

    def draw(self, surface):
        super(Spell, self).draw(surface)
        self.label.draw(surface)
