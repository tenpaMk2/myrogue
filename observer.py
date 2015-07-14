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

    # notifyの呼び出しもとってMapModelなんだよね。turn_endのときしか更新しないなら、なんかもういらない感ある。
    def notify(self):
        for observer in self._observers:
            observer.update()


# FIXME 循環importをさけるためにこんな場所に。やはり、Observerが単体で動作するのはまずい気がする。
# ViewObserverとControllerObserverに分けたらどうか。
import view
import controller

from abc import ABCMeta, abstractmethod


class ObserverBase(metaclass=ABCMeta):
    def __init__(self, viewer: "view.Viewer", my_keyboard: "controller.Controller"):
        self.viewer = viewer
        self.controller = my_keyboard

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def update_turn_start(self):
        pass


class Observer(ObserverBase):
    def update(self):
        self.viewer.draw()

    def update_turn_start(self):
        self.viewer.draw()
        self.controller.start_input()


# turn_endはロジックに関わるので、Observerに書くべきではないと判断。

class NPCObserver(ObserverBase):
    def update(self):
        pass

    def update_turn_start(self):
        print("--start NPC turn--")
