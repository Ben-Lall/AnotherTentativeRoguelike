from bearlibterminal import terminal as blt
from symbol import Symbol


class Tile:
    """A tile of the world.  May be obstructed/passable and transparent/opaque."""

    def __init__(self, symbol=None, bkcolor=None, blocked=False, transparent=True):
        # symbol
        if symbol is None:
            self.symbol = Symbol(' ', blt.color_from_name("white"))
        else:
            self.symbol = symbol

        # background color
        if bkcolor is None:
            if blocked:
                self.bkcolor = blt.color_from_argb(255, 0, 15, 120)
            else:
                self.bkcolor = blt.color_from_argb(255, 0, 0, 12)
        else:
            self.bkcolor = bkcolor

        self.blocked = blocked
        self.transparent = transparent

    def render(self, x, y, renderer):
        """Render this tile at the given world coordinates."""
        if isinstance(self.symbol, list):
            renderer.render_composite(x, y, self.symbol, 0, self.bkcolor)
        else:
            renderer.render(x, y, self.symbol, 0, self.bkcolor)
