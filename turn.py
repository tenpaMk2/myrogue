#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

# TODO queueが空の場合のIndexErrorを対処した方が良いかも?

class TurnManager(object):
    def __init__(self):
        self.queue = []
        self.total_turn_count = 0

    def register(self, next_turn_time: int, callable_obje):
        # まずは追加。その後に次回ターンまでの時間でソートする。
        self.queue.append([next_turn_time, callable_obje])
        self.queue.sort(key=lambda x: x[0])

    def update(self):
        current_pair = self.queue.pop(0)
        spent_time = current_pair[0]
        current_obje = current_pair[1]

        self.__decrease_turn_time(spent_time)
        current_obje.start_turn()

    def __decrease_turn_time(self, decreasing_time: int):
        self.queue = list(map(
            lambda x: [x[0] - decreasing_time, x[1]],
            self.queue
        ))

    def __str__(self):
        print_str = "<turn stack list>\n"

        for pair in self.queue:
            print_str += "[{0}, \"{1}\"]\n".format(
                pair[0],
                pair[1].name
            )

        return print_str


if __name__ == "__main__":
    class TestCallableObject(object):
        def __init__(self, name: str):
            self.name = name

        def start_turn(self):
            print("---next turn---")
            print(self.name)

    tm = TurnManager()

    hero = TestCallableObject("I'm Hero.")
    villager = TestCallableObject("I'm Villager.")
    enemy = TestCallableObject("I'm Enemy.")
    boss = TestCallableObject("I'm Boss.")

    tm.register(2, hero)
    tm.register(23, villager)
    tm.register(12, enemy)
    tm.register(33, boss)

    print(tm)

    tm.update()
    print(tm)
    tm.update()
    print(tm)
    tm.update()
    print(tm)
    tm.update()
    print(tm)
