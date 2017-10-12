from enum import Enum
from symbol import Symbol
import random as rand
import world
from bearlibterminal import terminal as blt


class _GenTileType(Enum):
    """Enumerator detailing the different types of world gen tiles."""
    EMPTY = 0
    ROOM = 1
    ROOM_WALL = 2
    CORRIDOR = 3
    CORRIDOR_WALL = 4


class _GenTile:
    """A tile containing extra information needed strictly for world generation."""
    def __init__(self, tile_type):
        self.tile_type = tile_type

    def render(self, x, y, renderer):
        """Render this tile at the given world coordinates."""
        if self.tile_type == _GenTileType.EMPTY:
            bkcolor = blt.color_from_argb(255, 0, 0, 50)
        elif self.tile_type == _GenTileType.ROOM:
            bkcolor = blt.color_from_argb(255, 0, 0, 30)
        elif self.tile_type == _GenTileType.ROOM_WALL:
            bkcolor = blt.color_from_argb(255, 0, 0, 70)
        else:
            bkcolor = blt.color_from_argb(255, 0, 0, 50)
        renderer.render(x, y, Symbol(' ', blt.color_from_name("white")), 0, bkcolor)


def generate_floor(floor):
    """Generate rooms and corridors for the given floor.  Expects a floor of completely blocked tiles, and the
    floor will be "carved" out of the existing floor."""
    blueprint = [[_GenTile(_GenTileType.EMPTY) for x in range(len(floor[0]))] for y in range(len(floor))]
    world.blueprint = blueprint

    start_pos = _place_dungeon_start(blueprint)
    #place_rooms(blueprint)

    _build_floor(blueprint, floor)
    return start_pos


#def place_rooms(blueprint):



def _place_dungeon_start(floor):
    """Place a room at one of the side centers of the floor.  Return a coordinate for a good start position."""
    # Room width and height are relative to entrance facing direction.
    # i.e. width refers to the left-right distance of the room if the player
    # is facing the exit. (not necessarily the x-width of the room.)
    start_room_width = 10
    start_room_height = 7

    # Decide if the room will be top/bottom or left/right
    if rand.random() <= 0.5:  # Top/bottom
        x = len(floor[0]) - int((len(floor[0]) - start_room_width) / 2)
        # Decide top or bottom:
        y = rand.randint(0, 1) * len(floor)

        _draw_rectangular_room(floor, x, max(y - start_room_height, 0), start_room_width, start_room_height)
        return x + int(start_room_width / 2), max(y - 1, 0)
    else:  # Left/right
        y = len(floor) - int((len(floor) - start_room_height) / 2)
        # Decide left or right:
        x = rand.randint(0, 1) * len(floor[0])

        _draw_rectangular_room(floor, max(x - start_room_height, 0), y, start_room_height, start_room_width)
        return max(x - 1, 0), y + int(start_room_width / 2)


def _draw_rectangular_room(blueprint, x, y, width, height):
    """Draw a rectangular room at the given coordinates with the given dimensions."""
    max_x = x + width
    max_y = y + height
    for i in range(y, max_y):
        for j in range(x, max_x):
                blueprint[i][j].tile_type = _GenTileType.ROOM
    mark_rectangular_walls(blueprint, x, y, width, height)


def mark_rectangular_walls(blueprint, x, y, width, height):
    """Mark the walls surrounding the given rectangular area with walls."""
    max_x = x + width
    max_y = y + height
    for j in range(x - 1, max_x):
        if is_in_bounds(blueprint, j, y - 1):
            blueprint[y - 1][j].tile_type = _GenTileType.ROOM_WALL
        if is_in_bounds(blueprint, j, max_y):
            blueprint[max_y][j].tile_type = _GenTileType.ROOM_WALL

    for i in range(y - 1, max_y):
        if is_in_bounds(blueprint, x - 1, i):
            blueprint[i][x - 1].tile_type = _GenTileType.ROOM_WALL
        if is_in_bounds(blueprint, max_x, i):
            blueprint[i][max_x].tile_type = _GenTileType.ROOM_WALL


def is_in_bounds(floor, x, y):
    """Determine if the given coordinates are within the bounds of the floor."""
    return 0 <= x < len(floor[0]) and 0 <= y < len(floor)


def _build_floor(blueprint, floor):
    """Build the floor using the given blueprint.  blueprint is a 2D array of GenTiles and floor is a 2D array of
    Tiles."""
    for i in range(len(blueprint)):
        for j in range(len(blueprint[0])):
            if blueprint[j][i].tile_type in [_GenTileType.CORRIDOR, _GenTileType.ROOM]:
                floor[j][i].unblock()
