#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")

from abc import ABCMeta, abstractmethod
import model
import astar


# TODO やっぱりちゃんと2次元リストをクラス定義した方が良さそう。[y][x]とかやってると絶対ミスする。

class STATE(object):
    stop = 0
    wander = 1
    chase = 2
    escape = 3


class AIBase(metaclass=ABCMeta):
    def __init__(self, map_model: "model.MapModel"):
        self.map_model = map_model
        self.state = STATE.stop

    @abstractmethod
    def act(self):
        if self.state == STATE.stop:
            self.stop()
        elif self.state == STATE.wander:
            self.wander()
        elif self.state == STATE.chase:
            self.chase()
        elif self.state == STATE.escape:
            self.escape()
        else:
            raise Exception("Invalid STATE!")

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def wander(self):
        pass

    @abstractmethod
    def chase(self):
        pass

    @abstractmethod
    def escape(self):
        pass


class VillagerAI(AIBase):
    def __init__(self, map_model: "model.MapModel", villager: "model.Villager"):
        super(VillagerAI, self).__init__(map_model)
        self.state = STATE.stop

        self.villager = villager

    def act(self):
        super(VillagerAI, self).act()

    def stop(self):
        logging.info("VillagerAI")
        self.villager.do_nothing()

    def wander(self):
        logging.info("VillagerAI")
        self.villager.do_nothing()

    def chase(self):
        logging.info("VillagerAI")
        self.villager.do_nothing()

    def escape(self):
        logging.info("VillagerAI")
        self.villager.do_nothing()


class EnemyAI(AIBase):
    def __init__(self, map_model: "model.MapModel", enemy: "model.Enemy"):
        super(EnemyAI, self).__init__(map_model)
        self.state = STATE.wander

        self.enemy = enemy

    def act(self):
        super(EnemyAI, self).act()

    def stop(self):
        logging.info("EnemyAI")
        self.enemy.do_nothing()

    def wander(self):
        logging.info("EnemyAI")

        parsed_map = self.return_map_for_astr()
        searching_map = astar.SearchingMap(parsed_map)
        logging.info("made searching_map")

        ast = astar.Astar(searching_map)
        next_position = ast.get_next_position()
        logging.info("next position is %r", next_position)

        y_n, x_n = next_position
        y_e, x_e = self.enemy.get_position()
        if [y_e, x_e] == [y_n + 1, x_n]:
            self.enemy.move_north()
        elif [y_e, x_e] == [y_n, x_n - 1]:
            self.enemy.move_east()
        elif [y_e, x_e] == [y_n - 1, x_n]:
            self.enemy.move_south()
        elif [y_e, x_e] == [y_n, x_n + 1]:
            self.enemy.move_west()
        else:
            self.enemy.do_nothing()

    def chase(self):
        logging.info("EnemyAI")
        self.enemy.do_nothing()

    def escape(self):
        logging.info("EnemyAI")
        self.enemy.do_nothing()

    def return_map_for_astr(self):
        height = self.map_model.height
        width = self.map_model.width

        # 床と壁の追加
        parsed_map = astar.SearchingMap.make_empty_map(height, width, astar.MAP.nothing)
        for obs in self.map_model.obstacle_objects:
            y, x = obs.get_position()
            parsed_map.set_value_at(y, x, astar.MAP.wall)

        # スタート（自分の位置）の追加
        y_s, x_s = self.enemy.get_position()
        parsed_map.set_value_at(y_s, x_s, astar.MAP.start)

        # ゴール（Heroの位置）の追加
        # FIXME Heroの位置を知らなければいけない
        # FIXME GとSが同じ座標になる場合がある。
        parsed_map.set_value_at(1, 1, astar.MAP.goal)

        return parsed_map
