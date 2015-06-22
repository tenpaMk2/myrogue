#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import random
from abc import ABCMeta, abstractmethod

ROOM_PADDING_Y = 3
ROOM_PADDING_X = 3

NOTHING = ' '
WALL = '#'
FLOOR = '.'
ROUTE = 'o'
ROUTE_CANDIDATE = '\''
DOOR = '+'

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
NODIRECTION = 4

FLIPPED_DIRECTION = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}


class AreaBase(metaclass=ABCMeta):
    def __init__(self, top: int, right: int, bottom: int, left: int):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

        self.height = self.bottom - self.top + 1
        self.width = self.right - self.left + 1

    def get_area(self):
        # 紛らわしいが面積のこと
        return self.height * self.width


class Room(AreaBase):
    def __init__(self, top: int, right: int, bottom: int, left: int):
        super(Room, self).__init__(top, right, bottom, left)

        self.door_position = (None, None)

        self.map = [[None for _ in range(self.width)] for _ in range(self.height)]

        self._make_wall()

    def _make_wall(self):
        for y in range(self.height):
            for x in range(self.width):
                if y == 0 or y == self.height - 1 or x == 0 or x == self.width - 1:
                    self.map[y][x] = WALL
                else:
                    self.map[y][x] = FLOOR

    def make_door(self, edge_select=NORTH):
        if edge_select == NORTH:
            door_g_y = self.top
            door_g_x = random.randint(self.left + 1, self.right - 1)

        elif edge_select == EAST:
            door_g_y = random.randint(self.top + 1, self.bottom - 1)
            door_g_x = self.right

        elif edge_select == SOUTH:
            door_g_y = self.bottom
            door_g_x = random.randint(self.left + 1, self.right - 1)

        elif edge_select == WEST:
            door_g_y = random.randint(self.top + 1, self.bottom - 1)
            door_g_x = self.left

        else:
            raise Exception("edge_select must be NORTH~WEST")

        self.door_position = (door_g_y, door_g_x)
        self.map[door_g_y - self.top][door_g_x - self.left] = DOOR


class Route(object):
    def __init__(self, parent_area: "Area", child_area: "Area"):
        self.parent_area = parent_area
        self.child_area = child_area

        self.parent_room = self.parent_area.room
        self.child_room = self.child_area.room

        self.route_positions = []

    def make_route(self):
        self.make_door()

        parent_door_g_y, parent_door_g_x = self.parent_room.door_position
        child_door_g_y, child_door_g_x = self.child_room.door_position

        print("door_position : ({0}, {1}) and ({2}, {3})"
              .format(parent_door_g_y, parent_door_g_x, child_door_g_y, child_door_g_x))

        start_pos = (parent_door_g_y, parent_door_g_x)
        end_pos = (child_door_g_y, child_door_g_x)
        if self.parent_area.border_side == NORTH \
                or self.parent_area.border_side == SOUTH:
            relay_pos1 = (self.parent_area.border.top, parent_door_g_x)
            relay_pos2 = (self.parent_area.border.top, child_door_g_x)

        elif self.parent_area.border_side == EAST \
                or self.parent_area.border_side == WEST:
            relay_pos1 = (parent_door_g_y, self.parent_area.border.right)
            relay_pos2 = (child_door_g_y, self.parent_area.border.right)
        else:
            raise Exception("border_side must be NORTH~WEST")

        relay_positions = [start_pos, relay_pos1, relay_pos2, end_pos]
        self.route_positions = self._make_positions_from_relay_positions(relay_positions)

        # start_posとend_posを除外しておく。
        self.route_positions.pop(0)
        self.route_positions.pop(-1)

        print("route_positions : {0}".format(self.route_positions))

    def make_door(self):
        self.parent_room.make_door(self.parent_area.border_side)
        self.child_room.make_door(FLIPPED_DIRECTION[self.parent_area.border_side])

    @staticmethod
    def _make_positions_from_relay_positions(relay_positions):
        print("relay_positions : {0}".format(relay_positions))

        route_positions = []

        for pos1, pos2 in zip(relay_positions, relay_positions[1:]):
            if pos1[0] == pos2[0]:
                crese_or_decrease = 1 if pos1[1] < pos2[1] else -1

                for x in range(pos1[1], pos2[1], crese_or_decrease):
                    route_positions.append((pos1[0], x))
            else:
                crese_or_decrease = 1 if pos1[0] < pos2[0] else -1
                for y in range(pos1[0], pos2[0], crese_or_decrease):
                    route_positions.append((y, pos1[1]))

        # 最後の座標だけ含まれないので、appendしておく。
        route_positions.append(relay_positions[-1])
        return route_positions


