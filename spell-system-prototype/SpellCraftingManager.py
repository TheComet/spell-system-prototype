__author__ = 'thecomet'

from Updateable import Updateable
from SpellBase import SpellBase
from SpellLumen import SpellLumen
from SpellTemperatus import SpellTemperatus
from Horn import Horn


class SpellCraftingManager(Updateable, SpellBase.Listener):

    def __init__(self):
        self.updateable_items = list()
        self.spells = list()
        self.horn = None

        self.__floating_spell = None

        self.__create_horn()
        self.__create_all_spell_templates()

    def __create_horn(self):
        self.horn = Horn((70, 300))
        self.spells.append(self.horn)
        self.updateable_items.append(self.horn)

    def __create_all_spell_templates(self):
        self.add_spell_as_template(SpellLumen((50, 550)))
        self.add_spell_as_template(SpellTemperatus((120, 550)))

    def add_spell_as_template(self, spell):
        spell.is_draggable = False
        spell.is_template = True
        spell.listeners.append(self)
        self.updateable_items.append(spell)

    def create_new_spell_from_template(self, template):
        new_spell = template.create_instance()
        new_spell.listeners.append(self)
        self.spells.append(new_spell)
        self.updateable_items.append(new_spell)
        return new_spell

    def on_spell_clicked(self, spell):
        if spell.is_template:
            self.__floating_spell = self.create_new_spell_from_template(spell)
        else:
            self.__floating_spell = spell

    def on_spell_released(self, spell):
        if self.__floating_spell:
            self.__floating_spell = None

    def process_event(self, event):
        for item in self.updateable_items:
            item.process_event(event)

    def update(self, time_step):
        for item in self.updateable_items:
            item.update(time_step)
        self.__handle_collisions_between_spells(time_step)
        self.__handle_floating_spell_links()

    def draw(self, surface):
        for item in self.updateable_items:
            item.draw(surface)

    def __handle_collisions_between_spells(self, time_step):
        for n, spell in enumerate(self.spells):
            for other_spell in self.spells[n + 1:]:
                if self.__spells_are_colliding(spell, other_spell):
                    self.__move_spells_apart(spell, other_spell, time_step)

    def __handle_floating_spell_links(self):
        if not self.__floating_spell:
            return

        self.__floating_spell.unlink_local()
        self.__handle_floating_spell_links_in(150)
        self.__handle_floating_spell_links_out(150)

    def __handle_floating_spell_links_in(self, max_link_range):
        free_link_slots = self.__floating_spell.free_link_slots_in
        # create a list of key-value pairs as tuples. key=distance, value=spell object
        distance_spell_pairs = ((self.__floating_spell.distance_to_squared(x), x)
                                for x in self.spells if x is not self.__floating_spell
                                and x.position[0] < self.__floating_spell.position[0])
        candidates = sorted(x for x in distance_spell_pairs
                            if x[0] < max_link_range**2 and x[1].free_link_slots_out > 0)[:free_link_slots]

        for distance, spell in candidates:
            self.__floating_spell.link_input_to(spell)

    def __handle_floating_spell_links_out(self, max_link_range):
        free_link_slots = self.__floating_spell.free_link_slots_out
        # create a list of key-value pairs as tuples. key=distance, value=spell object
        distance_spell_pairs = ((self.__floating_spell.distance_to_squared(x), x)
                                for x in self.spells if x is not self.__floating_spell
                                and x.position[0] > self.__floating_spell.position[0])
        candidates = sorted(x for x in distance_spell_pairs
                            if x[0] < max_link_range**2 and x[1].free_link_slots_in > 0)[:free_link_slots]

        for distance, spell in candidates:
            self.__floating_spell.link_output_to(spell)

    @staticmethod
    def __spells_are_colliding(spell, other_spell):
        dist = spell.radius + other_spell.radius
        if spell.distance_to_squared(other_spell) <= dist**2:
            return True
        return False

    @staticmethod
    def __move_spells_apart(spell, other_spell, time_step):
        # normalised direction vector
        direction = (spell.position[0] - other_spell.position[0], spell.position[1] - other_spell.position[1])
        hypothenuse = (direction[0]**2 + direction[1]**2)**0.5
        if hypothenuse > 0:
            direction = (direction[0] / hypothenuse, direction[1] / hypothenuse)
        else:
            direction = (0, 1)

        # push spells apart
        speed = time_step * 50
        if spell.is_draggable and not spell.is_template and not spell.is_dragging:
            spell.position = (spell.position[0] + direction[0] * speed,
                              spell.position[1] + direction[1] * speed)
        if other_spell.is_draggable and not other_spell.is_template and not other_spell.is_dragging:
            other_spell.position = (other_spell.position[0] - direction[0] * speed,
                                    other_spell.position[1] - direction[1] * speed)
