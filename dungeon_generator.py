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

    def __init__(self, index, top: int, right: int, bottom: int, left: int):
        self.index = index

        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

        self.border_side = None
        self.padding = 1  # min width(height) is padding*2+1

        self.top_split_max = self.top + self.padding * 2 + 1
        self.bottom_split_max = self.bottom - self.padding * 2 - 1
        self.left_split_max = self.left + self.padding * 2 + 1
        self.right_split_max = self.right - self.padding * 2 - 1

        if self.bottom - self.padding < self.top + self.padding \
                or self.left + self.padding > self.right - self.padding:
            raise Exception("too small!!")

    # TODO hとvで別々なのは単調すぎる。どこかで統一できるはず。
    def split_h(self):
        border_h = random.randint(self.top_split_max, self.bottom_split_max)

        top_or_bottom = random.randint(0, 1)
        if top_or_bottom == 0:
            new_area = Area(self.index + 1, self.top, self.right, border_h, self.left)
            self.border_side = self.TOP
            self.top = border_h + 1

            print("split to top : border_h : {0}".format(border_h))

        elif top_or_bottom == 1:
            new_area = Area(self.index + 1, border_h, self.right, self.bottom, self.left)
            self.border_side = self.BOTTOM
            self.bottom = border_h - 1

            print("split to bottom : border_h : {0}".format(border_h))

        else:
            raise Exception("split room only top or bottom!!")

        return new_area

    def split_v(self):
        border_v = random.randint(self.left_split_max, self.right_split_max)

        left_or_right = random.randint(0, 1)
        if left_or_right == 0:
            new_area = Area(self.index + 1, self.top, border_v, self.bottom, self.left)
            self.border_side = self.LEFT
            self.left = border_v + 1

            print("split to left : border_v : {0}".format(border_v))

        elif left_or_right == 1:
            new_area = Area(self.index + 1, self.top, self.right, self.bottom, border_v)
            self.border_side = self.RIGHT
            self.right = border_v - 1

            print("split to right : border_v : {0}".format(border_v))


        else:
            raise Exception("split room only left or right!!")

        return new_area

    def is_splittable_v(self):
        # 要はrandintが呼び出せるか否か
        print("top_split_max : {0}, bottom_split_max : {1}".format(self.top_split_max, self.bottom_split_max))
        print("left_split_max : {0}, right_split_max : {1}".format(self.left_split_max, self.right_split_max))

        if self.left_split_max > self.right_split_max:
            return False
        else:
            return True

    def is_splittable_h(self):
        # 要はrandintが呼び出せるか否か
        print("top_split_max : {0}, bottom_split_max : {1}".format(self.top_split_max, self.bottom_split_max))
        print("left_split_max : {0}, right_split_max : {1}".format(self.left_split_max, self.right_split_max))

        if self.top_split_max > self.bottom_split_max:
            return False
        else:
            return True

    def get_area(self):
        # 紛らわしいが面積のこと
        return (self.bottom - self.top) * (self.right - self.left)


class DungeonGenerator(object):
    def __init__(self, size=(8, 16)):
        self.size = size
        self.map = [[FLOOR for _ in range(size[1])] for _ in range(size[0])]

        self.areas = [Area(1, 0, size[1] - 1, size[0] - 1, 0)]

    def split_area(self, split_count: int):
        for c in range(split_count):
            print("------------c = {0} : start---------".format(c))
            current_area = self.areas[-1]
            if c % 2 == 0:
                if current_area.is_splittable_v():
                    new_area = current_area.split_v()
                else:
                    break
            else:
                if current_area.is_splittable_h():
                    new_area = current_area.split_h()
                else:
                    break

            # TODO 面積が大きい方が新たな分割エリアになるようにしよう。
            # if new_area.get_area() < current_area.get_area():
            #     self.areas.insert(-1, new_area)
            self.areas.append(new_area)

            self.print_area()
            print("-------------c = {0} : end------------".format(c))

    def print_map(self):
        for y in self.map:
            for x in y:
                print(x, end='')
            print('')

    def print_area(self):
        area_map = [['b' for _ in range(self.size[1])] for _ in range(self.size[0])]

        for area in self.areas:
            t = area.top if not area.border_side == Area.TOP else area.top + 1
            r = area.right if not area.border_side == Area.RIGHT else area.right - 1
            b = area.bottom if not area.border_side == Area.BOTTOM else area.bottom - 1
            l = area.left if not area.border_side == Area.LEFT else area.left + 1

            for y in range(t, b + 1):
                for x in range(l, r + 1):
                    area_map[y][x] = area.index

        for y in area_map:
            for idx in y:
                print(idx, end='')
            print('')

# FIXME ときどき too small!! と言われる。paddingまわりの設定が怪しい
if __name__ == '__main__':
    # random.seed(3)

    dg = DungeonGenerator((60, 80))
    # dg.print_map()
    # dg.print_area()

    dg.split_area(10)


    # for x in range(1000):
    #     try:
    #         dg = DungeonGenerator()
    #         # dg.print_map()
    #         # dg.print_area()
    #
    #         dg.split_area(2)
    #         dg.print_area()
    #     except:
    #         pass