class ValidArea(AreaBase):
    pass


class Border(AreaBase):
    pass


class BorderV(Border):
    @property
    def right(self):
        if self.__is_same_left_and_right():
            return self._right
        else:
            raise Exception("This Border object's left-right is different!!")

    @right.setter
    def right(self, value: int):
        self.__set_left_and_right(value)

    @property
    def left(self):
        if self.__is_same_left_and_right():
            return self._left
        else:
            raise Exception("This Border object's left-right is different!!")

    @left.setter
    def left(self, value: int):
        self.__set_left_and_right(value)

    def __set_left_and_right(self, value):
        self._right = value
        self._left = value

    def __is_same_left_and_right(self):
        return True if self._right == self._left else False


class BorderH(Border):
    @property
    def bottom(self):
        if self.__is_same_top_and_bottom():
            return self._bottom
        else:
            raise Exception("This Border object's left-right is different!!")

    @bottom.setter
    def bottom(self, value: int):
        self.__set_top_and_bottom(value)

    @property
    def top(self):
        if self.__is_same_top_and_bottom():
            return self._top
        else:
            raise Exception("This Border object's left-right is different!!")

    @top.setter
    def top(self, value: int):
        self.__set_top_and_bottom(value)

    def __set_top_and_bottom(self, value):
        self._top = value
        self._bottom = value

    def __is_same_top_and_bottom(self):
        return True if self._top == self._bottom else False


class Area(AreaBase):
    def __init__(self, top: int, right: int, bottom: int, left: int, index: int=1):
        super(Area, self).__init__(top, right, bottom, left)
        self.index = index

        self.valid_area = ValidArea(self.top, self.right, self.bottom, self.left)
        self.border = None
        self.room = None

        self.border_side = NODIRECTION
        self.padding_y = ROOM_PADDING_Y
        self.padding_x = ROOM_PADDING_X

        # 分割候補の幅。分割された側に境界（b）が含まれることも考えて、必ず(margin*2+1)^2の空間が残るようにしてある。
        self.top_split_min = self.top + (self.padding_y + 2)
        self.bottom_split_max = self.bottom - (self.padding_y + 2)
        self.left_split_min = self.left + (self.padding_x + 2)
        self.right_split_max = self.right - (self.padding_x + 2)

    # TODO hとvで別々なのは単調すぎる。どこかで統一できるはず。
    def split_h(self):
        border_h = random.randint(self.top_split_min, self.bottom_split_max)

        if border_h > (self.top + self.bottom) / 2:
            top_or_bottom = 0
        else:
            top_or_bottom = 1

        if top_or_bottom == 0:
            new_area = Area(self.top, self.right, border_h - 1, self.left, self.index + 1)
            self.border_side = NORTH
            self.top = border_h
            self.border = BorderH(self.top, self.right, self.top, self.left)
            self.valid_area.top = border_h + 1

            print("split to top : border_h : {0}".format(border_h))

        elif top_or_bottom == 1:
            new_area = Area(border_h + 1, self.right, self.bottom, self.left, self.index + 1)
            self.border_side = SOUTH
            self.bottom = border_h
            self.border = BorderH(self.bottom, self.right, self.bottom, self.left)
            self.valid_area.bottom = border_h - 1

            print("split to bottom : border_h : {0}".format(border_h))

        else:
            raise Exception("split room only top or bottom!!")

        return new_area

    def split_v(self):
        border_v = random.randint(self.left_split_min, self.right_split_max)

        if border_v > (self.left + self.right) / 2:
            left_or_right = 0
        else:
            left_or_right = 1

        if left_or_right == 0:
            new_area = Area(self.top, border_v - 1, self.bottom, self.left, self.index + 1)
            self.border_side = WEST
            self.left = border_v
            self.border = BorderV(self.top, self.left, self.bottom, self.left)
            self.valid_area.left = border_v + 1

            print("split to left : border_v : {0}".format(border_v))

        elif left_or_right == 1:
            new_area = Area(self.top, self.right, self.bottom, border_v + 1, self.index + 1)
            self.border_side = EAST
            self.right = border_v
            self.border = BorderV(self.top, self.right, self.bottom, self.right)
            self.valid_area.right = border_v - 1

            print("split to right : border_v : {0}".format(border_v))

        else:
            raise Exception("split room only left or right!!")

        return new_area

    def is_splittable_v(self):
        # 要はrandintが呼び出せるか否かの判定。
        print("top_split_max : {0}, bottom_split_max : {1}".format(self.top_split_min, self.bottom_split_max))
        print("left_split_max : {0}, right_split_max : {1}".format(self.left_split_min, self.right_split_max))

        if self.left_split_min > self.right_split_max:
            return False
        else:
            return True

    def is_splittable_h(self):
        # 要はrandintが呼び出せるか否かの判定。
        print("top_split_max : {0}, bottom_split_max : {1}".format(self.top_split_min, self.bottom_split_max))
        print("left_split_max : {0}, right_split_max : {1}".format(self.left_split_min, self.right_split_max))

        if self.top_split_min > self.bottom_split_max:
            return False
        else:
            return True

    def make_plain_room(self):
        max_top = self.valid_area.bottom - (self.padding_y + 1)
        max_left = self.valid_area.right - (self.padding_x + 1)

        top = random.randint(self.valid_area.top, max_top)
        left = random.randint(self.valid_area.left, max_left)

        bottom = random.randint(top + (self.padding_y + 1), self.valid_area.bottom)
        right = random.randint(left + (self.padding_x + 1), self.valid_area.right)

        self.room = Room(top, right, bottom, left)

    def has_room(self):
        return True if self.room is not None else False

    def has_border(self):
        return True if self.border is not None else False


