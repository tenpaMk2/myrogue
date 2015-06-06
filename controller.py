#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import view
import observer

# FIXME ControllerはHeroを知ってないとだめだ。

class Controller(object):
    def __init__(self, observable: "observer.Observable", map_model: "model.MapModel", viewer: "view.Viewer"):
        self.observable = observable
        self.observer = observable.create_observer()

        self.map_model = map_model
        self.viewer = viewer

    def start_input(self):
        self.viewer.draw_message_before_input()
        arg = input()
        self.viewer.draw_message_after_input(arg)

    def input_parser(self, arg):
        if arg in (0, 'S'):
            pass


