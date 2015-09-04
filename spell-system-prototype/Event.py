__author__ = 'thecomet'

import pygame

event_counter = 0


def unique_id():
    global event_counter
    event_counter += 1
    return pygame.USEREVENT + event_counter


DRAGGABLECIRCLECLICKED = unique_id()
DRAGGABLECIRCLERELEASED = unique_id()
SPELLCLICKED = unique_id()
SPELLRELEASED = unique_id()
REMOVEDEADSPELLS = unique_id()
