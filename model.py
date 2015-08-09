#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")

from abc import ABCMeta, abstractmethod
import warnings

from position import PositionAndDirection
import observer
import turn
import npcai


# TODO シーンの管理者が必要。Observerの作成者はこいつに任せる予定。
# TODO MessageModelとMessageViewを用意したいが、Heroが二つもオブジェクトを持つ必要があるなあ。
# TODO Floorが上下左右のFloorをチェックして、iconを変えるようにしたいなあ
# TODO save関連はCSVモジュールを使うといいかもね。当分先の話。


class HOSTILITY(object):
    friend = 0
    neutral = 1
    hostile = 2


class MapModel(observer.Subject):
    # TODO dungeon_generatorとの連携を急げ

    def __init__(self, size: (int, int)):
        observer.Subject.__init__(self)
        (self.height, self.width) = size

        self.message = ''
        self.floor_objects = []
        self.obstacle_objects = []

        self._init_floor_objects()
        self.make_map_edge()

    def _init_floor_objects(self):
        p_and_ds = (PositionAndDirection((y, x)) for y in range(self.height) for x in range(self.width))
        floors = (Floor(self, p_and_d) for p_and_d in p_and_ds)
        self.floor_objects.extend(floors)

    def make_map_edge(self):
        # リスト内包表記は内側のforであるほど、後（右）に書かれることに注意しよう。条件も同様に内側が後。
        edge_y_x = ([y, x] for y in range(self.height) for x in range(self.width)
                    if y == 0 or y == self.height - 1
                    or x == 0 or x == self.width - 1)
        edge_p_and_d = (PositionAndDirection(pos) for pos in edge_y_x)
        walls = (Wall(self, p_and_d) for p_and_d in edge_p_and_d)

        self.obstacle_objects.extend(walls)

    def clear_message(self):
        self.message = ""

    def is_empty_place_at(self, position):
        obstacles_positions = [obje.get_position() for obje in self.obstacle_objects]
        return position not in obstacles_positions

    def interact(self, people: "Character"):
        object_front_position = people.get_front_position()
        interact_object = self.get_map_object_at(object_front_position)

        self.set_message(interact_object, interact_object.comment)
        self.notify()

    def get_map_object_at(self, position):
        obstacle_obje = next(
            (obje for obje in self.obstacle_objects if obje.get_position() == position),
            None
        )

        if obstacle_obje:
            return obstacle_obje

        floor_obje = next((obje for obje in self.floor_objects if obje.get_position() == position), None)
        if floor_obje:
            return floor_obje

        raise Exception("map is collapsed!!!!")

    def get_character_at(self, position):
        # 条件に沿うオブジェクトをリストから高速にサーチする方法。
        # 条件に沿う最初のオブジェクトのみを返す。
        return next(
            (obje for obje in self.obstacle_objects
             if obje.get_position() == position and isinstance(obje, Character)),
            None)

    def set_message(self, map_object: "MapObject", message: str):
        self.message = "{0} >{1}".format(map_object.pose_icon, message)

    def register_obstacle(self, obstacle_object: "ObstacleObject"):
        self.obstacle_objects.append(obstacle_object)

        self.set_message(obstacle_object, "resister {0}".format(obstacle_object.get_position()))
        self.notify()

    def remove_obstacle(self, obstacle_object: "ObstacleObject"):
        self.obstacle_objects.remove(obstacle_object)
        logging.info("remove obstacle_object")

        self.set_message(obstacle_object, "remove {0}".format(obstacle_object.get_position()))
        # self.notify()


class BattleField(object):
    def __init__(self, map_model: "MapModel", attacker: "Character"):
        self.map_model = map_model
        self.attacker = attacker

    def attack_to(self, position):
        defender = self.map_model.get_character_at(position)

        if defender is not None:
            self._battle(defender)
            self.attacker.throw_message("attack to {0} : {1}".format(defender.pose_icon, position))
        else:
            self.attacker.throw_message("Oops! No one is in front of me. : {0}".format(position))

    def _battle(self, defender: "Character"):
        atk_str = self.attacker.parameter.strength
        def_tou = defender.parameter.toughness

        logging.info("atk_str : {0}".format(atk_str))
        logging.info("def_tou : {0}".format(def_tou))

        damage = atk_str - def_tou
        damage = damage if damage > 0 else 0
        logging.info("damage : {0}".format(damage))

        defender.parameter.hp -= damage
        logging.info("defender hp : {0}".format(defender.parameter.hp))

        if defender.is_died():
            defender.die()
            logging.info("die!!")


