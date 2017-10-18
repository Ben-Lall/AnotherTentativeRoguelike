from bearlibterminal import terminal as blt
import colors
from symbol import Symbol


class Tile:
    """A tile of the world.  May be obstructed/passable and transparent/opaque."""

    def __init__(self, symbol=None, bkcolor=None, blocked=False, transparent=True):
        # symbol
        if symbol is None:
            self.symbol = Symbol(' ', blt.color_from_name("white"))
        else:
            self.symbol = symbol

        self.blocked = blocked
        self.transparent = transparent

    def render(self, x, y, renderer, fade=False):
        """Render this tile at the given world coordinates."""
        bkcolor = self._get_bk_color(fade)
        if isinstance(self.symbol, list):
            renderer.render_composite(x, y, self.symbol, 0, bkcolor)
        else:
            renderer.render(x, y, self.symbol, 0, bkcolor)

    def _get_bk_color(self, fade):
        if self.blocked:
            if fade:
                return colors.WALL_FADED
            else:
                return colors.WALL
        else:
            if fade:
                return colors.FLOOR_FADED
            else:
                return colors.FLOOR

    def unblock(self):
        """Unblock this tile and change its color to match."""
        self.blocked = False
