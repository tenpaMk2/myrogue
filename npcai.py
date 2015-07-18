#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

from abc import ABCMeta, abstractmethod
import model


class AIBase(metaclass=ABCMeta):
    @abstractmethod
    def act(self):
        pass


class VillagerAI(AIBase):
    def __init__(self, villager: "model.Villager", map_model: "model.MapModel"):
        self.villager = villager
        self.map_model = map_model

    def act(self):
        # ここにAIのロジック
        # とりあえず今は何もしない。
        self.villager.do_nothing()
