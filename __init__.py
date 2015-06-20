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

# Model:Map
map_model = model.MapModel([5, 20])
# Model:TurnManager
turn_manager = turn.TurnManager()

# Viewer
viewer = view.Viewer(map_model)

# HeroとPeopleの作製
hero_pos = PositionAndDirection([1, 1], 0)
hero_parameter = model.ParameterFactory.make_hero()
hero = model.Hero(map_model, hero_pos, hero_parameter, turn_manager)

villager1_parameter = model.ParameterFactory.make_villager()
villager2_parameter = model.ParameterFactory.make_villager()
villager1 = model.Villager(map_model, PositionAndDirection([2, 2]), villager1_parameter, turn_manager, "Yo! Hage!")
villager2 = model.Villager(map_model, PositionAndDirection([1, 4]), villager2_parameter, turn_manager, "ya, Hage.")

# Mapへの登録
map_model.resister_map_object(hero)
map_model.resister_map_object(villager1)
map_model.resister_map_object(villager2)

# Controller
my_keyboard = controller.Controller(hero, viewer)

# Observerを追加
map_model.add_observer(observer.Observer(viewer, my_keyboard))
viewer.add_observer(observer.Observer(viewer, my_keyboard))

hero.add_observer(observer.Observer(viewer, my_keyboard))
villager1.add_observer(observer.NPCObserver(viewer, my_keyboard))
villager2.add_observer(observer.NPCObserver(viewer, my_keyboard))

my_keyboard.add_observer(observer.Observer(viewer, my_keyboard))

# TurnManagerに追加
hero_turn_entry = turn.TurnQueueEntryFactory.make_hero_turn_queue(hero._observers[0], 0)
turn_manager.register(hero_turn_entry)
villager1_turn_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(villager1.ai, 0)
turn_manager.register(villager1_turn_entry)
villager2_turn_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(villager2.ai, 0)
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
