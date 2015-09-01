__author__ = 'thecomet'

import pygame
from Updateable import Updateable


class DraggableCircle(Updateable):

    def __init__(self, color, position, radius):
        self.color = color
        self.position = position
        self.__radius = radius

        self.__actual_radius = radius
        self.__is_dragging = False
        self.__cursor_grab_offset = None

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__cursor_grab_offset = (self.position[0] - event.pos[0], self.position[1] - event.pos[1])
            if self.__cursor_grab_offset[0]**2 + self.__cursor_grab_offset[1]**2 <= self.__radius**2:
                self.__is_dragging = True

        if event.type == pygame.MOUSEMOTION and self.__is_dragging:
            self.position = (event.pos[0] + self.__cursor_grab_offset[0], event.pos[1] + self.__cursor_grab_offset[1])

        if event.type == pygame.MOUSEBUTTONUP:
            self.__is_dragging = False

    def update(self, time_step):
        target_radius = self.__radius * 1.3 if self.__is_dragging else self.__radius
        diff = target_radius - self.__actual_radius
        self.__actual_radius += diff * time_step * 40

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, int(self.__actual_radius), 1)

    @property
    def radius(self):
        return int(self.__actual_radius)

    @radius.setter
    def radius(self, radius):
        self.__radius = radius
