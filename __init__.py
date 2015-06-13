#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

from position import PositionAndDirection
import controller
import model
import view
import observer
import turn

# 生成する順番は
# Observable
# Model
# Viewer
# Hero
# Controller
# の順番である。

obs = observer.Observable()
map_model = model.MapModel(obs, [5, 20])
viewer = view.Viewer(obs, map_model)
obs.change_viewer(viewer)

turn_manager = turn.TurnManager()

heropos = PositionAndDirection([1, 1], 0)
hero = model.Hero(obs, map_model, heropos, turn_manager)
villager1 = model.Villager(obs, map_model, PositionAndDirection([2, 2]), turn_manager, "Yo! Hage!")
villager2 = model.Villager(obs, map_model, PositionAndDirection([1, 4]), turn_manager, "Hey! Hage!")

map_model.resister_map_object(hero)
map_model.resister_map_object(villager1)
map_model.resister_map_object(villager2)

my_keyboard = controller.Controller(obs, hero, viewer)
obs.change_controller(my_keyboard)


while True:
    turn_manager.update()



# hero.move_to(1)
# hero.move_to(0)
# hero.interact_to_front()
#
# hero.move_to(1)
# hero.interact_to_front()
