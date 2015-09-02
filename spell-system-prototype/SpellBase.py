__author__ = 'thecomet'

from DraggableCircle import DraggableCircle
from SpellLabel import SpellLabel
import pygame


class SpellBase(DraggableCircle):

    class Listener(DraggableCircle.Listener):
        def on_draggable_circle_clicked(self, draggable_circle):
            self.on_spell_clicked(draggable_circle)

        def on_draggable_circle_released(self, draggable_circle):
            self.on_spell_released(draggable_circle)

        def on_spell_clicked(self, spell):
            pass

        def on_spell_released(self, spell):
            pass

    def __init__(self, name, color, position):
        super(SpellBase, self).__init__(color, position, 20)
        self.label = SpellLabel(self, name)

        self.is_template = False

    def process_event(self, event):
        super(SpellBase, self).process_event(event)

    def update(self, time_step):
        super(SpellBase, self).update(time_step)
        self.__keep_spell_on_screen()

    def draw(self, surface):
        super(SpellBase, self).draw(surface)
        self.label.draw(surface)

    def clone(self):
        raise NotImplementedError('Spells must implement this method')

    def __keep_spell_on_screen(self):
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        self.position = (min(max(self.position[0], self.radius), width - self.radius),
                         min(max(self.position[1], self.radius), height - self.radius))
