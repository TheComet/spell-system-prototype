__author__ = 'thecomet'

from Updateable import Updateable
from Spell import Spell


class SpellCraftingManager(Updateable, Spell.Listener):

    def __init__(self):
        self.updateable_items = list()
        self.spells = list()
        self.create_spell_template("Spell", (400, 300))

    def create_spell_template(self, name, position):
        template = Spell(name, position)
        template.dragging_enabled = False
        template.listeners.append(self)
        self.updateable_items.append(template)

    def on_spell_clicked(self, spell):
        # if the spell is a template (i.e. it doesn't have dragging enabled), create a new, draggable clone
        if not spell.dragging_enabled:
            self.create_new_spell_from_template(spell)

    def create_new_spell_from_template(self, template):
        new_spell = Spell(template.label.text, template.position)
        new_spell.listeners.append(self)
        self.spells.append(new_spell)
        self.updateable_items.append(new_spell)

    def on_spell_released(self, spell):
        print('spell "{}" was released'.format(spell.label.text))

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
        direction_vec = (spell.position[0] - other_spell.position[0], spell.position[1] - other_spell.position[1])
        hypothenuse = (direction_vec[0]**2 + direction_vec[1]**2)**0.5
        direction_vec = (direction_vec[0] / hypothenuse, direction_vec[1] / hypothenuse)

        speed = time_step * 30
        spell.position = (spell.position[0] + direction_vec[0] * speed,
                          spell.position[1] + direction_vec[1] * speed)
        if not other_spell.is_dragging:
            other_spell.position = (other_spell.position[0] - direction_vec[0] * speed,
                                    other_spell.position[1] - direction_vec[1] * speed)