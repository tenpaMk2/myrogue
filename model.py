#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

from position import PositionAndDirection
import observer
import turn

# TODO シーンの管理者が必要。Observerの作成者はこいつに任せる予定。
# TODO MessageModelとMessageViewを用意したいが、Heroが二つもオブジェクトを持つ必要があるなあ。
# TODO Floorが上下左右のFloorをチェックして、iconを変えるようにしたいなあ
# TODO Okmrさんに言われた通り、HeroのMove系メソッドはupdateを伴うので親クラスと違う名前にしよう。
# TODO save関連はCSVモジュールを使うといいかもね。当分先の話。

# TODO MapModelもSubjectを多重継承するようにしよう
class MapModel(observer.Subject):
    # TODO make_roomを実装し、make_map_edgeをinit_map_edgeからmake_roomを呼び出すようにしよう

    def __init__(self, size: (int, int)):
        observer.Subject.__init__(self)
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
        self.notify()

    def get_map_object_by_position(self, position: "PositionAndDirection"):
        for obstacle in self.obstacle_list:
            if position == obstacle.get_position():
                return obstacle

        for flo in self.floor_list:
            if position == flo.get_position():
                return flo

        raise Exception("map is collapsed!!!!")

    def set_message(self, map_object: "MapObject", message: str):
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
        self.notify()


# 全てのマップオブジェクトの基本となるクラス
class MapObject(object):
    pose_icon = ' '
    comment = "ERROR!! I'm Map_Object."

    def __init__(self, map_model: "MapModel", pos_and_dir: "PositionAndDirection"):
        self.map_model = map_model
        self.pos_and_dir = pos_and_dir

        self.icon = self.pose_icon

        # TODO 既にこの座標にオブジェクトが存在していないかチェック。

    def get_position(self):
        return self.pos_and_dir.get_position()


# TODO isObstacleの名称はまずいか? 変数とメソッドの区別がつかない。
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
    pose_icon = '='
    comment = "It's a wall."


# FIXME HeroとVillagerで共通する部分を抜き出しつつ、それぞれ個別に処理する所はきっちり分けれるようにしたい。
class People(ObstacleObject, observer.Subject):
    pose_icon = 'P'
    comment = "It's a people."
    turn_period = 5  # FIXME パラメータの概念をそろそろ導入しないと

    def __init__(self,
                 map_model: "MapModel",
                 pos_and_dir: "PositionAndDirection",
                 turn_manager: "turn.TurnManager"):
        super().__init__(map_model, pos_and_dir)
        self.turn_manager = turn_manager

        observer.Subject.__init__(self)

    def run(self):
        front_position = self.pos_and_dir.get_front_position()

        dir_word = self.pos_and_dir.get_direction_by_word()
        if self.map_model.is_empty_place_at(front_position):
            self.pos_and_dir.run()
            self.throw_message("move to {0}".format(dir_word))
        else:
            self.throw_message("Ouch!! Obstacle is at {0}.".format(dir_word))

    def move_north(self):
        self.pos_and_dir.turn_north()
        self.run()

    def move_east(self):
        self.pos_and_dir.turn_east()
        self.run()

    def move_south(self):
        self.pos_and_dir.turn_south()
        self.run()

    def move_west(self):
        self.pos_and_dir.turn_west()
        self.run()

    def throw_message(self, message: str):
        self.map_model.set_message(self, message)

    def get_front_position(self):
        return self.pos_and_dir.get_front_position()

    def get_direction(self):
        return self.pos_and_dir.direction

    def get_icon(self):
        return self.icon


class Villager(People):
    pose_icon = "V"

    def __init__(self, map_model: MapModel, pos_and_dir: "PositionAndDirection", turn_manager: "turn.TurnManager",
                 comment: str="hoge"):
        super().__init__(map_model, pos_and_dir, turn_manager)
        self.comment = comment
        self.ai = AI(self, map_model)

    def get_comment(self):
        return self.comment

    def do_nothing(self):
        print("do_nothing:{0}".format(self))
        self.__end_turn()

    def __end_turn(self):
        queue_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(
            self.ai,
            self.turn_period
        )
        self.turn_manager.register(queue_entry)


class Hero(People, observer.Subject):
    pose_icon = '@'
    direction_icon_list = ['^', '>', 'v', '<']
    turn_period = 2  # FIXME パラメータの概念をそろそろ導入しないと

    def update_icon(self):
        self.icon = self.direction_icon_list[self.pos_and_dir.direction]

    def run(self):
        super().run()
        self.update_icon()
        self.__end_turn()

    def interact_to_front(self):
        self.map_model.interact(self)
        self.__end_turn()

    def __end_turn(self):
        queue_entry = turn.TurnQueueEntryFactory.make_hero_turn_queue(
            self._observers[0],
            self.turn_period
        )
        self.turn_manager.register(queue_entry)

# TODO 例えばactで右に動くようにしたとき、現状はターンエンド処理が入らない。根本的に見直さないと。
class AI(object):
    def __init__(self, villager: "Villager", map_model: "MapModel"):
        self.villager = villager
        self.map_model = map_model

    def act(self):
        # ここにAIのロジック
        # とりあえず今は何もしない。
        self.villager.do_nothing()




