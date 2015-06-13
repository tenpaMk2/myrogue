#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import view
import observer


class Controller(object):
    def __init__(self, observable: "observer.Observable", hero: "model.Hero", viewer: "view.Viewer"):
        self.observable = observable
        self.observer = observable.create_observer_and_return()

        self.hero = hero
        self.viewer = viewer

    def start_input(self):
        self.viewer.draw_message_before_input()
        arg = input()
        self.viewer.draw_message_after_input(arg)

        self.input_parser(arg)

    def input_parser(self, arg):
        if arg in (0, 'S', 's'):
            self.hero.move_south()
        elif arg in (1, 'E', 'e'):
            self.hero.move_east()
        elif arg in (2, 'N', 'n'):
            self.hero.move_north()
        elif arg in (3, 'W', 'w'):
            self.hero.move_west()
        elif arg in ('a', 'A'):
            self.hero.interact_to_front()
        elif arg in ('r', 'R'):
            self.hero.run()
        else:
            raise ValueError('Invalid command!')
