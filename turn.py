#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import observer

# TODO queueが空の場合のIndexErrorを対処した方が良いかも?

class TurnManager(object):
    def __init__(self):
        self.queue = []
        self.total_turn_count = 0

    def register(self, turn_queue_entry: "TurnQueueEntry"):
        # まずは追加。その後に次回ターンまでの時間でソートする。
        self.queue.append(turn_queue_entry)
        self.queue.sort(key=lambda x: x.next_turn_time)

    def update(self):
        current_entry = self.queue.pop(0)
        spent_time = current_entry.next_turn_time

        self.__decrease_turn_time(spent_time)

        print("start_turn:", current_entry)
        current_entry.start_turn()

    def __decrease_turn_time(self, decreasing_time: int):
        for entry in self.queue:
            entry.decrease_turn_time(decreasing_time)

    def _print_queue(self):
        print("<-----queue----->")
        for entry in self.queue:
            print("remain time = {0}: {1}: {2}".format(entry.next_turn_time, entry, entry.observer.__dict__))

class TurnQueueEntry(object):
    def __init__(self, observer: "observer.Observer", turn_period: int):
        self.observer = observer
        self.next_turn_time = turn_period

    def decrease_turn_time(self, decreasing_time: int):
        self.next_turn_time -= decreasing_time

    def start_turn(self):
        self.observer.update_turn_start()


class TurnQueueEntryFactory(object):
    @staticmethod
    def make_hero_turn_queue(observer: "observer.Observer", turn_period: int):
        return TurnQueueEntry(observer, turn_period)

    # FIXME 今の所は同じ実装だが、後々別れるかもしれない。ま、Observerの方で区別つけるのが適切だと思うけどね。
    @staticmethod
    def make_npc_turn_queue(observer: "observer.Observer", turn_period: int):
        return TurnQueueEntry(observer, turn_period)


if __name__ == "__main__":
    class TestObserver(object):
        def __init__(self, name: str="hoge"):
            self.name = name

        def update_turn_start(self):
            print("---next turn---")
            print(self.name)
            print('')

    tm = TurnManager()

    hero_entry = TurnQueueEntryFactory.make_hero_turn_queue(TestObserver("I'm Hero."), 2)
    villager_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestObserver("I'm Villager."), 23)
    sonchou_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestObserver("私が村長です。"), 23)
    enemy_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestObserver("I'm Enemy."), 12)
    boss_entry = TurnQueueEntryFactory.make_npc_turn_queue(TestObserver("I'm Boss."), 33)

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
