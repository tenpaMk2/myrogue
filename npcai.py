#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")

from abc import ABCMeta, abstractmethod
import warnings
import model
import astar
import shadowcasting


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


# TODO FOVとastarを組み合わせて、Heroを追跡、攻撃するようにしよう。
# TODO searchメソッドがいるのかな?
class EnemyAI(AIBase):
    def __init__(self, map_model: "model.MapModel", enemy: "model.Enemy"):
        super(EnemyAI, self).__init__(map_model)
        self.state = STATE.stop

        self.enemy = enemy

        self.target_pos = None

    def act(self):
        super(EnemyAI, self).act()

    def stop(self):
        logging.info("EnemyAI")

        nearest_target_pos = self._get_nearest_target_pos()

        if self._is_in_fov(nearest_target_pos):
            logging.info("change mode : chase")
            self.state = STATE.chase
            self.target_pos = nearest_target_pos
            self.enemy.do_nothing()
        else:
            logging.info("Hero not found")
            self.enemy.do_nothing()

    def wander(self):
        logging.info("EnemyAI")
        self.enemy.do_nothing()

    def chase(self):
        logging.info("EnemyAI")

        self.target_pos = self._get_nearest_target_pos()
        logging.info("target_pos : %r", self.target_pos)

        ast = self._make_ast()
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
        # FIXME GとSが同じ座標になる場合がある。
        y_t, x_t = self.target_pos
        parsed_map.set_value_at(y_t, x_t, astar.MAP.goal)

        return parsed_map

    def return_map_for_fov(self):
        height = self.map_model.height
        width = self.map_model.width

        # 床と壁の追加
        parsed_map = shadowcasting.MAPParser.make_empty_map(height, width, shadowcasting.MAP.nothing)
        for obs in self.map_model.obstacle_objects:
            y, x = obs.get_position()
            parsed_map.set_value_at(y, x, shadowcasting.MAP.wall)

        return parsed_map

    def _get_nearest_target(self) -> "model.Character":
        y_e, x_e = self.enemy.get_position()

        # FIXME これもユーティリティモジュールに分けたほうが良さそう。
        calculate_euclid_square_distance = lambda chara: \
            (chara.get_position()[0] - y_e) ^ 2 + (chara.get_position()[1] - x_e) ^ 2

        return min(self.map_model.get_characters_by_hostility(model.HOSTILITY.friend),
                   key=calculate_euclid_square_distance)

    def _is_in_fov(self, target_pos: list):
        fov = self._make_fov()

        y_e, x_e = self.enemy.get_position()
        fov.do_fov(y_e, x_e, self.enemy.get_fov_distance())

        return fov.is_in_fov(*target_pos)

    def _make_fov(self):
        parsed_map = self.return_map_for_fov()
        return shadowcasting.FOVMap(parsed_map)

    def _get_nearest_target_pos(self):
        nearest_target = self._get_nearest_target()

        if nearest_target:
            return nearest_target.get_position()
        else:
            warnings.warn("No nearest target!!")
            return None

    def _make_ast(self):
        parsed_map = self.return_map_for_astr()
        searching_map = astar.SearchingMap(parsed_map)
        logging.info("made searching_map")

        return astar.Astar(searching_map)
