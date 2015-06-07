#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import view
import observer


class Controller(object):
    def __init__(self, observable: "observer.Observable", hero: "model.Hero", viewer: "view.Viewer"):
        self.observable = observable
        self.observer = observable.create_observer()

        self.hero = hero
        self.viewer = viewer

    def start_input(self):
        self.viewer.draw_message_before_input()
        arg = input()
        self.viewer.draw_message_after_input(arg)

        self.input_parser(arg)

    def input_parser(self, arg):
        if arg in (0, 'S', 's'):
            self.hero.move_to(0)
        elif arg in (1, 'E', 'e'):
            self.hero.move_to(1)
        elif arg in (2, 'N', 'n'):
            self.hero.move_to(2)
        elif arg in (3, 'W', 'w'):
            self.hero.move_to(3)
        elif arg in ('a', 'A'):
            self.hero.interact_to_front()
        elif arg in ('r', 'R'):
            self.hero.run()
        else:
            raise ValueError('Invalid command!')
