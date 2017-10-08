class Tile:
    """A tile of the world.  May be obstructed/passable and transparent/opaque."""

    def __init__(self, color, blocked=False, transparent=True):
        self.color = color
        self.blocked = blocked
        self.transparent = transparent
