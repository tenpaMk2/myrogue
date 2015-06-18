#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import view
import observer

# TODO ControllerにあてるObserverは普通のObserverで良いんだろうか。というかNPCObserverなんてもんがあっちゃまずいのか?
# ControllerにObserverを当てる意味はないのでは…。
# FIXME inputを始めるときにマップの描画もしちゃえばええんや！これでObserverもすっきりするんちゃう?
# Observerを使うのは正しい。Modelから直接ControllerやViewが見えてはいけない。
# しかし、どうやってHeroとVillagerのObserverを区別するかが問題だ。
class Controller(observer.Subject):
    def __init__(self, hero: "model.Hero", viewer: "view.Viewer"):
        observer.Subject.__init__(self)
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
        elif arg in ('i', 'I'):
            self.hero.interact_to_front()
        elif arg in ('r', 'R'):
            self.hero.run()
        else:
            raise ValueError('Invalid command!')
