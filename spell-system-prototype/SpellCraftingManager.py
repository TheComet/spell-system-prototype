__author__ = 'thecomet'

from Updateable import Updateable
from SpellBase import SpellBase
from SpellLumen import SpellLumen
from Horn import Horn
import heapq


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
        candidates = [x for x in self.spells if not x.is_template and not x.is_dragging]
        for n, spell in enumerate(candidates):
            for other_spell in candidates[n + 1:]:
                if self.__spells_are_colliding(spell, other_spell):
                    self.__move_spells_apart(spell, other_spell, time_step)

    def __handle_floating_spell_links(self):
        if not self.__floating_spell:
            return

        max_link_range = 150
        free_link_slots = self.__floating_spell.free_link_slots_in + 1
        # create a list of key-value pairs as tuples. key=distance, value=spell object
        distance_spell_pairs = ((self.__floating_spell.distance_to_squared(x), x)
                                for x in self.spells if x is not self.__floating_spell)
        candidates = sorted(x for x in distance_spell_pairs if x[0] < max_link_range**2)[:free_link_slots]

        for distance, spell in candidates:
            pass

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
        if spell.is_draggable:
            spell.position = (spell.position[0] + direction[0] * speed,
                              spell.position[1] + direction[1] * speed)
        if other_spell.is_draggable:
            other_spell.position = (other_spell.position[0] - direction[0] * speed,
                                    other_spell.position[1] - direction[1] * speed)
