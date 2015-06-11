#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'
# TODO enumerateを使ってdirectionを定義し直した方がいいか?

NUM_DIRECTION = dict(enumerate([
    'n',
    'e',
    's',
    'w']))
DIRECTION_NUM = dict(zip(NUM_DIRECTION.values(), NUM_DIRECTION.keys()))

DIRECTION_MOVE = ([-1, 0], [0, 1], [1, 0], [0, -1])


class PositionAndDirectionFactory(object):
    @staticmethod
    def make_north_p(position):
        return PositionAndDirection(position, DIRECTION_NUM['n'])

    @staticmethod
    def make_east_p(position):
        return PositionAndDirection(position, DIRECTION_NUM['e'])

    @staticmethod
    def make_south_p(position):
        return PositionAndDirection(position, DIRECTION_NUM['s'])

    @staticmethod
    def make_west_p(position):
        return PositionAndDirection(position, DIRECTION_NUM['w'])


class PositionAndDirection(object):
    def __init__(self, position, direction=DIRECTION_NUM['n']):
        self.position = position
        self.direction = direction

    def __move_towards(self, direction):
        self.direction = direction

        self.position[0] += DIRECTION_MOVE[direction][0]
        self.position[1] += DIRECTION_MOVE[direction][1]

    def move_north(self):
        self.__move_towards(DIRECTION_NUM['n'])

    def move_east(self):
        self.__move_towards(DIRECTION_NUM['e'])

    def move_south(self):
        self.__move_towards(DIRECTION_NUM['s'])

    def move_west(self):
        self.__move_towards(DIRECTION_NUM['w'])

    def turn_north(self):
        self.direction = DIRECTION_NUM['n']

    def turn_east(self):
        self.direction = DIRECTION_NUM['e']

    def turn_south(self):
        self.direction = DIRECTION_NUM['s']

    def turn_west(self):
        self.direction = DIRECTION_NUM['w']

    def run(self):
        self.__move_towards(self.direction)

    def set_direction(self, direction):
        self.direction = direction

    def get_front_position(self):
        front_y = self.position[0] + DIRECTION_MOVE[self.direction][0]
        front_x = self.position[1] + DIRECTION_MOVE[self.direction][1]
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
        for key in DIRECTION_NUM:
            if DIRECTION_NUM[key] == self.direction:
                return key
