#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import observer
from abc import ABCMeta, abstractmethod

# TODO queueが空の場合のIndexErrorを対処した方が良いかも?

class TurnManager(object):
    def __init__(self):
        self.queue = []
        self.total_turn_count = 0

    def register(self, turn_queue_entry: "TurnQueueEntryBase"):
        # まずは追加。その後に次回ターンまでの時間でソートする。
        self.queue.append(turn_queue_entry)
        self.queue.sort(key=lambda x: x.next_turn_time)

    def update(self):
        current_entry = self.queue.pop(0)
        spent_time = current_entry.next_turn_time

        self._decrease_turn_time(spent_time)

        print("start_turn:", current_entry)
        current_entry.start_turn()

    def _decrease_turn_time(self, decreasing_time: int):
        for entry in self.queue:
            entry.decrease_turn_time(decreasing_time)

    def _print_queue(self):
        print("<-----queue----->")
        for entry in self.queue:
            print("remain time = {0}: {1}".format(entry.next_turn_time, entry))


class TurnQueueEntryBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, turn_period: int):
        self.next_turn_time = turn_period

    def decrease_turn_time(self, decreasing_time: int):
        self.next_turn_time -= decreasing_time

    @abstractmethod
    def start_turn(self):
        pass


class HeroTurnQueueEntry(TurnQueueEntryBase):
    def __init__(self, observer: "observer.ObserverBase", turn_period: int):
        super(HeroTurnQueueEntry, self).__init__(turn_period)
        self.observer = observer

    def start_turn(self):
        self.observer.update_turn_start()


class NPCTurnQueueEntry(TurnQueueEntryBase):
    def __init__(self, ai: "model.AI", turn_period: int):
        super(NPCTurnQueueEntry, self).__init__(turn_period)
        self.ai = ai

    def decrease_turn_time(self, decreasing_time: int):
        self.next_turn_time -= decreasing_time

    def start_turn(self):
        self.ai.act()


class TurnQueueEntryFactory(object):
    @staticmethod
    def make_hero_turn_queue(observer: "observer.ObserverBase", turn_period: int):
        return HeroTurnQueueEntry(observer, turn_period)

    @staticmethod
    def make_npc_turn_queue(ai: "model.AI", turn_period: int):
        return NPCTurnQueueEntry(ai, turn_period)


if __name__ == "__main__":
    class TestObserver(observer.ObserverBase):
        def __init__(self, name: str="hoge"):
            self.name = name

        def update(self):
            pass

        def update_turn_start(self):
            print("---current Hero turn---")
            print(self.name)
            print('')

    class TestAI(object):
        def __init__(self, name: str="AI"):
            self.name = name

        def act(self):
            print("---current NPC turn---")
            print(self.name)
            print('')

    tm = TurnManager()

    hero_entry = TurnQueueEntryFactory.make_hero_turn_queue(TestObserver("I'm Hero."), 2)
    villager_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestAI("I'm Villager."), 23)
    sonchou_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestAI("私が村長です。"), 23)
    enemy_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestAI("I'm Enemy."), 12)
    boss_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestAI("I'm Boss."), 33)

    tm.register(hero_entry)
    tm.register(villager_entry)
    tm.register(sonchou_entry)
    tm.register(enemy_entry)
    tm.register(boss_entry)

    tm._print_queue()

    tm.update()
    tm._print_queue()
    tm.update()
    tm._print_queue()
    tm.update()
    tm._print_queue()
    tm.update()
    tm._print_queue()
