from tile import Tile
import world_generator as gen
from renderer import Renderer
from bearlibterminal import terminal as blt

FLOOR_WIDTH = 80
FLOOR_HEIGHT = 50
blueprint = 0


class World:
    """The game world.  Consists of tiles and gameplay objects."""
    FLOOR_WIDTH = FLOOR_WIDTH
    FLOOR_HEIGHT = FLOOR_HEIGHT

    def __init__(self):
        self.current_floor = [[Tile(blocked=True) for x in range(FLOOR_WIDTH)] for y in range(FLOOR_HEIGHT)]
        self.current_floor_elements = []
        self.active_player = None

    def generate_floor(self):
        return gen.generate_floor(self.current_floor)

    def add_player(self, player):
        """Add a playable creature to this world."""
        self.current_floor_elements.append(player)
        if self.active_player is None:
            self.active_player = player

    def is_unobstructed(self, x, y):
        """Check if the given coordinates of the current floor is unobstructed."""
        return not self.current_floor[y][x].blocked

    def render(self, camera, renderer, memory_map, fov_map):
        """Render the portion of the world visible by the given camera"""

        # Draw all tiles currently in the player's field of vision with no modifications.
        for (j, i) in fov_map:
            tile = self.current_floor[i][j]
            tile.render(j, i, renderer)

        # Draw all visible gameplay objects
        for e in self.current_floor_elements:
            if camera.is_within_bounds(e.x, e.y):
                e.render(renderer)
