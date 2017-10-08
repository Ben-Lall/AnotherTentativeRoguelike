from bearlibterminal import terminal
from tile import Tile

FLOOR_WIDTH = 40
FLOOR_HEIGHT = 40


class World:
    """The game world.  Consists of tiles and gameplay objects."""
    FLOOR_WIDTH = 40
    FLOOR_HEIGHT = 40

    current_floor = [[Tile(terminal.color_from_argb(255, 0, 0, 12)) for x in range(FLOOR_WIDTH)] for y in range(FLOOR_HEIGHT)]
    current_floor_elements = []
    active_player = None

    @staticmethod
    def add_player(player):
        World.current_floor_elements.append(player)
        if World.active_player is None:
            World.active_player = player
