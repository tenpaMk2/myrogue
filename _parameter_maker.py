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


parameters_directory = os.path.join("./parameters")
print("parameters directory:")
print(parameters_directory)
print('')

# Hero
default_hero_parameter_file = os.path.join(parameters_directory, "default_hero_000.json")
default_hero_parameter = model.Parameter(
    hp=100,
    mp=50,
    strength=20,
    toughness=10,
    turn_period=5,
    fov_distance=10
)
write_parameter_json(default_hero_parameter_file, default_hero_parameter)

# Villager
default_villager_parameter_file = os.path.join(parameters_directory, "default_villager_000.json")
default_villager_parameter = model.Parameter(
    hp=20,
    mp=5,
    strength=8,
    toughness=3,
    turn_period=14,
    fov_distance=5
)
write_parameter_json(default_villager_parameter_file, default_villager_parameter)

# Enemy
default_enemy_parameter_file = os.path.join(parameters_directory, "default_enemy_000.json")
default_enemy_parameter = model.Parameter(
    hp=20,
    mp=5,
    strength=8,
    toughness=3,
    turn_period=14,
    fov_distance=5
)
write_parameter_json(default_enemy_parameter_file, default_enemy_parameter)

print("---------check load------------")

with open(default_hero_parameter_file, mode='r', encoding="utf-8") as f:
    hoge = json.load(f)
    reconstruct_hero_parameter = model.Parameter(**hoge)
print(reconstruct_hero_parameter.__dict__)
print(default_hero_parameter.__dict__)
if reconstruct_hero_parameter.__dict__ == default_hero_parameter.__dict__:
    print("same!!")
else:
    print("not same...")
