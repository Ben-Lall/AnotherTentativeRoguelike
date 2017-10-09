from gameplay_object import GameplayObject
import utilities as util


class Creature(GameplayObject):
    """A living creature capable of living and dying."""

    def __init__(self, x, y, symbol, ):
        super().__init__(symbol, x, y)

    def render(self, renderer):
        super().render(renderer, 1)

    def move(self, dx, dy):
        if util.is_unobstructed(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
