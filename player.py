from creature import Creature
from camera import Camera
from renderer import Renderer
from bearlibterminal import terminal


class Player(Creature):
    """A controllable player character."""

    def __init__(self):
        super().__init__(15, 15, '@', terminal.color_from_name("dark white"))
        self.camera = Camera(0, 0)
        self.world_renderer = Renderer()

    def render_screen(self, world):
        """Render everything visible to this player to the screen."""
        self.world_renderer.transform(self.camera)
        self.camera.render(world, self.world_renderer)

