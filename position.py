#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

# FIXME 方角が文字の場合と単語の場合とで別々に生成するのは良くなさそう。一括で管理できないかな。

NUM_TO_DIRECTION = dict(enumerate([
    'n',
    'e',
    's',
    'w']))
DIRECTION_TO_NUM = dict(zip(NUM_TO_DIRECTION.values(), NUM_TO_DIRECTION.keys()))
DIRECTION_WORD = ['North', 'East', 'South', 'West']

DIRECTION_MOVE = ([-1, 0], [0, 1], [1, 0], [0, -1])


class PositionAndDirectionFactory(object):
    @staticmethod
    def make_north_p(position):
        return PositionAndDirection(position, DIRECTION_TO_NUM['n'])

    @staticmethod
    def make_east_p(position):
        return PositionAndDirection(position, DIRECTION_TO_NUM['e'])

    @staticmethod
    def make_south_p(position):
        return PositionAndDirection(position, DIRECTION_TO_NUM['s'])

    @staticmethod
    def make_west_p(position):
        return PositionAndDirection(position, DIRECTION_TO_NUM['w'])


class PositionAndDirection(object):
    def __init__(self, position, direction=DIRECTION_TO_NUM['n']):
        self.position = position
        self.direction = direction

    def __move_towards(self, direction):
        self.direction = direction

        self.position[0] += DIRECTION_MOVE[direction][0]
        self.position[1] += DIRECTION_MOVE[direction][1]

    def move_north(self):
        self.__move_towards(DIRECTION_TO_NUM['n'])

    def move_east(self):
        self.__move_towards(DIRECTION_TO_NUM['e'])

    def move_south(self):
        self.__move_towards(DIRECTION_TO_NUM['s'])

    def move_west(self):
        self.__move_towards(DIRECTION_TO_NUM['w'])

    def turn_north(self):
        self.direction = DIRECTION_TO_NUM['n']

    def turn_east(self):
        self.direction = DIRECTION_TO_NUM['e']

    def turn_south(self):
        self.direction = DIRECTION_TO_NUM['s']

    def turn_west(self):
        self.direction = DIRECTION_TO_NUM['w']

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

    def get_direction_by_character(self):
        return NUM_TO_DIRECTION[self.direction]

    def get_direction_by_word(self):
        return DIRECTION_WORD[self.direction]
