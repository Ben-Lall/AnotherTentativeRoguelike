from gameplay_object import GameplayObject


class Creature(GameplayObject):
    """A living creature capable of living and dying."""

    def __init__(self, x, y, symbol, ):
        super().__init__(symbol, x, y)

    def render(self, renderer):
        super().render(renderer, 1)
