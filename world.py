from tile import Tile

FLOOR_WIDTH = 40
FLOOR_HEIGHT = 40


class World:
    """The game world.  Consists of tiles and gameplay objects."""
    FLOOR_WIDTH = 40
    FLOOR_HEIGHT = 40

    current_floor = [[Tile(blocked=False) for x in range(FLOOR_WIDTH)] for y in range(FLOOR_HEIGHT)]
    current_floor[15][15] = Tile(blocked=True)
    current_floor_elements = []
    active_player = None  # Temporarily a member of this class.

    @staticmethod
    def add_player(player):
        World.current_floor_elements.append(player)
        if World.active_player is None:
            World.active_player = player
