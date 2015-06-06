#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'


class View(object):
    def __init__(self, map_model: "MapModel"):
        self.map_model = map_model
        self.map_list = []
        self.message_list = []

    def draw_map(self):
        map_list = [[None for x in range(self.width)] for y in range(self.height)]

        for floor_object in self.floor_list:
            position = floor_object.get_position()
            y = position[0]
            x = position[1]

            map_list[y][x] = floor_object

        for obstacle_object in self.obstacle_list:
            position = obstacle_object.get_position()
            y = position[0]
            x = position[1]
            map_list[y][x] = obstacle_object

        for y in range(self.height):
            for x in range(self.width):
                print(map_list[y][x].icon, end='')
            print('')

        self.draw_message()

    def draw_message(self):
        print('#' * self.width)
        print("# " + self.message)
        print('#' * self.width + '\n')

        self.clear_message()

    def set_message(self, map_object, message: str):
        self.message = "{0} >{1}".format(map_object.pose_icon, message)