# 全てのマップオブジェクトの基本となるクラス
class MapObject(object):
    pose_icon = ' '
    comment = "ERROR!! I'm Map_Object."

    def __init__(self, map_model: "MapModel", pos_and_dir: "PositionAndDirection"):
        self.map_model = map_model
        self.pos_and_dir = pos_and_dir

        self.icon = self.pose_icon

    def get_position(self):
        return self.pos_and_dir.get_position()


# 通行不可のマップオブジェクト
class ObstacleObject(MapObject):
    comment = "ERROR!! I'm Obstacle_Object."

    @staticmethod
    def is_obstacle():
        return True


# 通行可能なマップオブジェクト
class NonObstacleObject(MapObject):
    comment = "ERROR!! I'm Non_Obstacle_Object."

    @staticmethod
    def is_obstacle():
        return False


class Floor(NonObstacleObject):
    pose_icon = '.'
    comment = "It's a floor."


class Wall(ObstacleObject):
    pose_icon = '='
    comment = "It's a wall."


class Character(ObstacleObject, observer.Subject, metaclass=ABCMeta):
    pose_icon = 'P'
    comment = "It's a Character"
    direction_icons = ['P'] * 4

    def __init__(self, map_model: "MapModel",
                 pos_and_dir: "PositionAndDirection",
                 parameter: "Parameter",
                 turn_manager: "turn.TurnManager"):
        super(Character, self).__init__(map_model, pos_and_dir)
        self.turn_manager = turn_manager

        self.parameter = parameter

        observer.Subject.__init__(self)

    def run(self):
        front_position = self.pos_and_dir.get_front_position()

        dir_word = self.pos_and_dir.get_direction_by_word()
        if self.map_model.is_empty_place_at(front_position):
            self.pos_and_dir.run()
            self.throw_message("move to {0}".format(dir_word))
        else:
            self.throw_message("Ouch!! Obstacle is at {0}.".format(dir_word))

        self._end_turn()

    def move_north(self):
        self.pos_and_dir.turn_north()
        self._update_icon()
        self.run()

    def move_east(self):
        self.pos_and_dir.turn_east()
        self._update_icon()
        self.run()

    def move_south(self):
        self.pos_and_dir.turn_south()
        self._update_icon()
        self.run()

    def move_west(self):
        self.pos_and_dir.turn_west()
        self._update_icon()
        self.run()

    def attack_front(self):
        bf = BattleField(self.map_model, self)
        bf.attack_to(self.get_front_position())

        self._end_turn()

    def throw_message(self, message: str):
        self.map_model.set_message(self, message)

    def _update_icon(self):
        self.icon = self.direction_icons[self.pos_and_dir.direction]

    def get_front_position(self):
        return self.pos_and_dir.get_front_position()

    def get_direction(self):
        return self.pos_and_dir.direction

    def get_icon(self):
        return self.icon

    def get_fov_distance(self):
        return self.parameter.fov_distance

    def is_died(self):
        return True if self.parameter.hp <= 0 else False

    def die(self):
        self.map_model.remove_obstacle(self)
        # self.turn_manager.queue
        del self

        logging.info("delete self")

    @abstractmethod
    def _end_turn(self):
        raise Exception("Not implemented!!")


class Villager(Character):
    pose_icon = "V"
    direction_icons = ['V'] * 4

    def __init__(self,
                 map_model: "MapModel",
                 pos_and_dir: "PositionAndDirection",
                 parameter: "Parameter",
                 turn_manager: "turn.TurnManager",
                 comment: str="hoge"
                 ):
        super().__init__(map_model, pos_and_dir, parameter, turn_manager)
        self.comment = comment

        self.ai = npcai.VillagerAI(map_model, self)
        self.turn_queue_entry = None
        """:type : turn.TurnQueueEntryBase"""

        self.hostility = HOSTILITY.neutral

    def do_nothing(self):
        logging.debug("{0}".format(self))
        self._end_turn()

    def die(self):
        super(Villager, self).die()
        self.turn_manager.remove(self.turn_queue_entry)
        logging.info("removed turn_queue_entry")

    def _end_turn(self):
        logging.info("Villager")

        queue_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(
            self.ai,
            self.parameter.turn_period
        )
        self.turn_manager.register(queue_entry)
        self.turn_queue_entry = queue_entry