class DungeonGenerator(object):
    def __init__(self, size=(8, 16)):
        self.size = size
        self.map = [[NOTHING for _ in range(size[1])] for _ in range(size[0])]

        self.areas = [Area(0, size[1] - 1, size[0] - 1, 0, index=1)]
        self.routes = []

    def split_area(self, split_count: int):

        # 最初にsplitするのが縦か横か決める。
        first_v_or_h = random.randint(0, 1)

        # 分割開始。小さくなりすぎた場合終了。
        for c in range(split_count):
            print("------------c = {0} : start---------".format(c))
            current_area = self.areas[-1]

            if (c + first_v_or_h) % 2 == 0:
                if current_area.is_splittable_v():
                    new_area = current_area.split_v()
                else:
                    break
            else:
                if current_area.is_splittable_h():
                    new_area = current_area.split_h()
                else:
                    break

            self.areas.append(new_area)

            self.print_area()
            print("-------------c = {0} : end------------".format(c))

    def print_map(self):
        for area in self.areas:
            if area.has_room():
                room = area.room
                for y in range(room.top, room.top + room.height):
                    for x in range(room.left, room.left + room.width):
                        self.map[y][x] = room.map[y - room.top][x - room.left]

            if area.has_border():
                for y in range(area.border.height):
                    for x in range(area.border.width):
                        self.map[y + area.border.top][x + area.border.left] = ROUTE_CANDIDATE

        for route in self.routes:
            for y, x in route.route_positions:
                self.map[y][x] = ROUTE

        self._print_nested_integer_list(self.map)

    def print_area(self):
        area_map = [['.' for _ in range(self.size[1])] for _ in range(self.size[0])]

        for area in self.areas:
            t = area.top if not area.border_side == NORTH else area.top + 1
            r = area.right if not area.border_side == EAST else area.right - 1
            b = area.bottom if not area.border_side == SOUTH else area.bottom - 1
            l = area.left if not area.border_side == WEST else area.left + 1

            for y in range(t, b + 1):
                for x in range(l, r + 1):
                    area_map[y][x] = area.index

        self._print_nested_integer_list(area_map)

    @staticmethod
    def _print_nested_integer_list(nested_integer_list: list):
        rows = ["".join([str(integer) for integer in row]) for row in nested_integer_list]
        print_data = "\n".join(rows)
        print(print_data)

    def make_room(self):
        for area in self.areas:
            area.make_plain_room()

    def make_route(self):
        for parent_area, child_area in zip(self.areas, self.areas[1:]):
            new_route = Route(parent_area, child_area)
            self.routes.append(new_route)
            new_route.make_route()


if __name__ == '__main__':
    # random.seed(51)
    # dg = DungeonGenerator()

    dg = DungeonGenerator((40, 80))

    dg.split_area(10)

    print("------------make room------------")
    dg.make_room()
    dg.print_map()

    print("------------make route------------")
    dg.make_route()
    dg.print_map()

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
