__author__ = 'thecomet'

import sys

import pygame

from Window import Window

if __name__ == '__main__':
    pygame.init()
    window = Window(640, 480)
    window.enter_main_loop()
    sys.exit(0)
