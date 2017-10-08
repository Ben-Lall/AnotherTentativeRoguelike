from bearlibterminal import terminal as blt


class Renderer:
    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0

    def render(self, x, y, symbol, layer, bkcolor=None):
        """Render the given symbol.  May modify the state of terminal.color or terminal.bkcolor."""
        # Set terminal
        blt.layer(layer)
        if bkcolor is not None:
            blt.bkcolor(bkcolor)
        blt.color(symbol.color)

        draw_x, draw_y = x + self.x_offset, y + self.y_offset
        blt.put_ext(draw_x, draw_y, symbol.dx, symbol.dy, symbol.char, None)

    def render_composite(self, x, y, symbol, layer, bkcolor=None):
        """Render a composite symbol."""
        blt.composition(blt.TK_ON)
        for s in symbol:
            self.render(x, y, s, layer, bkcolor)
        blt.composition(blt.TK_OFF)

    def transform(self, camera):
        """Transform this Renderer's offset to match the camera."""
        self.x_offset = -camera.x
        self.y_offset = -camera.y
