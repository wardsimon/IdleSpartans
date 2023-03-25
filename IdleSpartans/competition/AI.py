__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

import numpy as np

from typing import Dict

from IdleSpartans.components.common import World

CREATOR = 'IdleSpartans'

class PlayerAi:

    def __init__(self):
        self.team = CREATOR
        self.previous_positions = {}
        self.ntanks = {}
        self.nships = {}
        self.world: World = None
        self.enemy_world: Dict[World] = {}
        self.first_run = True

        self.closes_enemies = {}

    def build_enemies_world(self, info_dict: dict):
        for team in info_dict:
            if team != self.team:
                self.enemy_world[team] = World(team, worlds=self.enemy_world)

    def update_world(self, info_dict: dict, game_map):
        self.world.update_world(info_dict, game_map)
        for team in self.enemy_world:
            if team in info_dict:
                self.enemy_world[team].update_world(info_dict)

    def run_world(self):
        for key in self.world.world_objects:
            for uid in self.world.world_objects[key]:
                self.world.world_objects[key][uid].action()

    def run(self, t: float, dt: float, info: dict, game_map):

        if self.first_run:
            self.first_run = False
            self.world = World(self.team)
            self.build_enemies_world(info)
            self.world.worlds = self.enemy_world

        self.update_world(info, game_map)
        self.run_world()