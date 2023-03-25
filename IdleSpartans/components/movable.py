from __future__ import annotations

__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'


import numpy as np
from typing import Union, TYPE_CHECKING
from .common import Common

if TYPE_CHECKING:
    from supremacy.vehicles import VehicleProxy
    import numpy.typing as npt
    from .common import World

class Movable(Common):
    def __init__(self, base_class: str, input_obj: VehicleProxy, world: World):

        self._world = world
        self.team = input_obj.team

        self.base_class = base_class

        self._callable = input_obj

        self.map = map

        self.uid = input_obj.uid
        # Update the shared dict, note the plural
        try:
            att = getattr(self._world.world_objects["bases"][input_obj.owner.uid], self.base_class + "s")
            att[self.uid] = self
        except AttributeError:
            pass


        self.x = input_obj.x
        self.y = input_obj.y

        self.speed = input_obj.speed
        self.heading = input_obj.heading
        self.stopped = input_obj.stopped
        self.vector = input_obj.vector

        self.health = input_obj.health
        self.attack = input_obj.attack

        self.previous_position = np.array([0, 0])

        self.time = 0

    @property
    def position(self) -> 'npt.NDArray[np.float64]':
        return np.array([self.x, self.y])

    def update_object(self, input_obj: VehicleProxy, game_map=None):
        self._callable = input_obj

        self.previous_position = self.position

        self.x = input_obj.x
        self.y = input_obj.y

        self.speed = input_obj.speed
        self.heading = input_obj.heading
        self.stopped = input_obj.stopped
        self.vector = input_obj.vector

        self.health = input_obj.health
        self.attack = input_obj.attack
        self.map = game_map

    @property
    def stuck(self):
        return np.all(self.position == self.previous_position)

    def get_distance(self, x: float, y: float) -> float:
        return self._callable.get_distance(x, y)

    def stop(self):
        self._callable.stop()

    def set_heading(self, heading: float):
        self._callable.set_heading(heading)

    def goto(self, x: float, y: float):
        self._callable.goto(x, y)

    def action(self):
        pass


class Tank(Movable):

    BASE_CLASS = "tank"

    def __init__(self, input_obj: object, world: World):
        super().__init__(self.BASE_CLASS, input_obj, world)

    def action(self):

        my_base = self._world.my_closest("bases", self.x, self.y)

        if self.get_distance(my_base.x, my_base.y) < 15 and np.sum([tank.get_distance(my_base.x, my_base.y) < 15 for tank in self._world.world_objects["tanks"].values()]) < 6:
            dx = np.random.randint(3, 6)
            dy = np.random.randint(3, 6)
            if self.get_distance(my_base.x + dx, my_base.y + dy) == 0:
                self.stop()
            else:
                self.goto(my_base.x, my_base.y)
            return

        closest_bases = self._world.closest_base(self.x, self.y)
        if closest_bases is not None and self.get_distance(closest_bases.x, closest_bases.y) < 50:
            self.goto(closest_bases.x, closest_bases.y)
            return
        closest_tanks = self._world.closest_tank(self.x, self.y)
        if closest_tanks is not None:
            self.goto(closest_tanks.x, closest_tanks.y)
            return
        closest_jets = self._world.closest_jet(self.x, self.y)
        if closest_jets is not None:
            self.goto(closest_jets.x, closest_jets.y)
            return
        if self.stuck:
            self.set_heading(np.random.random() * 360.0)

class Ship(Movable):

    BASE_CLASS = "ship"

    def __init__(self, input_obj: object, world: World):
        super().__init__(self.BASE_CLASS, input_obj, world)

    def convert_to_base(self):
        self._callable.convert_to_base()

    def action(self):
        if self.stuck:
            nearest_base = self._world.my_closest("bases", self.x, self.y)
            if (nearest_base is not None and self.get_distance(nearest_base.x, nearest_base.y) > 40) or len(self._world.world_objects["bases"]) < 3:
                self.convert_to_base()
                return
            else:
                self.set_heading(np.random.random() * 360)
        else:
            closest_ship = self._world.closest_ship(self.x, self.y)
            if closest_ship is not None:
                self.goto(closest_ship.x, closest_ship.y)
                return


class Jet(Movable):

    BASE_CLASS = "jet"

    def __init__(self, input_obj: object, world: World):
        super().__init__(self.BASE_CLASS, input_obj, world)

    def action(self):
        closest_base = self._world.closest_base(self.x, self.y)
        if closest_base is not None:
            self.goto(closest_base.x, closest_base.y)
        else:
            if self.stuck:
                self.set_heading(np.random.random()*360)