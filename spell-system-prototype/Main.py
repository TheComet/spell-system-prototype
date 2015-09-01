__author__ = 'thecomet'

import sys
import pygame
from Window import Window

if __name__ == '__main__':
    pygame.init()
    window = Window(800, 600)
    window.enter_main_loop()
    pygame.quit()
    sys.exit(0)
