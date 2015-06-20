#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import random

FLOOR = 0
WALL = 1
ROUTE = 2


class Area(object):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def __init__(self, top: int, right: int, bottom: int, left: int):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

        self.border_side = None
        self.padding = 3

        if self.bottom - self.padding < self.top + self.padding \
                or self.left + self.padding > self.right - self.padding:
            raise Exception("too small!!")

    def split(self):
        split_vh = random.randint(0, 1)

        if split_vh == 0:
            border_v = random.randint(self.top + self.padding, self.bottom - self.padding)

            top_or_bottom = random.randint(0, 1)
            if top_or_bottom == 0:
                new_area = Area(self.top, self.right, border_v, self.left)
                self.border_side = self.TOP
                self.top = border_v - 1

            elif top_or_bottom == 1:
                new_area = Area(border_v, self.right, self.bottom, self.left)
                self.border_side = self.BOTTOM
                self.bottom = border_v + 1

        elif split_vh == 1:
            border_h = random.randint(self.left + self.padding, self.right - self.padding)

            left_or_right = random.randint(0, 1)
            if left_or_right == 0:
                new_area = Area(self.top, border_h, self.bottom, self.left)
                self.border_side = self.LEFT
                self.left = border_h + 1

            elif left_or_right == 1:
                new_area = Area(self.top, self.right, self.bottom, border_h)
                self.border_side = self.RIGHT
                self.right = border_h - 1

        return new_area


class DungeonGenerator(object):
    def __init__(self, size=(60, 80)):
        self.size = size
        self.map = [[FLOOR for _ in range(size[1])] for _ in range(size[0])]

        self.areas = [Area(0, size[1] - 1, size[0] - 1, 0)]

    def split_area(self):
        new_area = self.areas[-1].split()
        self.areas.append(new_area)

    def print_map(self):
        for y in self.map:
            for x in y:
                print(x, end='')
            print('')

    def print_area(self):
        area_map = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]

        for idx, area in enumerate(self.areas):
            for y in range(area.top, area.bottom + 1):
                for x in range(area.left, area.right + 1):
                    area_map[y][x] = idx

        for y in area_map:
            for idx in y:
                print(idx, end='')
            print('')


# FIXME ときどき too small!! と言われる。paddingまわりの設定が怪しい
if __name__ == '__main__':
    dg = DungeonGenerator()
    # dg.print_map()
    # dg.print_area()

    dg.split_area()
    dg.print_area()