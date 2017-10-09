from creature import Creature
from camera import Camera
from renderer import Renderer
from symbol import Symbol
from bearlibterminal import terminal as blt


class Player(Creature):
    """A controllable player character."""

    def __init__(self, world):
        symbol = Symbol('@', blt.color_from_name("dark white"))
        super().__init__(15, 15, symbol)
        self.camera = Camera(self.x, self.y, world)
        self.world_renderer = Renderer()

    def render_screen(self, world):
        """Render everything visible to this player to the screen."""
        self.world_renderer.transform(self.camera)
        self.camera.render(self.world_renderer)

    def move(self, dx, dy):
        """Move the player and pan the camera to compensate."""
        super().move(dx, dy)
        self.camera.move_to(self.x, self.y)
