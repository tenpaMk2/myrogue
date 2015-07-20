#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")

from abc import ABCMeta, abstractmethod
import model


class AIBase(metaclass=ABCMeta):
    def __init__(self, map_model: "model.MapModel"):
        self.map_model = map_model

    @abstractmethod
    def act(self):
        pass


class VillagerAI(AIBase):
    def __init__(self, map_model: "model.MapModel", villager: "model.Villager"):
        super(VillagerAI, self).__init__(map_model)
        self.villager = villager

    def act(self):
        # ここにAIのロジック
        # とりあえず今は何もしない。
        self.villager.do_nothing()


class EnemyAI(AIBase):
    def __init__(self, map_model: "model.MapModel", enemy: "model.Enemy"):
        super(EnemyAI, self).__init__(map_model)
        self.enemy = enemy

    def act(self):
        # ここにAIのロジック
        # とりあえず今は何もしない。
        self.enemy.do_nothing()
