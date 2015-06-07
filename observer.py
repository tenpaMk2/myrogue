#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import view


class Observable(object):
    def __init__(self):
        self.observer_list = []
        self.viewer = None

    def create_observer(self):
        # noinspection PyTypeChecker
        new_observer = Observer(self.viewer)
        self.observer_list.append(new_observer)

        return new_observer

    def change_viewer(self, viewer: "view.Viewer"):
        for observer in self.observer_list:
            observer.view = viewer
        self.viewer = viewer

        print("Successfully changed observer's viewer!")


# View-Model-Observerで循環参照してるので、初回だけはviewerにはNoneが入る。後でセットされる。
class Observer(object):
    def __init__(self, viewer: "view.Viewer"):
        self.view = viewer

    def update(self):
        self.view.draw()
