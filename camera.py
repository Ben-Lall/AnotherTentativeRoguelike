import utilities as util
import math
from bearlibterminal import terminal as blt


class Camera:
    """A camera that is used for rendering a specific region."""

    def __init__(self, x, y, world):
        self.world_width = world.FLOOR_WIDTH
        self.world_height = world.FLOOR_HEIGHT
        self.width = blt.state(blt.TK_WIDTH)
        self.height = blt.state(blt.TK_HEIGHT)
        self.x = x
        self.y = y
        self.pan(0, 0)

    def pan(self, dx, dy):
        """Pan the camera in the direction specified by (dx, dy)."""
        self.x = int(util.clamp(self.x + dx, self.width / 2, self.world_width - self.width / 2))
        self.y = int(util.clamp(self.y + dy, self.height / 2, self.world_height - self.height / 2))

    def move_to(self, x, y):
        """Move the camera as close to the given coordinates as possible, while staying within the acceptable world bounds."""
        self.x = x
        self.y = y
        self.pan(0, 0)

    def is_within_bounds(self, x, y):
        """Determine if the given coordinates (x, y) are within the visible boundaries of this camera."""
        (draw_x, draw_y) = self.get_draw_start_pos()
        return draw_x <= x <= draw_x + self.width and draw_y <= y <= draw_y + self.height

    def get_draw_start_pos(self):
        return (int(util.clamp(self.x - self.width / 2, 0, self.world_width - self.width)),
                int(util.clamp(self.y - self.height / 2, 0, self.world_height - self.height)))

    def get_max_draw_pos(self):
        return (min(self.x + int(math.ceil(self.width / 2)), self.world_width),
                min(self.y + int(math.ceil(self.height / 2)), self.world_height))
