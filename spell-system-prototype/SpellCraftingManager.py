__author__ = 'thecomet'

from Updateable import Updateable
from SpellBase import SpellBase
from SpellLumen import SpellLumen
from Horn import Horn


class SpellCraftingManager(Updateable, SpellBase.Listener):

    def __init__(self):
        self.updateable_items = list()
        self.spells = list()

        self.horn = Horn((70, 300))
        self.updateable_items.append(self.horn)

        self.create_all_spell_templates()

    def create_all_spell_templates(self):
        self.add_spell_as_template(SpellLumen((50, 550)))

    def add_spell_as_template(self, spell):
        spell.is_draggable = False
        spell.is_template = True
        spell.listeners.append(self)
        self.updateable_items.append(spell)

    def on_spell_clicked(self, spell):
        if spell.is_template:
            self.create_new_spell_from_template(spell)

    def create_new_spell_from_template(self, template):
        new_spell = template.clone()
        new_spell.listeners.append(self)
        self.spells.append(new_spell)
        self.updateable_items.append(new_spell)

    def on_spell_released(self, spell):
        pass

    def process_event(self, event):
        for item in self.updateable_items:
            item.process_event(event)

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

    @staticmethod
    def __spells_are_colliding(spell, other_spell):
        dx = spell.position[0] - other_spell.position[0]
        dy = spell.position[1] - other_spell.position[1]
        dist = spell.radius + other_spell.radius
        if dx**2 + dy**2 <= dist**2:
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

        # push spells apart - don't modify the position of spells that are still being dragged
        speed = time_step * 50
        if not spell.is_dragging:
            spell.position = (spell.position[0] + direction[0] * speed,
                              spell.position[1] + direction[1] * speed)
        if not other_spell.is_dragging:
            other_spell.position = (other_spell.position[0] - direction[0] * speed,
                                    other_spell.position[1] - direction[1] * speed)
