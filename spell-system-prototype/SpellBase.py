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
        self.__name = name
        self.label = SpellLabel(self, name)
        self.is_template = False
        self._links_in = list()
        self._links_out = list()

    def calculate_total_energy_requirement(self):
        energy = self.calculate_local_energy_requirement()
        for link in self._links_in:
            energy += link.calculate_total_energy_requirement()
        return energy

    def distance_to_squared(self, other_spell):
        dx = self.position[0] - other_spell.position[0]
        dy = self.position[1] - other_spell.position[1]
        return dx**2 + dy**2

    def process_event(self, event):
        super(SpellBase, self).process_event(event)

    def update(self, time_step):
        super(SpellBase, self).update(time_step)
        self.__keep_spell_on_screen()

    def draw(self, surface):
        super(SpellBase, self).draw(surface)
        self.label.draw(surface)
        self.__draw_spell_links(surface)

    def __draw_spell_links(self, surface):
        for spell in self._links_out:
            pygame.draw.line(surface, self.color, self.position, spell.position)

    def link_input_to(self, other_spell):
        if self.free_link_slots_in == 0 or other_spell.free_link_slots_out == 0:
            raise RuntimeError("Spells don't have any free link slots")
        self._links_in.append(other_spell)
        other_spell._links_out.append(self)

    def link_output_to(self, other_spell):
        if self.free_link_slots_out == 0 or other_spell.free_link_slots_in == 0:
            raise RuntimeError("Spells don't have any free link slots")
        self._links_out.append(other_spell)
        other_spell._links_in.append(self)

    def unlink_local(self):
        for linked in self._links_out:
            linked._links_in.remove(self)

        for linked in self._links_in:
            linked._links_out.remove(self)

        self._links_out = list()
        self._links_in = list()

    def unlink_chain(self):
        for linked in self._links_out:
            linked.unlink_chain()
        self._links_out = list()

        for linked in self._links_in:
            linked.unlink_chain()
        self._links_in = list()

    @property
    def free_link_slots_in(self):
        return self.total_links_in - len(self._links_in)

    @property
    def free_link_slots_out(self):
        return self.total_links_out - len(self._links_out)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
        self.label = SpellLabel(self, name)

    def __keep_spell_on_screen(self):
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        self.position = (min(max(self.position[0], self.radius), width - self.radius),
                         min(max(self.position[1], self.radius), height - self.radius))

    ####################################################################################################################
    # Interface for derived spells
    ####################################################################################################################

    def create_instance(self):
        raise NotImplementedError('Spells must be able to create instances of themselves')
        # return a new instance of this class. The new instance shouldn't be an exact copy of all members, it just needs
        # to have bare initialisation (e.g. set the position and name).
        #
        # something like:
        # return MySpell(self.position)

    def calculate_local_energy_requirement(self):
        raise NotImplementedError('Spells must provide their energy requirement')

    @property
    def total_links_in(self):
        raise NotImplementedError('Spells must provide information on how many links they can handle as input')

    @property
    def total_links_out(self):
        raise NotImplementedError('Spells must provide information on how many links they can handle as output')
