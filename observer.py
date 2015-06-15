#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

# TODO 依存してるモジュールが無くてもテストできるように、そのメソッドだけもつダミークラスをテスト用に作ったほうがいいかも。
# TODO そもそもObserverにいろいろ役割を持たせ過ぎなんじゃないだろうか…。

class Subject(object):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()

# FIXME 循環importをさけるためにこんな場所に。やはり、Observerが単体で動作するのはまずい気がする。
# ViewObserverとControllerObserverに分けたらどうか。
import view
import controller


# View-Model-Observerで循環参照してるので、初回だけはviewerにはNoneが入る。後でセットされる。
# 追記：controllerも後でセットされる。
class Observer(object):
    def __init__(self, viewer: "view.Viewer", my_keyboard: "controller.Controller"):
        self.view = viewer
        self.controller = my_keyboard

    def update(self):
        self.view.draw()

    def update_turn_start(self):
        self.view.draw()
        self.controller.start_input()


# turn_endはロジックに関わるので、Observerに書くべきではないと判断。

# FIXME 継承でメソッドを潰すのは良くないと思うんだよなあ。
# FIXME そのためにはABC使わないとだめか?
class NPCObserver(Observer):
    def update(self):
        pass

    def update_turn_start(self):
        print("--start NPC turn--")
