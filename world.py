from tile import Tile

FLOOR_WIDTH = 120
FLOOR_HEIGHT = 120


class World:
    """The game world.  Consists of tiles and gameplay objects."""
    FLOOR_WIDTH = FLOOR_WIDTH
    FLOOR_HEIGHT = FLOOR_HEIGHT

    def __init__(self):
        self.current_floor = [[Tile(blocked=True) if (x in [0, FLOOR_WIDTH - 1] or y in [0, FLOOR_HEIGHT - 1]) else Tile(blocked=False) for x in range(FLOOR_WIDTH)] for y in
                         range(FLOOR_HEIGHT)]
        self.current_floor[15][14] = Tile(blocked=True)
        self.current_floor[15][13] = Tile(blocked=True)
        self.current_floor[16][14] = Tile(blocked=True)
        self.current_floor[16][13] = Tile(blocked=True)
        self.current_floor_elements = []
        self.active_player = None

    def add_player(self, player):
        """Add a playable creature to this world."""
        self.current_floor_elements.append(player)
        if self.active_player is None:
            self.active_player = player

    def is_in_bounds(self, x, y):
        """Check if the given coordinates are within the bounds of a floor."""
        return 0 <= x < World.FLOOR_WIDTH and 0 <= y < World.FLOOR_HEIGHT

    def is_unobstructed(self, x, y):
        """Check if the given coordinates of the current floor is unobstructed."""
        return not self.current_floor[y][x].blocked

    def render(self, camera, renderer):
        """Render the portion of the world visible by the given camera."""
        (draw_x, draw_y) = camera.get_draw_start_pos()
        (max_x, max_y) = camera.get_max_draw_pos()
        # Draw all visible tiles
        for i in range(draw_y, max_y):
            for j in range(draw_x, max_x):
                tile = self.current_floor[i][j]
                tile.render(j, i, renderer)

        # Draw all visible gameplay objects
        for e in self.current_floor_elements:
            if camera.is_within_bounds(e.x, e.y):
                e.render(renderer)
