from tile import Tile

FLOOR_WIDTH = 120
FLOOR_HEIGHT = 120


class World:
    """The game world.  Consists of tiles and gameplay objects."""
    FLOOR_WIDTH = FLOOR_WIDTH
    FLOOR_HEIGHT = FLOOR_HEIGHT

    current_floor = [[Tile(blocked=True) if (x in [0, FLOOR_WIDTH - 1] or y in [0, FLOOR_HEIGHT - 1]) else Tile(blocked=False) for x in range(FLOOR_WIDTH)] for y in range(FLOOR_HEIGHT)]
    current_floor[15][14] = Tile(blocked=True)
    current_floor_elements = []
    active_player = None  # Temporarily a member of this class.

    @staticmethod
    def add_player(player):
        World.current_floor_elements.append(player)
        if World.active_player is None:
            World.active_player = player