class Enemy(Character):
    pose_icon = "E"
    direction_icons = ['E'] * 4

    def __init__(self,
                 map_model: "MapModel",
                 pos_and_dir: "PositionAndDirection",
                 parameter: "Parameter",
                 turn_manager: "turn.TurnManager",
                 comment: str="I'm enemy."
                 ):
        super().__init__(map_model, pos_and_dir, parameter, turn_manager)
        self.comment = comment

        self.ai = npcai.EnemyAI(map_model, self)
        self.turn_queue_entry = None
        """:type : turn.TurnQueueEntryBase"""

        self.hostility = HOSTILITY.hostile

    def do_nothing(self):
        logging.debug("{0}".format(self))
        self._end_turn()

    def die(self):
        super(Enemy, self).die()
        self.turn_manager.remove(self.turn_queue_entry)
        logging.info("removed turn_queue_entry")

    def _end_turn(self):
        queue_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(
            self.ai,
            self.parameter.turn_period
        )
        self.turn_manager.register(queue_entry)
        self.turn_queue_entry = queue_entry


class Hero(Character):
    pose_icon = '@'
    direction_icons = ['^', '>', 'v', '<']

    def __init__(self, map_model: "MapModel", pos_and_dir: "PositionAndDirection", parameter: "Parameter",
                 turn_manager: "turn.TurnManager"):
        super().__init__(map_model, pos_and_dir, parameter, turn_manager)

        self.hostility = HOSTILITY.friend

    # TODO これも本来はCharacterクラスにあるべき。しかし、NPCがNPCとinteractする処理がまだ定義できない…。
    def interact_to_front(self):
        self.map_model.interact(self)
        self._end_turn()

    def _end_turn(self):
        queue_entry = turn.TurnQueueEntryFactory.make_hero_turn_queue(
            self._observers[0],  # FIXME 怪しすぎるコード。observerでいいのか考え直そう。observersを投げて処理すれば良いんでね?
            self.parameter.turn_period
        )
        self.turn_manager.register(queue_entry)


import json
import os

# TODO どこかで設定用の変数を集めたファイルが必要だ。
PARAMETERS_DIRECTORY = os.path.join("parameters")


class ParameterFactory(object):
    @staticmethod
    def make_hero():
        file_name = "default_hero_000.json"
        return ParameterFactory._load_parameter(file_name)

    @staticmethod
    def make_villager():
        file_name = "default_villager_000.json"
        return ParameterFactory._load_parameter(file_name)

    @staticmethod
    def make_enemy():
        file_name = "default_enemy_000.json"
        return ParameterFactory._load_parameter(file_name)

    @staticmethod
    def _load_parameter(file_name):
        file_path = os.path.join(PARAMETERS_DIRECTORY, file_name)

        with open(file_path, mode='r', encoding="utf-8") as f:
            parameter_json = json.load(f)

        return ParameterFactory._make_parameter_from_json(parameter_json)

    @staticmethod
    def _make_parameter_from_json(json_parameter):
        parameter = Parameter(**json_parameter)

        return parameter


# TODO 敵対状態かどうかの設定がいる。
class Parameter(object):
    def __init__(self,
                 hp: int=100,
                 mp: int=50,
                 strength: int=20,
                 toughness: int=10,
                 turn_period: int=5,
                 fov_distance: int=5):
        self.hp = hp
        self.mp = mp

        self.strength = strength
        self.toughness = toughness

        self.turn_period = turn_period

        self.fov_distance = fov_distance

    # noinspection PyMethodMayBeStatic
    def load_parameter(self):
        warnings.warn("not implemented", Warning)


if __name__ == '__main__':
    para = ParameterFactory.make_hero()
    logging.debug(para)
    logging.debug(para.__dict__)
    para_v = ParameterFactory.make_villager()
    logging.debug(para_v)
    logging.debug(para_v.__dict__)


    class HHH(object):
        def __init__(self, abc):
            self.abc = abc
            self.pos_and_dir = PositionAndDirection([2, 2], 0)


    hhh = HHH("fjoijio")

    aho = list()
    aho.append(1)
    aho.append(hhh)
    aho.append('c')

    logging.debug(aho)
    del hhh
    # print(hhh.abc)
