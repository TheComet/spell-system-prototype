__author__ = 'thecomet'

from DraggableCircle import DraggableCircle
from SpellLabel import SpellLabel
import pygame
import Event


class SpellBase(DraggableCircle):

    def __init__(self, name, color, position):
        super(SpellBase, self).__init__(color, position, 20)
        self.__name = name
        self.label = SpellLabel(self, name)
        self.is_template = False
        self.links_in = list()
        self.links_out = list()

    def calculate_total_energy_requirement(self):
        energy = self.calculate_local_energy_requirement()
        for link in self.links_in:
            energy += link.calculate_total_energy_requirement()
        return energy

    def distance_to_squared(self, other_spell):
        dx = self.position[0] - other_spell.position[0]
        dy = self.position[1] - other_spell.position[1]
        return dx**2 + dy**2

    def process_event(self, event):
        super(SpellBase, self).process_event(event)

        if event.type == Event.DRAGGABLECIRCLECLICKED and event.draggable_circle is self:
            self.__notify_spell_clicked()
        if event.type == Event.DRAGGABLECIRCLERELEASED and event.draggable_circle is self:
            self.__notify_spell_released()

    def update(self, time_step):
        super(SpellBase, self).update(time_step)
        self.__keep_spell_on_screen()

    def draw(self, surface):
        super(SpellBase, self).draw(surface)
        self.__draw_spell_links(surface)
        self.label.draw(surface)

    def __draw_spell_links(self, surface):
        for spell in self.links_out:
            pygame.draw.line(surface, self.color, self.position, spell.position)

    def link_input_to(self, other_spell):
        if not self.is_linkable or not other_spell.is_linkable:
            raise RuntimeError("Spells can't link!")
        if self.free_link_slots_in == 0 or other_spell.free_link_slots_out == 0:
            raise RuntimeError("Spells don't have any free link slots")
        self.links_in.append(other_spell)
        other_spell.links_out.append(self)

    def link_output_to(self, other_spell):
        if not self.is_linkable or not other_spell.is_linkable:
            raise RuntimeError("Spells can't link!")
        if self.free_link_slots_out == 0 or other_spell.free_link_slots_in == 0:
            raise RuntimeError("Spells don't have any free link slots")
        self.links_out.append(other_spell)
        other_spell.links_in.append(self)

    def unlink_local(self):
        for linked in self.links_out:
            linked.links_in.remove(self)

        for linked in self.links_in:
            linked.links_out.remove(self)

        self.links_out = list()
        self.links_in = list()

    def unlink_chain(self):
        self.unlink_chain_out()
        self.unlink_chain_in()

    def unlink_chain_out(self):
        for linked in self.links_out:
            linked.unlink_chain_out()
        self.links_out = list()

    def unlink_chain_in(self):
        for linked in self.links_in:
            linked.unlink_chain()
        self.links_in = list()

    def is_linked_to(self, other_spell):
        return other_spell in self.outward_spells or other_spell in self.inward_spells

    @property
    def is_linkable(self):
        return not self.is_template

    @property
    def outward_spells(self):
        spells = list()
        self.get_outward_spells(spells)
        return spells

    @property
    def inward_spells(self):
        spells = list()
        self.get_inward_spells(spells)
        return spells

    def get_outward_spells(self, spells):
        spells.append(self)
        for linked in self.links_out:
            linked.get_outward_spells(spells)

    def get_inward_spells(self, spells):
        spells.append(self)
        for linked in self.links_in:
            linked.get_inward_spells(spells)

    @property
    def free_link_slots_in(self):
        return self.total_links_in - len(self.links_in)

    @property
    def free_link_slots_out(self):
        return self.total_links_out - len(self.links_out)

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

    def __notify_spell_clicked(self):
        evt = pygame.event.Event(Event.SPELLCLICKED, spell=self)
        pygame.event.post(evt)

    def __notify_spell_released(self):
        evt = pygame.event.Event(Event.SPELLRELEASED, spell=self)
        pygame.event.post(evt)

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
