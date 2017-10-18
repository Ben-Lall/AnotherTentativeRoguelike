from creature import Creature
from camera import Camera
from renderer import Renderer
from symbol import Symbol
import field_of_view as fov
from bearlibterminal import terminal as blt


class Player(Creature):
    """A controllable player character."""

    def __init__(self, pos, world_width, world_height):
        symbol = Symbol('@', blt.color_from_name("dark white"))
        super().__init__(pos[0], pos[1], symbol)
        self.camera = Camera(self.x, self.y, world_width, world_height)
        self.world_renderer = Renderer()
        self.sight_radius = 10
        self.memory_map = [[None for x in range(world_width)] for y in range(world_height)]
        self.fov_map = []

    def update_memory_map(self, world):
        self.fov_map = fov.get_fov_map(world.current_floor, (self.x, self.y), self.sight_radius)
        for (x, y) in self.fov_map:
            self.memory_map[y][x] = world.current_floor[y][x]

    def render_screen(self, world):
        """Render everything visible to this player to the screen."""
        self.world_renderer.transform(self.camera)
        # Render the tiles in the player's memory, faded
        for i in range(len(self.memory_map)):
            for j in range(len(self.memory_map[0])):
                if self.memory_map[i][j] is not None:
                    tile = self.memory_map[i][j]
                    tile.render(j, i, self.world_renderer, True)

        world.render(self.camera, self.world_renderer, self.memory_map, self.fov_map)

    def move(self, dx, dy, world):
        """Move the player and pan the camera to compensate."""
        super().move(dx, dy, world)
        self.camera.move_to(self.x, self.y)
