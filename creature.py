from gameplay_object import GameplayObject
import utilities as util
import field_of_view as fov
import pathfinding
from enum import Enum


class Faction(Enum):
    """Enumerator cataloguing the different factions."""
    PLAYER = 0
    MONSTER = 1

    @staticmethod
    def enemies_of(faction_type):
        if faction_type == Faction.PLAYER:
            return [Faction.MONSTER]
        if faction_type == Faction.MONSTER:
            return [Faction.PLAYER]


class Creature(GameplayObject):
    """A living creature capable of living and dying."""

    def __init__(self, x, y, symbol, sight_radius=8, faction=Faction.MONSTER):
        super().__init__(symbol, x, y)
        self.faction = faction
        self.sight_radius = sight_radius
        self.target_pos = None

    def render(self, renderer):
        super().render(renderer, 1)

    def take_turn(self, world):
        fov_map = fov.get_fov_map(world.current_floor, (self.x, self.y), self.sight_radius)
        enemies = world.creatures_of_faction(Faction.enemies_of(self.faction))

        # Find a new target, if possible.
        self._acquire_target(fov_map, enemies)
        if self.target_pos is not None:
            next_tile = pathfinding.get_next_tile(world.current_floor, (self.x, self.y), self.target_pos)
            self.move(next_tile[0] - self.x, next_tile[1] - self.y, world)

    def _acquire_target(self, fov_map, enemies):
        lowest_distance = None
        target = None

        for c in (c for c in enemies if (c.x, c.y) in fov_map):
            distance = util.euc_distance((self.x, self.y), (c.x, c.y))
            if target is None or distance < lowest_distance:
                lowest_distance = distance
                target = c

        if target is not None:
            self.target_pos = (target.x, target.y)

    def move(self, dx, dy, world):
        target = (self.x + dx, self.y + dy)
        if util.is_in_bounds(world.current_floor, target[0], target[1]) and world.is_unobstructed(target[0], target[1]):
            self.x += dx
            self.y += dy
