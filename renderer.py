from bearlibterminal import terminal


class Renderer:
    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0

    def render(self, x, y, symbol, color, background, dx=0, dy=0):
        """Render the given symbol.  May modify the state of terminal.color or terminal.bkcolor."""
        if background:
            terminal.bkcolor(color)
        else:
            terminal.color(color)
        draw_x, draw_y = x + self.x_offset, y + self.y_offset
        terminal.put_ext(draw_x, draw_y, dx, dy, symbol, None)

    def render_composite(self, x, y, symbol, dx=0, dy=0):
        """Render a composite symbol."""
        terminal.composition(terminal.TK_ON)
        for c in symbol:
            self.render(x, y, c.symbol, c.color, c.dx, c.dy)
        terminal.composition(terminal.TK_OFF)

    def transform(self, camera):
        """Transform this Renderer's offset to match the camera."""
        self.x_offset = -camera.x
        self.y_offset = -camera.y
