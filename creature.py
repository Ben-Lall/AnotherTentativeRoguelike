from gameplay_object import GameplayObject
import utilities as util


class Creature(GameplayObject):
    """A living creature capable of living and dying."""

    def __init__(self, x, y, symbol, ):
        super().__init__(symbol, x, y)

    def render(self, renderer):
        super().render(renderer, 1)

    def move(self, dx, dy, world):
        target = (self.x + dx, self.y + dy)
        if util.is_in_bounds(world.current_floor, target[0], target[1]) and world.is_unobstructed(target[0], target[1]):
            self.x += dx
            self.y += dy
