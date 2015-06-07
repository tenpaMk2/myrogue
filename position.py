#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'
# TODO enumerateを使ってdirectionを定義し直した方がいいか?

DIRECTION_LIST = {
    'n': 0,
    'e': 1,
    's': 2,
    'w': 3
}
DIRECTION_MOVE_LIST = ([-1, 0], [0, 1], [1, 0], [0, -1])


class PositionAndDirectionFactory(object):
    def make_north_p(self, position):
        return PositionAndDirection(position, DIRECTION_LIST['n'])

    def make_east_p(self, position):
        return PositionAndDirection(position, DIRECTION_LIST['e'])

    def make_south_p(self, position):
        return PositionAndDirection(position, DIRECTION_LIST['s'])

    def make_west_p(self, position):
        return PositionAndDirection(position, DIRECTION_LIST['w'])


class PositionAndDirection(object):
    def __init__(self, position, direction=0):
        self.position = position
        self.direction = direction

    def __move_towards(self, direction):
        self.direction = direction

        self.position[0] += DIRECTION_MOVE_LIST[direction][0]
        self.position[1] += DIRECTION_MOVE_LIST[direction][1]

    def move_north(self):
        self.__move_towards(DIRECTION_LIST['n'])

    def move_east(self):
        self.__move_towards(DIRECTION_LIST['e'])

    def move_south(self):
        self.__move_towards(DIRECTION_LIST['s'])

    def move_west(self):
        self.__move_towards(DIRECTION_LIST['w'])

    def turn_north(self):
        self.direction = DIRECTION_LIST['n']

    def turn_east(self):
        self.direction = DIRECTION_LIST['e']

    def turn_south(self):
        self.direction = DIRECTION_LIST['s']

    def turn_west(self):
        self.direction = DIRECTION_LIST['w']

    def run(self):
        self.__move_towards(self.direction)

    def set_direction(self, direction):
        self.direction = direction

    def get_front_position(self):
        front_y = self.position[0] + DIRECTION_MOVE_LIST[self.direction][0]
        front_x = self.position[1] + DIRECTION_MOVE_LIST[self.direction][1]
        return [front_y, front_x]

    def get_position(self):
        return self.position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if not len(position) == 2:
            raise ValueError("value must have 2 elements")
        self._position = list(position)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if not 0 <= direction <= 3:
            raise ValueError("direction must be [0, 3]")
        self._direction = direction

    def get_direction_by_charcter(self):
        for key in DIRECTION_LIST:
            if DIRECTION_LIST[key] == self.direction:
                return key
