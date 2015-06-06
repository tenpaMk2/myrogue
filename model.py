#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

from position import PositionAndDirection



class MapModel(object):
    # TODO make_roomを実装し、make_map_edgeをinit_map_edgeからmake_roomを呼び出すようにしよう

    def __init__(self, size: (int, int)):
        (self.height, self.width) = size
        self.message = ''

        self.floor_list = []
        self.obstacle_list = []

        self.__init_floor_list()
        self.make_map_edge()

    def __init_floor_list(self):
        for y in range(self.height):
            for x in range(self.width):
                pos_and_dir = PositionAndDirection([y, x])
                self.floor_list.append(Floor(self, pos_and_dir))

    def clear_message(self):
        self.message = ""

    def is_empty_place_at(self, position: "PositionAndDirection"):
        obstacle_position_list = [obje.get_position() for obje in self.obstacle_list]
        return position not in obstacle_position_list

    def interact(self, people: "People"):
        object_front_position = people.get_front_position()
        interact_object = self.get_map_object_by_position(object_front_position)
        self.set_message(interact_object, interact_object.comment)
        # self.draw_map()

    def get_map_object_by_position(self, position: "PositionAndDirection"):
        for obstacle in self.obstacle_list:
            if position == obstacle.get_position():
                return obstacle

        for flo in self.floor_list:
            if position == flo.get_position():
                return flo

        raise Exception("map is collapsed!!!!")

    def set_message(self, map_object, message: str):
        self.message = "{0} >{1}".format(map_object.pose_icon, message)

    def make_map_edge(self):
        for y in range(self.height):
            for x in range(self.width):
                if y == 0 or y == self.height - 1 or x == 0 or x == self.width - 1:
                    pos_and_dir = PositionAndDirection([y, x])
                    self.obstacle_list.append(Wall(self, pos_and_dir))

    def resister_map_object(self, map_object: "MapObject"):
        self.obstacle_list.append(map_object)

        self.set_message(map_object, "resister {0}".format(map_object.get_position()))
        # self.draw_map()


# 全てのマップオブジェクトの基本となるクラス
class MapObject(object):
    pose_icon = ' '
    comment = "ERROR!! I'm Map_Object."

    def __init__(self, dq_map: "MapModel", pos_and_dir: PositionAndDirection):
        self.dq_map = dq_map
        self.position_and_direction = pos_and_dir
        self.icon = self.pose_icon

    def get_position(self):
        return self.position_and_direction.get_position()


# 通行不可のマップオブジェクト
class ObstacleObject(MapObject):
    isObstacle = True
    comment = "ERROR!! I'm Obstacle_Object."


# 通行可能なマップオブジェクト
class NonObstacleObject(MapObject):
    isObstacle = False
    comment = "ERROR!! I'm Non_Obstacle_Object."


class Floor(NonObstacleObject):
    pose_icon = '.'
    comment = "It's a floor."


class Wall(ObstacleObject):
    isObstacle = True
    pose_icon = '='
    comment = "It's a wall."


class People(ObstacleObject):
    isObstacle = True
    pose_icon = 'P'
    comment = "It's a people."

    def __init__(self, dq_map: "MapModel", pos_and_dir: "PositionAndDirection"):
        super().__init__(dq_map, pos_and_dir)
        self.dq_map = dq_map
        self.position_and_direction = pos_and_dir

        # TODO マップの中で、立ってて大丈夫な場所なのかどうかチェック

    def move_to(self, direction: int):
        # directionの方向の座標を取得
        self.position_and_direction.set_direction(direction)
        front_position = self.position_and_direction.get_front_position()

        if self.dq_map.is_empty_place_at(front_position):
            self.position_and_direction.move_towards(direction)
            self.throw_message("move to {0}".format(direction))
        else:
            self.throw_message("Ouch!! {0} is obstacle.".format(direction))

    def throw_message(self, message: str):
        self.dq_map.set_message(self, message)

    def get_front_position(self):
        return self.position_and_direction.get_front_position()

    def get_position_y(self):
        return self.position_and_direction.get_position_y()

    def get_position_x(self):
        return self.position_and_direction.get_position_x()

    def get_direction(self):
        return self.position_and_direction.get_direction()

    def get_icon(self):
        return self.icon


class Villager(People):
    pose_icon = "V"

    def __init__(self, dq_map: "MapModel", pos_and_dir: PositionAndDirection, comment="__init__"):
        super().__init__(dq_map, pos_and_dir)
        self.comment = comment

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment: str):
        if not isinstance(comment, str):
            raise TypeError("comment must be strings")
        self._comment = comment

    def get_response(self):
        return self.comment


class Hero(People):
    pose_icon = '@'
    direction_icon_list = ['v', '>', '^', '<']

    def move_to(self, direction: int):
        super().move_to(direction)

        self.update_icon()
        # self.dq_map.draw_map()

    def update_icon(self):
        self.icon = self.direction_icon_list[self.position_and_direction.get_direction()]

    def run(self):
        self.move_to(self.get_direction())

    def interact_to_front(self):
        self.dq_map.interact(self)


if __name__ == "__main__":
    map_model = MapModel([5, 20])


