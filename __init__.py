#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

from position import PositionAndDirection
import controller
import model
import view
import observer


obs = observer.Observable()
map_model = model.MapModel(obs, [5, 20])
viewer = view.Viewer(obs, map_model)
obs.change_viewer(viewer)

heropos = PositionAndDirection([1,1], 0)
hero = model.Hero(obs, map_model, heropos)

map_model.resister_map_object(hero)

hero.move_to(0)



