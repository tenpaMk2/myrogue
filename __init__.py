#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

from position import PositionAndDirection
import controller
import model
import view
import observer
import turn

import warnings

# Observer
obs = observer.Observable()
# Model:Map
map_model = model.MapModel(obs, [5, 20])
# Model:TurnManager
turn_manager = turn.TurnManager()

# Viewer
viewer = view.Viewer(obs, map_model)
# ObserverにViewerを設定
obs.change_viewer(viewer)

# HeroとPeopleの作製
heropos = PositionAndDirection([1, 1], 0)
hero = model.Hero(map_model, heropos, turn_manager)

villager1 = model.Villager(map_model, PositionAndDirection([2, 2]), turn_manager, "Yo! Hage!")
villager2 = model.Villager(map_model, PositionAndDirection([1, 4]), turn_manager, "Hello, Hage!")
# Mapへの登録
map_model.resister_map_object(hero)
map_model.resister_map_object(villager1)
map_model.resister_map_object(villager2)

# Controller
my_keyboard = controller.Controller(obs, hero, viewer)
# ObserverにControllerを設定
obs.change_controller(my_keyboard)

# Observerを追加
hero.add_observer(observer.Observer(viewer, my_keyboard))
villager1.add_observer((observer.NPCObserver(viewer, my_keyboard)))
villager2.add_observer((observer.NPCObserver(viewer, my_keyboard)))

# TurnManagerに追加
hero_turn_entry = turn.TurnQueueEntryFactory.make_hero_turn_queue(hero._observers[0], 0)
turn_manager.register(hero_turn_entry)
villager1_turn_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(villager1.ai, 10)
turn_manager.register(villager1_turn_entry)
villager2_turn_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(villager2.ai, 10)
turn_manager.register(villager2_turn_entry)

# warnings.warn("ahoaho")
# warnings.warn("ahoaho")
# warnings.warn("ahoaho2")


while True:
    turn_manager._print_queue()
    turn_manager.update()



# hero.move_to(1)
# hero.move_to(0)
# hero.interact_to_front()
#
# hero.move_to(1)
# hero.interact_to_front()
