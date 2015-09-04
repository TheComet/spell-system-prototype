__author__ = 'thecomet'

from Updateable import Updateable
from SpellLumen import SpellLumen
from SpellTemperatus import SpellTemperatus
from Horn import Horn
import Event
import pygame


class SpellCraftingManager(Updateable):

    def __init__(self):
        self.updateable_items = list()
        self.spells = list()
        self.horn = None

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
        self.updateable_items.append(spell)

    def create_new_spell_from_template(self, template):
        new_spell = template.create_instance()
        self.spells.append(new_spell)
        self.updateable_items.append(new_spell)
        return new_spell

    def destroy_spell(self, spell):
        self.spells.remove(spell)
        self.updateable_items.remove(spell)
        spell.unlink_chain()

    def __on_spell_clicked(self, spell):
        if spell.is_template:
            new_spell = self.create_new_spell_from_template(spell)
            new_spell.grab()
        else:
            for other_spell in spell.links_out:
                other_spell.grab()

    def __remove_dead_spells(self):
        for spell in [x for x in self.spells if x is not self.horn]:
            if not self.horn.is_linked_to(spell):
                self.destroy_spell(spell)

    def process_event(self, event):
        for item in self.updateable_items:
            item.process_event(event)

        if event.type == Event.SPELLCLICKED:
            self.__on_spell_clicked(event.spell)

        if event.type == pygame.MOUSEMOTION:
            self.__handle_floating_spell_links()

        if event.type == Event.SPELLRELEASED:
            self.__handle_floating_spell_links()
            self.__notify_remove_dead_spells()
            self.horn.update_power()

        if event.type == Event.REMOVEDEADSPELLS:
            self.__remove_dead_spells()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    def update(self, time_step):
        for item in self.updateable_items:
            item.update(time_step)
        self.__handle_collisions_between_spells(time_step)

    def draw(self, surface):
        for item in self.updateable_items:
            item.draw(surface)

    def __handle_collisions_between_spells(self, time_step):
        for n, spell in enumerate(self.spells):
            for other_spell in self.spells[n + 1:]:
                if self.__spells_are_colliding(spell, other_spell):
                    self.__move_spells_apart(spell, other_spell, time_step)

    def __handle_floating_spell_links(self):
        for spell in self.spells:
            spell.unlink_local()
        self.__relink_all_spells(150)

    def __relink_all_spells(self, max_link_range):
        for spell in self.spells:
            free_link_slots = spell.free_link_slots_in
            # create a list of key-value pairs as tuples. key=distance, value=spell object
            distance_spell_pairs = [(spell.distance_to_squared(x), x)
                                    for x in self.spells if x is not spell
                                    and x.position[0] < spell.position[0]]
            candidates = sorted((x for x in distance_spell_pairs
                                if x[0] < max_link_range**2 and x[1].free_link_slots_out > 0),
                                key=lambda y: y[0])[:free_link_slots]

            for distance, other_spell in candidates:
                spell.link_input_to(other_spell)

    @staticmethod
    def __notify_remove_dead_spells():
        evt = pygame.event.Event(Event.REMOVEDEADSPELLS)
        pygame.event.post(evt)

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
