__author__ = 'thecomet'

import pygame
from Updateable import Updateable


class DraggableCircle(Updateable):

    def __init__(self, color, position, radius):
        self.color = color
        self.position = position
        self.radius = radius

        self.__actual_radius = radius
        self.__is_dragging = False

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[0] - self.position[0])**2 + (event.pos[1] - self.position[1])**2 <= self.radius**2:
                self.__is_dragging = True
                self.position = event.pos

        if event.type == pygame.MOUSEMOTION and self.__is_dragging:
            self.position = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            self.__is_dragging = False

    def update(self, time_step):
        target_radius = self.radius * 1.2 if self.__is_dragging else self.radius
        diff = target_radius - self.__actual_radius
        self.__actual_radius += diff * time_step * 10

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, int(self.__actual_radius), 1)
