#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod

__author__ = 'tenpa'


class AIBase(metaclass=ABCMeta):
    @abstractmethod
    def act(self):
        pass


class VillagerAI(AIBase):
    def __init__(self, villager: "Villager", map_model: "MapModel"):
        self.villager = villager
        self.map_model = map_model

    def act(self):
        # ここにAIのロジック
        # とりあえず今は何もしない。
        self.villager.do_nothing()