__author__ = 'thecomet'

import pygame
from Updateable import Updateable


class DraggableCircle(Updateable):

    class Listener(object):
        def on_draggable_circle_clicked(self, draggable_circle):
            pass

        def on_draggable_circle_released(self, draggable_circle):
            pass

    def __init__(self, color, position, radius):
        self.color = color
        self.position = position
        self.listeners = list()

        self.__radius = radius
        self.__actual_radius = radius
        self.__is_draggable = True
        self.__is_dragging = False
        self.__cursor_grab_offset = None

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__cursor_grab_offset = (self.position[0] - event.pos[0], self.position[1] - event.pos[1])
            if self.__cursor_grab_offset[0]**2 + self.__cursor_grab_offset[1]**2 <= self.__radius**2:
                self.__set_dragging(True)
                self.__notify_clicked()

        if event.type == pygame.MOUSEMOTION and self.__is_dragging:
            self.position = (event.pos[0] + self.__cursor_grab_offset[0], event.pos[1] + self.__cursor_grab_offset[1])

        if event.type == pygame.MOUSEBUTTONUP:
            if self.__is_dragging:
                self.__notify_released()
            self.__set_dragging(False)

    def update(self, time_step):
        factor = 1.3
        target_radius = self.__radius * factor if self.__is_dragging else self.__radius
        max_diff = (target_radius - self.__actual_radius)
        diff = max_diff * time_step * 40
        self.__actual_radius += min(diff, max_diff) if diff > 0 else max(diff, max_diff)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, tuple(map(int, self.position)), int(self.__actual_radius), 1)
        pygame.draw.circle(surface, (0, 0, 0), tuple(map(int, self.position)), int(self.__actual_radius) - 1)

    @property
    def radius(self):
        return int(self.__actual_radius)

    @radius.setter
    def radius(self, radius):
        self.__radius = radius

    @property
    def is_draggable(self):
        return self.__is_draggable

    @is_draggable.setter
    def is_draggable(self, enable):
        self.__is_draggable = enable
        self.__is_dragging = False

    @property
    def is_dragging(self):
        return self.__is_dragging

    def __set_dragging(self, enable):
        if self.__is_draggable:
            self.__is_dragging = enable

    def __notify_clicked(self):
        for item in self.listeners:
            item.on_draggable_circle_clicked(self)

    def __notify_released(self):
        for item in self.listeners:
            item.on_draggable_circle_released(self)
