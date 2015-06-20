#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import model
import os
import json


def write_parameter_json(file_path, parameter):
    with open(file_path, mode='w', encoding="utf-8") as f:
        print("{0} : Writing...".format(file_path))
        json.dump(parameter.__dict__, f, indent=2)
    print("{0} : Writing...successful!!".format(file_path))


parameters_directory = os.path.join(".")
print("parameters directory:")
print(parameters_directory)
print('')

default_hero_parameter_file = os.path.join(parameters_directory, "default_hero_000.json")
default_hero_parameter = model.Parameter(
    hp=100,
    mp=50,
    strength=20,
    toughness=10,
    turn_period=5
)

write_parameter_json(default_hero_parameter_file, default_hero_parameter)

default_villager_parameter_file = os.path.join(parameters_directory, "default_villager_000.json")
default_villager_parameter = model.Parameter(
    hp=80,
    mp=10,
    strength=8,
    toughness=6,
    turn_period=14
)

write_parameter_json(default_villager_parameter_file, default_villager_parameter)

with open(default_hero_parameter_file, mode='r', encoding="utf-8") as f:
    hoge = json.load(f)
    reconstruct_hero_parameter = model.Parameter(
        hp=hoge["hp"],
        mp=hoge["mp"],
        strength=hoge["strength"],
        toughness=hoge["toughness"],
        turn_period=hoge["turn_period"]
    )
print(reconstruct_hero_parameter.__dict__)
print(default_hero_parameter.__dict__)
if reconstruct_hero_parameter.__dict__ == default_hero_parameter.__dict__:
    print("same!!")
else:
    print("not same...")
