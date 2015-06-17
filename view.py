#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import observer


class Viewer(observer.Subject):
    def __init__(self, map_model: "model.MapModel"):
        observer.Subject.__init__(self)
        self.map_model = map_model
        self.map_list = []
        self.message_list = []

    def draw(self):
        self.draw_map()
        self.draw_message()

    def draw_map(self):
        map_list = [[None for _ in range(self.map_model.width)] for _ in range(self.map_model.height)]

        for floor_object in self.map_model.floor_objects:
            position = floor_object.get_position()
            y = position[0]
            x = position[1]

            map_list[y][x] = floor_object

        for obstacle_object in self.map_model.obstacle_objects:
            position = obstacle_object.get_position()
            y = position[0]
            x = position[1]
            map_list[y][x] = obstacle_object

        for y in range(self.map_model.height):
            for x in range(self.map_model.width):
                print(map_list[y][x].icon, end='')
            print('')

    def draw_message(self):
        print('#' * self.map_model.width)
        print("# " + self.map_model.message)
        print('#' * self.map_model.width)

    @staticmethod
    def draw_message_before_input():
        print('')
        print('')

    def draw_message_after_input(self, input_message):
        print('>' * self.map_model.width, end='')
        print(' ', end='')
        print(input_message)
