#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")

import warnings

from position import PositionAndDirection
import controller
import model
import view
import observer
import turn


# Model:Map
map_model = model.MapModel([5, 20])
logging.info("made MapModel")

# Model:TurnManager
turn_manager = turn.TurnManager()
logging.info("made TurnManager")

# Viewer
viewer = view.Viewer(map_model)
logging.info("made Viewer")

# HeroとPeopleの作製
hero_pos = PositionAndDirection([1, 1], 0)
hero_parameter = model.ParameterFactory.make_hero()
hero = model.Hero(map_model, hero_pos, hero_parameter, turn_manager)
logging.info("made Hero at %r", hero.get_position())

villager1_parameter = model.ParameterFactory.make_villager()
villager2_parameter = model.ParameterFactory.make_villager()
villager1 = model.Villager(map_model, PositionAndDirection([2, 2]), villager1_parameter, turn_manager, "Yo! Hage!")
villager2 = model.Villager(map_model, PositionAndDirection([1, 4]), villager2_parameter, turn_manager, "ya, Hage.")
logging.info("made Villager1 at %r", villager1.get_position())
logging.info("made Villager2 at %r", villager2.get_position())

# Mapへの登録
map_model.register_obstacle(hero)
logging.info("registered Hero")
map_model.register_obstacle(villager1)
logging.info("registered Villager1")
map_model.register_obstacle(villager2)
logging.info("registered Villager2")

# Controller
my_keyboard = controller.Controller(hero, viewer)
logging.info("made Controller")

# Observerを追加
map_model.add_observer(observer.Observer(viewer, my_keyboard))
logging.info("add observer to map_model")
viewer.add_observer(observer.Observer(viewer, my_keyboard))
logging.info("add observer to viewer")

hero.add_observer(observer.Observer(viewer, my_keyboard))
logging.info("add observer to hero")
villager1.add_observer(observer.NPCObserver(viewer, my_keyboard))
logging.info("add observer to villager1")
villager2.add_observer(observer.NPCObserver(viewer, my_keyboard))
logging.info("add observer to villager2")

my_keyboard.add_observer(observer.Observer(viewer, my_keyboard))
logging.info("add observer to my_keyboard")

# TurnManagerに追加
hero_turn_entry = turn.TurnQueueEntryFactory.make_hero_turn_queue(hero._observers[0], 0)
turn_manager.register(hero_turn_entry)
logging.info("register hero to turn_manager : next_turn_time %r", hero_turn_entry.next_turn_time)
villager1_turn_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(villager1.ai, 0)
turn_manager.register(villager1_turn_entry)
logging.info("register villager1 to turn_manager : next_turn_time %r", villager1_turn_entry.next_turn_time)
villager2_turn_entry = turn.TurnQueueEntryFactory.make_npc_turn_queue(villager2.ai, 0)
turn_manager.register(villager2_turn_entry)
logging.info("register villager2 to turn_manager : next_turn_time %r", villager2_turn_entry.next_turn_time)


while True:
    turn_manager._print_queue()
    turn_manager.update()


warnings.warn("while Trueつってんだルルォ!?")
