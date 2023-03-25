from __future__ import annotations

__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from typing import Union, TYPE_CHECKING

import numpy as np

from .common import Common

if TYPE_CHECKING:
    from supremacy.base import BaseProxy
    import numpy.typing as npt


class Base(Common):
    def __init__(self, obj_type: str, input_obj: BaseProxy, world):
        self.base_class = obj_type

        self._world = world
        self._callable = input_obj

        self.uid = input_obj.uid

        self.x = input_obj.x
        self.y = input_obj.y

        self._crystal = input_obj.crystal
        self.mines = input_obj.mines

        self.tanks = {}
        self.jets = {}
        self.ships = {}
        self.time = 0
        self.map = None

    def cost(self, costable: Union[Common, str]) -> float:
        if isinstance(costable, str):
            return self._callable.cost(costable)
        return self._callable.cost(costable.base_class)

    def update_object(self, input_obj: BaseProxy, game_map: npt.ndarray):
        self._callable = input_obj

        self.x = input_obj.x
        self.y = input_obj.y

        self._crystal = input_obj.crystal
        self.mines = input_obj.mines
        self.map = game_map

    @property
    def crystal(self):
        return self._crystal

    @crystal.setter
    def crystal(self, new_value: float):
        self._crystal = new_value

    def build_mine(self):
        self.crystal -= self.cost("mine")
        self._callable.build_mine()

    def build_tank(self, heading: float):
        self.crystal -= self.cost('tank')
        self._callable.build_tank(heading=heading)

    def build_ship(self, heading: float):
        self.crystal -= self.cost('ship')
        self._callable.build_ship(heading=heading)

    def build_jet(self, heading: float):
        self.crystal -= self.cost("jet")
        self._callable.build_jet(heading=heading)

    def action(self):

        if self.mines < 3:
            if self.mines == 1 and len(self.tanks) == 0 and self.crystal > self.cost('tank'):
                self.build_tank(heading=360 * np.random.random())
                return
            elif self.mines == 3 and len(self.tanks) == 1 and self.crystal > self.cost("tank"):
                self.build_tank(heading=360 * np.random.random())
            if self.crystal > self.cost("mine"):
                self.build_mine()
            else:
                return
        if self.crystal > self.cost('tank') and len(self.tanks) < 6:
            self.build_tank(heading=360 * np.random.random())
            return
        if self.crystal > self.cost('ship') and len(self.ships) < 3:
            self.build_ship(heading=360 * np.random.random())
        if self.crystal > self.cost('jet'):
            self.build_jet(heading=360 * np.random.random())
