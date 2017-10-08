from gameplay_object import GameplayObject


class Creature(GameplayObject):
    """A living creature capable of living and dying."""

    def __init__(self, x, y, symbol, color):
        super().__init__(symbol, color, x, y)
