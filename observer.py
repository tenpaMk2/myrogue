#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import view
import controller

# TODO 依存してるモジュールが無くてもテストできるように、そのメソッドだけもつダミークラスをテスト用に作ったほうがいいかも。

class Observable(object):
    def __init__(self):
        self.observer_list = []
        self.viewer = None
        self.controller = None

    def create_observer(self):
        # noinspection PyTypeChecker
        new_observer = Observer(self.viewer, self.controller)
        self.observer_list.append(new_observer)

        return new_observer

    def change_viewer(self, viewer: "view.Viewer"):
        for observer in self.observer_list:
            observer.view = viewer
        self.viewer = viewer

        print("Successfully changed observer's viewer!")

    def change_controller(self, controller: "controller.Controller"):
        for observer in self.observer_list:
            observer.controller = controller
        self.controller = controller

        print("Successfully changed observer's controller!")


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
