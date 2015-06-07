#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'
# TODO enumerateを使ってdirectionを定義し直した方がいいか?


class PositionAndDirection(object):
    position = [0, 0]
    direction = 0

    DIRECTION_MOVE_LIST = ([1, 0], [0, 1], [-1, 0], [0, -1])

    def __init__(self, position, direction=0):
        self.position = position
        self.direction = direction

    def move_towards(self, direction):
        self.direction = direction

        self.position[0] += self.DIRECTION_MOVE_LIST[direction][0]
        self.position[1] += self.DIRECTION_MOVE_LIST[direction][1]

    def set_direction(self, direction):
        self.direction = direction

    def get_front_position(self):
        front_y = self.position[0] + self.DIRECTION_MOVE_LIST[self.direction][0]
        front_x = self.position[1] + self.DIRECTION_MOVE_LIST[self.direction][1]
        return [front_y, front_x]

    def get_position(self):
        return self.position

    # TODO getter系を全部書き換えよう
    def get_direction(self):
        return self.direction

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
