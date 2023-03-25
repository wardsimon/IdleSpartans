from __future__ import annotations

__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from abc import ABC, abstractmethod
import supremacy.tools as tls

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from IdleSpartans.components.movable import Tank, Ship, Jet
    from IdleSpartans.components.stationary import Base

class Common(ABC):
    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def update_object(self, input_obj):
        pass


class World:

    def __init__(self, team: str, worlds = None):
        self.team = team
        self.world_objects = {'bases': {}, 'tanks': {}, 'ships': {}, 'jets': {}}

        from IdleSpartans.components.movable import Tank, Ship, Jet
        from IdleSpartans.components.stationary import Base
        self._CLS = {'base': Base, 'tank': Tank, 'ship': Ship, 'jet': Jet}
        self.worlds = worlds

    def update_world(self, info_dict: dict, game_map = None):

        known_bases = set(self.world_objects['bases'].keys())
        known_tanks = set(self.world_objects['tanks'].keys())
        known_ships = set(self.world_objects['ships'].keys())
        known_jets = set(self.world_objects['jets'].keys())

        if "bases" in info_dict[self.team]:
            for base in info_dict[self.team]['bases']:
                if base.uid not in self.world_objects['bases']:
                    self.world_objects['bases'][base.uid] = \
                        self._CLS["base"]('base', base, self)
                else:
                    # The base still exists
                    known_bases.remove(base.uid)
                    self.world_objects['bases'][base.uid].update_object(base, game_map)
        for base in known_bases:
            # The base no longer exists
            del self.world_objects['bases'][base]

        if "tanks" in info_dict[self.team]:
            for tank in info_dict[self.team]['tanks']:
                if tank.uid not in self.world_objects['tanks']:
                    self.world_objects['tanks'][tank.uid] = self._CLS["tank"](tank, self)
                else:
                    # The tank still exists
                    known_tanks.remove(tank.uid)
                    self.world_objects['tanks'][tank.uid].update_object(tank, game_map)

        for tank in known_tanks:
            # The tank no longer exists
            del self.world_objects['tanks'][tank]

        if "ships" in info_dict[self.team]:
            for ship in info_dict[self.team]['ships']:
                if ship.uid not in self.world_objects['ships']:
                    self.world_objects['ships'][ship.uid] = self._CLS["ship"](ship, self)
                else:
                    # The ship still exists
                    known_ships.remove(ship.uid)
                    self.world_objects['ships'][ship.uid].update_object(ship, game_map)

        for ship in known_ships:
            # The ship no longer exists
            del self.world_objects['ships'][ship]

        if "jets" in info_dict[self.team]:
            for jet in info_dict[self.team]['jets']:
                if jet.uid not in self.world_objects['jets']:
                    self.world_objects['jets'][jet.uid] = self._CLS["jet"](jet, self)
                else:
                    # The jet still exists
                    known_jets.remove(jet.uid)
                    self.world_objects['jets'][jet.uid].update_object(jet, game_map)
        for jet in known_jets:
            # The jet no longer exists
            del self.world_objects['jets'][jet]

    def closest_base(self, x: float, y: float) -> Optional[Base]:
        closest = None
        closest_distance = None
        for world in self.worlds.values():
            for base in world.world_objects['bases'].values():
                distance = tls.distance_on_torus(x, y, base.x, base.y)
                if closest_distance is None or distance < closest_distance:
                    closest = base
                    closest_distance = distance
        return closest

    def closest_tank(self, x: float, y: float) -> Optional[Tank]:
        closest = None
        closest_distance = None
        for world in self.worlds.values():
            for tank in world.world_objects['tanks'].values():
                distance = tls.distance_on_torus(x, y, tank.x, tank.y)
                if closest_distance is None or distance < closest_distance:
                    closest = tank
                    closest_distance = distance
        return closest

    def closest_ship(self, x: float, y: float) -> Optional[Ship]:
        closest = None
        closest_distance = None
        for world in self.worlds.values():
            for ship in world.world_objects['ships'].values():
                distance = tls.distance_on_torus(x, y, ship.x, ship.y)
                if closest_distance is None or distance < closest_distance:
                    closest = ship
                    closest_distance = distance
        return closest

    def closest_jet(self, x: float, y: float) -> Optional[Jet]:
        closest = None
        closest_distance = None
        for world in self.worlds.values():
            for jet in world.world_objects['jets'].values():
                distance = tls.distance_on_torus(x, y, jet.x, jet.y)
                if closest_distance is None or distance < closest_distance:
                    closest = jet
                    closest_distance = distance
        return closest

    def my_closest(self, item: str, x: float, y: float) -> Optional[Common]:
        items = self.world_objects[item].values()
        closest = None
        closest_distance = None
        for item in items:
            distance = tls.distance_on_torus(x, y, item.x, item.y)
            if distance > 0 and closest_distance is None or distance < closest_distance:
                closest = item
                closest_distance = distance
        return closest
